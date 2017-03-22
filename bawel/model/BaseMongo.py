# from flask import jsonify
from pymongo import MongoClient

class BaseMongo:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.linebot
