# from flask import jsonify

from BaseMongo import BaseMongo
from datetime import datetime,date,time
import pprint

class Event(BaseMongo):
    def __init__(self, line_id, _about, _urgency, dd, mm, yy, hh, _mm, _fullfiled):
        super().__init__()
        self.lineid = line_id
        self.about = _about
        self.urgency = _urgency
        d = date(int(yy), int(mm), int(dd))
        t = time(int(hh), int(_mm))
        self.datetime = datetime.combine(d, t)
        self.fullfiled = _fullfiled

    # def setLineId(self, line_id):
    #     self.lineid = line_id

    # def setAbout(self, _about):
    #     self.about = _about

    def setUrgency(self, _urgency):
        self.urgency = _urgency

    def setDatetime(self, dd, mm, yy, hh, _mm):
        d = date(yy, mm, dd)
        t = time(hh, _mm)
        self.datetime = datetime.combine(d, t)

    def setFulfilled(self, _fullfiled):
        self.fullfiled = _fullfiled

    def getLineId(self):
        return self.lineid

    def getAbout(self):
        return self.about

    def getUrgency(self):
        return self.urgency

    def getDatetime(self):
        return self.datetime

    def getlineId(self):
        return self.lineid

    def create(self):
        if self.searchOne(self.makeEvent()):
            return 0
        event_id = self.db.events.insert_one(self.makeEvent()).inserted_id
        return event_id

    def update(self):
        event = self.searchOne({ "lineid" : self.lineid, "about" : self.about })
        self.db.events.update(
            {'_id': event['_id']},
            { "$set": { "urgency" : self.urgency,"datetime" : self.datetime,"fullfiled" : self.fullfiled}},
            upsert=False, multi=True)
        # TODO: err handle
        return event

    def search(self, query):
        events =  self.db.events.find(query)
        return events

    def searchOne(self, query):
        event =  self.db.events.find_one(query)
        return event

    def removeSelf(self):
        self.db.events.delete_one(self.makeEvent())

    def removeQuery(self, query):
        self.db.events.delete_many(query)

    def set(self, event):
        self.lineid = event['lineid']
        self.about = event['about']
        self.urgency = event['urgency']
        self.datetime = event['datetime']
        self.fullfiled = event['fullfiled']

    def makeEvent(self):
        event = {"lineid": self.lineid,
                  "about" : self.about,
                  "urgency" : self.urgency,
                  "datetime" : self.datetime,
                  "fullfiled" : self.fullfiled}
        return event

# ev1 = Event("2783718371823718","ujian kanji",10,31,3,1997,12,30,-1)
# ev1.create()
# # ev1.removeSelf()
# # event = ev1.searchOne({"lineid":"2783718371823718"})
# # pprint.pprint(event)
# ev1.setFulfilled(0)
# ev1.setUrgency(3)
# ev1.update()
