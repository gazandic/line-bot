import os
import random
import sys
from typing import Dict, List, Union, Optional, Tuple

from linebot.models import TextSendMessage, TextMessage, TemplateSendMessage, StickerSendMessage

from bawel.action.ActionUtils import handle_action, dispatch_action
from bawel.constant.ActionMapper import ACTION_MAPPER
from bawel.constant.StateConstant import STATE_ADD_PENGELUARAN, STATE_IMAGE_ADD_PENGELUARAN, REQUEST_STATE
from bawel.processor.TextProcessor import TextProcessor
from bawel.util.CheckMoney import CheckMoney
from bawel.util.JsonToQuery import JsonToQuery
from bawel.util.Sticker import randomPrivate


class Image:
    def __init__(self, location: str, size: str):
        self.location = location
        self.size = size


ResponseList = Optional[List[Union[TextMessage, TextSendMessage]]]


token_kata = os.getenv('TOKEN_KATA', '')
token_google = os.getenv('GOOGLE_MAP_TOKEN', '')

text_processor = TextProcessor(token_kata)


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
                    sticker_id=random.choice(randomPrivate))
            ]

    def handle_image(self, image: Image):
        pass
