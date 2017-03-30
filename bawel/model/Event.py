# from flask import jsonify

from datetime import datetime,date,time

from bawel.model.BaseMongo import BaseMongo

class Event(BaseMongo):
    def __init__(self, line_id="0", _about="", dd="1", mm="1", yy="2000", hh="0", _mm="0", _loc=None, _fullfiled=0):
        super().__init__()
        self.lineid = line_id
        self.about = _about
        self.loc = _loc
        d = date(int(yy), int(mm), int(dd))
        t = time(int(hh), int(_mm))
        self.datetime = datetime.combine(d, t)
        self.fullfiled = _fullfiled

    # def setLineId(self, line_id):
    #     self.lineid = line_id

    # def setAbout(self, _about):
    #     self.about = _about

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
            { "$set": { 
                "datetime" : self.datetime,
                "fullfiled" : self.fullfiled
            }},
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
        self.datetime = event['datetime']
        self.fullfiled = event['fullfiled']

    def makeEvent(self):
        event = {"lineid": self.lineid,
                  "about" : self.about,
                  "location": self.loc,
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
