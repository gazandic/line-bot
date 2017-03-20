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
