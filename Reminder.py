<<<<<<< HEAD
import os
import sys
import time
import threading
# from schedule import Scheduler as schedule
import schedule

from linebot import (
    LineBotApi, WebhookHandler
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

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

def job():
    line_bot_api.push_message("U39166bd6890a58b174c92aed76983241", TextMessage(text="Morning honey :))) Howdy?"))


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


schedule.every(10).seconds.do(run_threaded, job)
run_continuously()
=======
# from flask import jsonify
from ImageProcessor import ImageProcessor
from validate_email import validate_email
from pymongo import MongoClient
from datetime import datetime,date,time
import pprint

client = MongoClient('localhost', 27017)
db = client.linebot

d = date(2017, 3, 14)
t = time(12, 30)
event = {"lineid":"2783718371823718",
          "about" : "ujian kanji",
          "urgency" : 10,
          "datetime" : datetime.combine(d, t),
          "fullfiled" : -1}
events = db.events
eventone = events.find_one()

pprint.pprint(eventone)
print (eventone.data.lineid)
# event_id = events.insert_one(event).inserted_id

# print (jsonify(event))
# print (event_id)

# app = Flask(__name__)
#
# pathImage = "/home/gazandic/linebot/line-bot/";
#
# @app.route("/email/<string:url>",methods=['GET'])
# def get_email(url):
#     if len(url) == 0:
#         abort(404)
#     ip = ImageProcessor()
#     s = ip.process_image(pathImage+url)
#     is_valid = validate_email(s)
#     if is_valid :
#         return jsonify({'result':s})
#     else :
#         return jsonify({'result':"fail"})
#
# @app.route("/",methods=['GET'])
# def get_home():
#     s = "random"
#     print(s)
#     return jsonify({"result":s})
#
#
# @app.route("/create",methods=['GET'])
# def get_home():
#     return jsonify(event)
#
#
# @app.route("/telephone/<string:url>",methods=['GET'])
# def get_telephone(url):
#     if len(url) == 0:
#         abort(404)
#     ip = ImageProcessor()
#     s = ip.process_image(pathImage+url)
#     print(s)
#     return jsonify({"result":s})
#
# if __name__ == "__main__":
#
#     app.run()
>>>>>>> master
