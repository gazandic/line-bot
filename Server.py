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
from bawel.util import searchLoc
from bawel.util.PengeluaranDetector import PengeluaranDetector
from bawel.util.Reminder import Reminder
from bawel.util.RequestParser import RequestParser
from bawel.util.TextProcessor import TextProcessor
from bawel.util.JsonToQuery import JsonToQuery
from bawel.util.CheckMoney import CheckMoney

from bawel.constant.StateConstant import (
    ACTION_MAPPER,
    STATE_ADD_JADWAL,
    STATE_DELETE_JADWAL,
    STATE_ADD_PENGELUARAN,
    STATE_SHOW_PENGELUARAN,
    STATE_DELETE_PENGELUARAN,
    STATE_IMAGE_ADD_PENGELUARAN,
    REQUEST_STATE
)

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
jadwaler = sched.scheduler(time.time, time.sleep)
reminder = Reminder(jadwaler, line_bot_api)
randomPrivate = [181, 183, 187, 188]
state = {}


static_tmp_path = os.path.join(os.path.dirname(__file__), 'bawel', 'static', 'tmp')
app = Flask(__name__, static_url_path='', static_folder='bawel/static')


# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise


def handle_action(raw_text, text, state):
    state, param = parser.parse(text, state)
    if state['state_id'] >= STATE_ADD_JADWAL and \
       state['state_id'] <= STATE_DELETE_JADWAL:
        param.append(reminder)
    if state['state_id'] == STATE_ADD_PENGELUARAN:
        param.insert(3, state)
    elif state['state_id'] == STATE_DELETE_PENGELUARAN:
        param.insert(1, state)
    elif state['state_id'] == STATE_SHOW_PENGELUARAN:
        param.insert(0, state)
    else:
        param.append(state)

    if state['state_id'] == STATE_ADD_JADWAL:
        ent = nlptext.checkEntity(raw_text)
        print(ent)
        loc_name = [entity["fragment"] for entity in ent if entity['entity'] == "LOCATION"]
        loc_coord = searchLoc(loc_name)
        param.append(loc_coord)

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
        id = None
        if isinstance(event.source, SourceGroup):
            id = event.source.group_id
        elif isinstance(event.source, SourceRoom):
            id = event.source.room_id

        global state

        if id in state:
            user_state = state[id]
        else:
            user_state = { 'id': id }

        s = text.split(" ")
        if user_state.get('before_state'):
            if user_state['before_state'] == STATE_ADD_PENGELUARAN :
                cm = str(CheckMoney().processText(text))
                print(cm)
                if not cm == "None" :
                    user_state['state_id'] = STATE_IMAGE_ADD_PENGELUARAN
                    user_state, output = dispatch_action(ACTION_MAPPER[user_state['state_id']], *(cm, "", user_state))
                    state = {**state, id: user_state}
                    line_bot_api.reply_message(
                        event.reply_token, [
                            TextSendMessage(text=output)
                        ])
                return
        elif REQUEST_STATE.get(s[0]):
            try:
                user_state, output = handle_action(text, text, user_state)
                state = {**state, id: user_state}
                if type(output[0]) == TemplateSendMessage:
                    line_bot_api.reply_message(event.reply_token, output)
                else :
                    line_bot_api.reply_message(
                        event.reply_token, TextMessage(text=output))
            except:
                line_bot_api.reply_message(
                    event.reply_token, TextMessage(text="ketik 'si bawel tolong' kak"))

        elif text == '@bye':
            line_bot_api.reply_message(
                event.reply_token, TextMessage(text='Leaving group'))
            line_bot_api.leave_group(id)

        elif text == 'si bawel tolong':
            text = '/help'
            print(user_state)
            user_state, output = handle_action(text, text, user_state)
            state = {**state, id: user_state}
            line_bot_api.reply_message(
                event.reply_token, TextMessage(text=output))
        elif not 'si bawel' in text.lower():
            pass

        else:
            restext = "Tolong ketik 'si bawel tolong' ya kakak kakak"

            try:
                nlptext.processText(event.message.text)
                jtq = JsonToQuery(nlptext.getJsonToSent())
                restext = jtq.parseJSON()
                if not jtq.json.get('error'):
                    print(user_state)
                    user_state, output = handle_action(text, restext, user_state)
                    state = {**state, id: user_state}
                else:
                    output = restext
                if type(output[0]) == TemplateSendMessage :
                    line_bot_api.reply_message(event.reply_token, output)
                else :
                    line_bot_api.reply_message(
                        event.reply_token, TextMessage(text=output))

            except:
                print(sys.exc_info())
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(text=restext),
                        StickerSendMessage(
                            package_id=3,
                            sticker_id=random.choice(randomPrivate))
                    ])


@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=event.message.title, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )

# Image Message Type
@handler.add(MessageEvent, message=ImageMessage)
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
        id = None
        if isinstance(event.source, SourceGroup):
            id = event.source.group_id
        elif isinstance(event.source, SourceRoom):
            id = event.source.room_id

        global state
        if id in state:
            user_state = state[id]
        else:
            user_state = { 'id': id }

        if user_state.get('before_state'):
            ext = 'jpg'
            message_content = \
                line_bot_api.get_message_content(event.message.id)
            with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
                for chunk in message_content.iter_content():
                    tf.write(chunk)
                tempfile_path = tf.name

            dist_path = tempfile_path + '.' + ext
            dist_name = os.path.basename(dist_path)
            os.rename(tempfile_path, dist_path)
            try :
                PD = PengeluaranDetector(str(dist_path))
                total_amount = PD.checkForTotal()
                if not total_amount:
                    user_state, output = user_state, "Gambar tidak terbaca \nCoba lagi dengan gambar yang lebih baik"
                    state = {**state, id: user_state}
                else:
                    user_state['state_id'] = STATE_IMAGE_ADD_PENGELUARAN
                    user_state, output = dispatch_action(ACTION_MAPPER[user_state['state_id']], *(total_amount, request.host_url + os.path.join('tmp', dist_name), user_state))
                    state = {**state, id: user_state}
            except:
                print(sys.exc_info())
                user_state, output = user_state, "Gambar tidak bisa dibaca \nCoba lagi dengan gambar yang lebih baik"
                state = {**state, id: user_state}
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=output)
                ])


# @handler.add(FollowEvent)
# def handle_follow(event):
#     line_bot_api.reply_message(
#         event.reply_token, TextSendMessage(text='Got follow event'))


# @handler.add(UnfollowEvent)
# def handle_unfollow():
#     app.logger.info("Got Unfollow event")


# @handler.add(JoinEvent)
# def handle_join(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text='Joined this ' + event.source.type))


# @handler.add(LeaveEvent)
# def handle_leave():
#     app.logger.info("Got leave event")


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'ping':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='pong'))


# @handler.add(BeaconEvent)
# def handle_beacon(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text='Got beacon event. hwid=' + event.beacon.hwid))


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    # create tmp dir for download content
    make_static_tmp_dir()
    jadwaler.run()

    app.run(debug=options.debug, port=options.port)
