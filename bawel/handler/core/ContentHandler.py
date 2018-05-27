import os
import random
import sys
import tempfile
from typing import Dict, List, Union, Optional, Tuple

from flask import request
from linebot.models import TextSendMessage, TextMessage, TemplateSendMessage, StickerSendMessage
from linebot.models.responses import MessageContent

from bawel.action.ActionUtils import handle_action, dispatch_action
from bawel.constant.ActionMapper import ACTION_MAPPER
from bawel.constant.StateConstant import STATE_ADD_PENGELUARAN, STATE_IMAGE_ADD_PENGELUARAN, REQUEST_STATE

from bawel.processor.TextProcessor import TextProcessor

from bawel.util.CheckMoney import CheckMoney
from bawel.util.ExpenseDetector import ExpenseDetector
from bawel.util.JsonToQuery import JsonToQuery
from bawel.util.Sticker import line_sticker_nums


class Image:
    def __init__(self, location: str, size: str):
        self.location = location
        self.size = size


ResponseList = Optional[List[Union[TextMessage, TextSendMessage]]]

token_kata = os.getenv('TOKEN_KATA', '')
token_google = os.getenv('GOOGLE_MAP_TOKEN', '')

text_processor = TextProcessor(token_kata)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'bawel', 'static', 'tmp', 'line')


class ContentHandler:

    @staticmethod
    def handle_text(user_state: Dict, text: str, entities_resolver) -> Tuple[Dict, ResponseList]:
        # entities = entities_resolver.get_entities()

        if text == '@bye':
            # line_bot_api.reply_message(
            #     event.reply_token, TextMessage(text='Leaving group'))
            # line_bot_api.leave_group(id)
            return user_state, None

        if 'si bawel tolong' == text.lower():
            text = '/help'
            user_state, output = handle_action(text, text, user_state)
            return user_state, [TextMessage(text=output)]

        s = text.split(" ")
        if user_state.get('before_state'):
            if user_state['before_state'] == STATE_ADD_PENGELUARAN:
                cm = str(CheckMoney.process_text(text))
                if not cm == "None":
                    user_state['state_id'] = STATE_IMAGE_ADD_PENGELUARAN
                    user_state, output = dispatch_action(
                        ACTION_MAPPER[user_state['state_id']], *(cm, "", user_state))
                    return user_state, [TextSendMessage(text=output)]
                else:
                    output = 'masukkan tulisan harga atau gambar bon'
                    return user_state, [TextSendMessage(text=output)]

        if REQUEST_STATE.get(s[0]):
            try:
                user_state, output = handle_action(text, text, user_state)
                if type(output[0]) == TemplateSendMessage:
                    return user_state, output
                else:
                    return user_state, [TextMessage(text=output)]
            except:
                return user_state, [TextMessage(text="ketik 'si bawel tolong' kak")]

        try:
            text_processor.process_text(text)
            json = text_processor.get_json_to_sent()
            resp_text = JsonToQuery.parse_json(json)

            if not json.get('error'):
                user_state, output = handle_action(text, resp_text, user_state)
            else:
                output = resp_text

            if type(output[0]) == TemplateSendMessage:
                return user_state, output
            else:
                return user_state, [TextMessage(text=output)]

        except:
            print(sys.exc_info())
            return user_state, [
                TextSendMessage(
                    text="Keyword tidak ditemukan, tolong ketik 'si bawel tolong' atau '/help'"),
                StickerSendMessage(
                    package_id=3,
                    sticker_id=random.choice(line_sticker_nums))
            ]

    @staticmethod
    def handle_join(type):
        return 'Hai, si bawel telah join ' + type + ' ini. ' \
               'Mohon bantuannya, ketik "si bawel tolong" atau "/help" ya kak'

    @staticmethod
    def handle_image(user_state: Dict, message_content: MessageContent) -> Tuple[Dict, ResponseList]:

        if not user_state.get('before_state'):
            return user_state, None

        ext = 'jpg'
        with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
            tempfile_path = tf.name

        dist_path = tempfile_path + '.' + ext
        dist_name = os.path.basename(dist_path)
        os.rename(tempfile_path, dist_path)
        try:
            total_amount = ExpenseDetector.check_for_total(str(dist_path))
            if not total_amount:
                user_state, output = user_state, "Gambar tidak terbaca \nCoba lagi dengan gambar yang lebih baik"
            else:
                user_state['state_id'] = STATE_IMAGE_ADD_PENGELUARAN
                user_state, output = dispatch_action(ACTION_MAPPER[user_state['state_id']],
                                                     *(total_amount,
                                                       request.host_url + os.path.join('tmp', dist_name),
                                                       user_state))
        except:
            print(sys.exc_info())
            user_state, output = user_state, "Gambar tidak bisa dibaca \nCoba lagi dengan gambar yang lebih baik"

        return user_state, [
            TextSendMessage(text=output),
            TextSendMessage(
                text='jika ada kesalahan bisa diubah kok kak :)')
        ]
