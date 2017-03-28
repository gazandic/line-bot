# from flask import jsonify

from bawel.model.BaseMongo import BaseMongo
from datetime import datetime,date,time
import pprint

class Habit(BaseMongo):
    def __init__(self, line_id, _about, _frequency, hh, mm, _fullfiled):
        super().__init__()
        self.lineid = line_id
        self.about = _about
        self.frequency = _frequency
        self.time = time(hh, mm)
        self.fullfiled = _fullfiled
    # def setLineId(self, line_id):
    #     self.lineid = line_id

    # def setAbout(self, _about):
    #     self.about = _about

    def setFrequency(self, _frequency):
        self.frequency = _frequency

    def setTime(self, hh, mm):
        self.time  = time(hh, mm)

    def setFulfilled(self, _fullfiled):
        self.fullfiled = _fullfiled

    def getLineId(self):
        return self.lineid

    def getAbout(self):
        return self.about

    def getFrequency(self):
        return self.frequency

    def getTime(self):
        return self.time

    def getFullfiled(self):
        return self.fullfiled

    def create(self):
        if self.searchOne(self.makeHabit()):
            return 0
        event_id = self.db.habits.insert_one(self.makeHabit()).inserted_id
        return event_id

    def update(self):
        habit = self.searchOne({ "lineid" : self.lineid, "about" : self.about })
        self.db.habits.update(
            {'_id': habit['_id']},
            { "$set": { "frequency" : self.frequency,"time" : self.time}},
            upsert=False, multi=True)
        return 0

    def search(self, query):
        habits =  self.db.habits.find(query)
        return habits

    def searchOne(self, query):
        habit =  self.db.habits.find_one(query)
        return habit

    def removeSelf(self):
        self.db.habits.delete_one(self.makeHabit())

    def removeQuery(self, query):
        self.db.habits.delete_many(query)

    def makeHabit(self):
        habit = { "lineid": self.lineid,
                  "about" : self.about,
                  "frequency" : self.frequency,
                  "time" : self.time,
                  "fullfiled" : self.fullfiled }
        return habit

# ev1 = Habit("2783718371823718","shalat dhuhur",0,12,30)
# ev1.create()
# # ev1.removeSelf()
# # event = ev1.searchOne({"lineid":"2783718371823718"})
# # pprint.pprint(event)
# ev1.setFrequency(12)
# ev1.update()
