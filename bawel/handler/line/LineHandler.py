import os
import random
import sys
from typing import Dict, Tuple

from linebot.models import MessageEvent, LocationMessage, ImageMessage, SourceGroup, TextSendMessage, SourceUser, \
    SourceRoom, JoinEvent, PostbackEvent, TextMessage, TemplateSendMessage, LocationSendMessage, StickerSendMessage

from bawel.action.ActionUtils import handle_action
from bawel.client.Line import Line
from bawel.constant.StateConstant import REQUEST_STATE
from bawel.handler.core.ContentHandler import ContentHandler
from bawel.state.StateManager import StateManager
from bawel.util.Sticker import randomPrivate

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', '')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

lineClient = Line(channel_secret, channel_access_token)


def handle(body, signature):
    lineClient.handler.handle(body, signature)


@lineClient.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    lineClient.api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=event.message.title, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )


def process_image(ID: str, message_content: str) -> Tuple[Dict[str, str], str]:
    global state
    # if ID in state:
    #     user_state = state[ID]
    # else:
    #     user_state = {'id': ID}

    # if not user_state.get('before_state'):
    #     return user_state, None

    # ext = 'jpg'
    # with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
    #     for chunk in message_content.iter_content():
    #         tf.write(chunk)
    #     tempfile_path = tf.name

    # dist_path = tempfile_path + '.' + ext
    # dist_name = os.path.basename(dist_path)
    # os.rename(tempfile_path, dist_path)
    # try:
    #     PD = ExpenseDetector(str(dist_path))
    #     total_amount = PD.check_for_total()
    #     if not total_amount:
    #         user_state, output = user_state, "Gambar tidak terbaca \nCoba lagi dengan gambar yang lebih baik"
    #     else:
    #         user_state['state_id'] = STATE_IMAGE_ADD_PENGELUARAN
    #         user_state, output = dispatch_action(ACTION_MAPPER[user_state['state_id']],
    #                                             *(total_amount,
    #                                             request.host_url + os.path.join('tmp', dist_name),
    #                                             user_state))
    # except:
    #     print(sys.exc_info())
    #     user_state, output = user_state, "Gambar tidak bisa dibaca \nCoba lagi dengan gambar yang lebih baik"

    # state = {**state, ID: user_state}
    # return user_state, output
    return state, ''


# Image Message Type
@lineClient.add(MessageEvent, message=ImageMessage)
def handle_content_message(event):
    id = None
    if isinstance(event.source, SourceGroup):
        id = 'LINE' + event.source.group_id
    elif isinstance(event.source, SourceRoom):
        id = 'LINE' + event.source.room_id

    message_content = lineClient.api.get_message_content(event.message.id)
    user_state, output = process_image(id, message_content)

    if output is not None:
        lineClient.api.reply_message(
            event.reply_token, [
                TextSendMessage(text=output),
                TextSendMessage(
                    text='jika ada kesalahan bisa diubah kok kak :)')
            ]
        )


# @lineClient.add(FollowEvent)
# def handle_follow(event):
#     lineClient.api.reply_message(
#         event.reply_token, TextSendMessage(text='Got follow event'))


# @lineClient.add(UnfollowEvent)
# def handle_unfollow():
#     app.logger.info("Got Unfollow event")


@lineClient.add(JoinEvent)
def handle_join(event):
    lineClient.api.reply_message(
        event.reply_token,
        TextSendMessage(text='Hai, si bawel telah join ' + event.source.type +
                             ' ini. Mohon bantuannya, ketik "si bawel tolong" atau "/help" ya kak'))


# @lineClient.add(LeaveEvent)
# def handle_leave():
#     app.logger.info("Got leave event")


@lineClient.add(PostbackEvent)
def handle_postback(event):
    text = event.postback.data

    id = None
    if isinstance(event.source, SourceGroup):
        id = event.source.group_id
    elif isinstance(event.source, SourceRoom):
        id = event.source.room_id

    user_state = StateManager.fetch(id)

    s = text.split(" ")
    if REQUEST_STATE.get(s[0]):
        try:
            user_state, output = handle_action(text, text, user_state)
            StateManager.update(id, user_state)
            if type(output[0]) == TemplateSendMessage:
                lineClient.api.reply_message(event.reply_token, output)
            else:
                lineClient.api.reply_message(
                    event.reply_token, TextMessage(text=output))
        except:
            lineClient.api.reply_message(event.reply_token, TextMessage(
                text="ketik 'si bawel tolong' kak"))


# @lineClient.add(BeaconEvent)
# def handle_beacon(event):
#     lineClient.api.reply_message(
#         event.reply_token,
#         TextSendMessage(text='Got beacon event. hwid=' + event.beacon.hwid))

@lineClient.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text

    line_bot_api = lineClient.api

    uid = None
    if isinstance(event.source, SourceGroup):
        uid = event.source.group_id
    elif isinstance(event.source, SourceRoom):
        uid = event.source.room_id

    user_state = StateManager.fetch(uid)
    updated_state, responses = ContentHandler.handle_text(user_state.state, text, None)

    line_bot_api.reply_message(event.reply_token, responses)
    StateManager.update(uid, updated_state)
