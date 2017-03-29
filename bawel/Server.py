from __future__ import unicode_literals

import errno
import os
import pprint
import random
import sched
import sys
import tempfile
import time

from argparse import ArgumentParser
from flask import Flask, request, abort

import bawel.util.Sticker

from bawel.action.Action import dispatch_action

from bawel.util.PengeluaranDetector import PengeluaranDetector
from bawel.util.Reminder import Reminder
from bawel.util.RequestParser import RequestParser
from bawel.util.TextProcessor import TextProcessor
from bawel.util.JsonToQuery import JsonToQuery

from bawel.constant.StateConstant import (
    ACTION_MAPPER, STATE_ADD_JADWAL, STATE_DELETE_JADWAL)

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, URITemplateAction, PostbackTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

handler = WebhookHandler(channel_secret)
line_bot_api = LineBotApi(channel_access_token)
nlptext = TextProcessor()
parser = RequestParser()
reminder = Reminder(sched.scheduler(time.time, time.sleep))
randomPrivate = [181, 183, 187, 188]
state = {}


static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
app = Flask(__name__, static_url_path='', static_folder='static')

# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise


def handle_action(text, state):
    state, param = parser.parse(text, state)
    param.append(state)

    if state['state_id'] >= STATE_ADD_JADWAL and \
       state['state_id'] <= STATE_DELETE_JADWAL:
        param.append(reminder)

    return dispatch_action(ACTION_MAPPER[state['state_id']], *param)
    # print(output)


@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    if isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text='Maaf, kak ' + profile.display_name + ' bot ini fokus pada asisten grup, undang bawel ke grup kak'
                ),
                StickerSendMessage(
                    package_id=3,
                    sticker_id=random.choice(randomPrivate))
            ]
        )
    else:
        if text == '@bye':
            if isinstance(event.source, SourceGroup):
                line_bot_api.reply_message(
                    event.reply_token, TextMessage(text='Leaving group'))
                line_bot_api.leave_group(event.source.group_id)
            elif isinstance(event.source, SourceRoom):
                line_bot_api.reply_message(
                    event.reply_token, TextMessage(text='Leaving group'))
                line_bot_api.leave_room(event.source.room_id)
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextMessage(text="Bot can't leave from 1:1 chat"))
        elif text == 'si bawel tolong':
            line_bot_api.reply_message(
                event.reply_token, [TextSendMessage(text='lagi dibuat hehe'),
                StickerSendMessage(
                    package_id=3,
                    sticker_id=random.choice(randomPrivate))])
        elif not 'si bawel' in text:
            pass
        else:
            try:
                nlptext.processText(event.message.text)
                line_bot_api.reply_message(
                    event.reply_token, TextMessage(text=event.message.text))
                jtq = JsonToQuery(test.getJsonToSent())
                line_bot_api.reply_message(
                    event.reply_token, TextMessage(text=str(jtq)))
                restext = jtq.parseJSON()
                line_bot_api.reply_message(
                    event.reply_token, TextMessage(text=restext))
                global state
                state = {**state, 'id': event.source.group_id}
                state, output = handle_action(restext, state)
                line_bot_api.reply_message(
                    event.reply_token, TextMessage(text=output))

            except:
                e = sys.exc_info()[0]
                print(e)
                restext = "tolong ketik 'si bawel tolong' ya kakak kakak"
                line_bot_api.reply_message(
                    event.reply_token, [TextSendMessage(text=restext),
                    StickerSendMessage(
                        package_id=3,
                        sticker_id=random.choice(randomPrivate))])


# @handler.add(MessageEvent, message=LocationMessage)
# def handle_location_message(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         LocationSendMessage(
#             title=event.message.title, address=event.message.address,
#             latitude=event.message.latitude, longitude=event.message.longitude
#         )
#     )


# @handler.add(MessageEvent, message=StickerMessage)
# def handle_sticker_message(event):
#     print("package_id:"+event.message.package_id)
#     print("sticker_id:"+event.message.sticker_id)
#     line_bot_api.reply_message(
#         event.reply_token,
#         StickerSendMessage(
#             package_id=event.message.package_id,
#             sticker_id=event.message.sticker_id)
#     )


# Other Message Type
@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    if isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text='Maaf, kak ' + profile.display_name + ' bot ini fokus pada asisten grup, undang bawel ke grup kak'
                ),
                StickerSendMessage(
                    package_id=3,
                    sticker_id=random.choice(randomPrivate))
            ]
        )
    else:
        if isinstance(event.message, ImageMessage):
            ext = 'jpg'
        elif isinstance(event.message, VideoMessage):
            ext = 'mp4'
        elif isinstance(event.message, AudioMessage):
            ext = 'm4a'
        else:
            return

        message_content = line_bot_api.get_message_content(event.message.id)
        with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
            tempfile_path = tf.name

        dist_path = tempfile_path + '.' + ext
        dist_name = os.path.basename(dist_path)
        os.rename(tempfile_path, dist_path)
        PD = PengeluaranDetector(str(dist_path))
        rptotal = str(PD.checkForTotal())
        if not rptotal:
            rptotal = 'Save content.'
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=rptotal),
                TextSendMessage(text=request.host_url + os.path.join('tmp', dist_name))
            ])


@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='Got follow event'))


@handler.add(UnfollowEvent)
def handle_unfollow():
    app.logger.info("Got Unfollow event")


@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Joined this ' + event.source.type))


@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("Got leave event")


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'ping':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='pong'))


@handler.add(BeaconEvent)
def handle_beacon(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Got beacon event. hwid=' + event.beacon.hwid))


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    # create tmp dir for download content
    make_static_tmp_dir()

    app.run(debug=options.debug, port=options.port)
