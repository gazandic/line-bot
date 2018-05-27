from datetime import datetime

from bawel.constant.StateConstant import STATE_NOTHING
from bawel.model.BaseMongo import BaseMongo

class User(BaseMongo):
    def __init__(self, line_id="0", _name="", _location="", _state=STATE_NOTHING):
        super().__init__()
        self.lineid = line_id
        self.name = _name
        self.location = _location
        self.state = _state
        self.jointime = datetime.now()

    def setLineId(self, line_id):
        self.lineid = line_id

    def setName(self, _name):
        self.name = _name

    def setState(self, _state):
        self.state = _state

    def setLocation(self, _location):
        self.location = _location

    def getLineId(self):
        return self.lineid

    def getName(self):
        return self.getName

    def getState(self):
        return self.state

    def getLocation(self):
        return self.location

    def getJointime(self):
        return self.jointime

    def create(self):
        if self.searchOne(self.makeUser()):
            return 0
        user_id = self.db.users.insert_one(self.makeUser()).inserted_id
        return user_id

    def update(self):
        user = self.searchOne({ "lineid" : self.lineid})
        self.db.users.update(
            {'_id': user['_id']},
            { "$set": { "name" : self.name,"location": self.location,"state" : self.state}},
            upsert=False, multi=True)
        return 0

    def search(self, query):
        users =  self.db.users.find(query)
        return users

    def searchOne(self, query):
        user =  self.db.users.find_one(query)
        return user

    def set(self, user):
        self.lineid = user['lineid']
        self.name = user['name']
        self.location = user['location']
        self.state = user['state']

    def removeSelf(self):
        self.db.users.delete_one(self.makeUser())

    def removeQuery(self, query):
        self.db.users.delete_many(query)

    def makeUser(self):
        user = {"lineid": self.lineid,
                "name" : self.name,
                "location" : self.location,
                "state" : self.state}
        return user

