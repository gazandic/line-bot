import os
import sys

from linebot.models import MessageEvent, LocationMessage, ImageMessage, SourceGroup, TextSendMessage, SourceRoom, \
    JoinEvent, PostbackEvent, TextMessage, TemplateSendMessage, LocationSendMessage

from bawel.action.ActionUtils import handle_action
from bawel.client.Line import Line
from bawel.constant.StateConstant import REQUEST_STATE
from bawel.handler.core.ContentHandler import ContentHandler
from bawel.state.StateManager import StateManager

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


def extract_uid(event_source) -> str:
    if isinstance(event_source, SourceGroup):
        return 'LINE' + event_source.group_id
    elif isinstance(event_source, SourceRoom):
        return 'LINE' + event_source.room_id


@lineClient.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    lineClient.api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=event.message.title, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )


# Image Message Type
@lineClient.add(MessageEvent, message=ImageMessage)
def handle_content_message(event):
    uid = extract_uid(event.source)
    line_bot_api = lineClient.api

    user_state = StateManager.fetch(uid)

    message_content = lineClient.api.get_message_content(event.message.id)
    updated_state, responses = ContentHandler.handle_image(user_state.state, message_content)

    line_bot_api.reply_message(event.reply_token, responses)
    StateManager.update(uid, updated_state)

    if responses is not None:
        lineClient.api.reply_message(event.reply_token, responses)


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
        TextSendMessage(text=ContentHandler.handle_join())
    )


# @lineClient.add(LeaveEvent)
# def handle_leave():
#     app.logger.info("Got leave event")


@lineClient.add(PostbackEvent)
def handle_postback(event):
    text = event.postback.data
    uid = extract_uid(event.source)
    line_bot_api = lineClient.api

    user_state = StateManager.fetch(uid)

    s = text.split(" ")
    if REQUEST_STATE.get(s[0]):
        try:
            updated_state, output = handle_action(text, text, user_state)
            StateManager.update(uid, updated_state)
            if type(output[0]) == TemplateSendMessage:
                line_bot_api.reply_message(event.reply_token, output)
            else:
                line_bot_api.reply_message(
                    event.reply_token, TextMessage(text=output))
        except:
            line_bot_api.reply_message(event.reply_token, TextMessage(
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
    uid = extract_uid(event.source)

    user_state = StateManager.fetch(uid)
    updated_state, responses = ContentHandler.handle_text(user_state.state, text, None)

    line_bot_api.reply_message(event.reply_token, responses)
    StateManager.update(uid, updated_state)
