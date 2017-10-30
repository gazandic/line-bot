from __future__ import unicode_literals

import os
import random
import sched
import sys
import tempfile
import time
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, LocationMessage, ImageMessage, SourceGroup, TextSendMessage, SourceUser, \
    SourceRoom, JoinEvent, PostbackEvent, TextMessage, LocationSendMessage, StickerSendMessage

from bawel.action.ActionUtils import dispatch_action, handle_action
from bawel.client.GoogleMaps import GoogleMaps
from bawel.client.Line import Line
from bawel.constant.StateConstant import STATE_IMAGE_ADD_PENGELUARAN, ACTION_MAPPER, TemplateSendMessage, REQUEST_STATE
from bawel.nlp.TextProcessor import TextProcessor
from bawel.util.Cycling import Cycling
from bawel.util.FileUtil import make_static_tmp_dir, static_tmp_path
from bawel.util.PengeluaranDetector import PengeluaranDetector
from bawel.util.Reminder import Reminder
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

token_kata = os.getenv('TOKEN_KATA', '')
token_google = os.getenv('GOOGLE_MAP_TOKEN', '')

gmaps = GoogleMaps(token_google)
nlptext = TextProcessor(token_kata)
jadwaler = sched.scheduler(time.time, time.sleep)
lineClient = Line(channel_secret, channel_access_token)
reminder = Reminder(jadwaler, lineClient)

cycling = Cycling(reminder)
cycling.process()

# Centralized state system
# TODO: utilize redis state mgmt
state = {}

app = Flask(__name__, static_url_path='', static_folder='bawel/static')


@app.route("/line", methods=['POST'])
def callbackLine():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        lineClient.handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# @app.route("/telegram", methods=['POST'])
# def callbackTelegram():
#     # retrieve the message in JSON and then transform it to Telegram object
#     update = telegram.Update.de_json(request.get_json(force=True))
#
#     chat_id = update.message.chat.id
#
#     # Telegram understands UTF-8, so encode text for unicode compatibility
#     text = update.message.text.encode('utf-8')
#
#     # repeat the same message back (echo)
#     bot.sendMessage(chat_id=chat_id, text=text)
#
#     return 'OK'

@lineClient.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    lineClient.api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=event.message.title, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )


def processImage(ID, message_content):
    global state
    if ID in state:
        user_state = state[ID]
    else:
        user_state = {'id': ID}

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
        PD = PengeluaranDetector(str(dist_path))
        total_amount = PD.checkForTotal()
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

    state = {**state, ID: user_state}
    return user_state, output


# Image Message Type
@lineClient.add(MessageEvent, message=ImageMessage)
def handle_content_message(event):
    if isinstance(event.source, SourceUser):
        profile = lineClient.api.get_profile(event.source.user_id)
        lineClient.api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text='Maaf, kak ' + profile.display_name + ' bot ini fokus pada asisten grup, undang bawel ke grup kak'
                ),
                StickerSendMessage(
                    package_id=3,
                    sticker_id=random.choice(randomPrivate)
                )
            ]
        )
    else:
        id = None
        if isinstance(event.source, SourceGroup):
            id = 'LINE' + event.source.group_id
        elif isinstance(event.source, SourceRoom):
            id = 'LINE' + event.source.room_id

        message_content = lineClient.api.get_message_content(event.message.id)
        user_state, output = processImage(id, message_content)

        if output is not None:
            lineClient.api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=output),
                    TextSendMessage(text='jika ada kesalahan bisa diubah kok kak :)')
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
        TextSendMessage(text='Hai, si bawel telah join ' + event.source.type + \
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

    global state

    if id in state:
        user_state = state[id]
    else:
        user_state = {'id': id}

    s = text.split(" ")
    if REQUEST_STATE.get(s[0]):
        try:
            user_state, output = handle_action(text, text, user_state)
            state = {**state, id: user_state}
            if type(output[0]) == TemplateSendMessage:
                lineClient.api.reply_message(event.reply_token, output)
            else:
                lineClient.api.reply_message(event.reply_token, TextMessage(text=output))
        except:
            lineClient.api.reply_message(event.reply_token, TextMessage(text="ketik 'si bawel tolong' kak"))
            # if event.postback.data == 'ping':
            #     lineClient.api.reply_message(
            #         event.reply_token, TextSendMessage(text='pong'))


# @lineClient.add(BeaconEvent)
# def handle_beacon(event):
#     lineClient.api.reply_message(
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
