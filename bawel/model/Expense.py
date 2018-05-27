# from flask import jsonify

from datetime import datetime, date, time

from bawel.model.BaseMongo import BaseMongo


class Expense(BaseMongo):
    def __init__(self, line_id="", _about="", _name="", _peoplename="", _total=0):
        super().__init__()
        self.lineid = line_id
        self.about = _about
        self.name = _name
        self.peoplename = _peoplename
        self.total = float(_total)

    def setName(self, _name):
        self.name = _name

    def setPathnota(self, _total):
        self.total = _total

    def getLineId(self):
        return self.lineid

    def getAbout(self):
        return self.about

    def getName(self):
        return self.name

    # def getDatetime(self):
    #     return self.datetime

    def getlineId(self):
        return self.lineid

    def create(self):
        if self.searchOne(self.makeExpense()):
            return 0
        expense_id = self.db.expenses.insert_one(
            self.makeExpense()).inserted_id
        return expense_id

    def update(self):
        expense = self.searchOne({"lineid": self.lineid, "about": self.about})
        self.db.expenses.update(
            {'_id': expense['_id']},
            {"$set": {"peoplename": self.peoplename,
                      "name": self.name, "total": self.total}},
            upsert=False, multi=True)
        return 0

    def updatePathNota(self, path):
        expense = self.searchOne(
            {"lineid": self.lineid, "about": self.about, "name": self.name})
        self.db.expenses.update(
            {'_id': expense['_id']},
            {"$set": {"peoplename": self.peoplename,
                      "total": self.total, "pathnota": path}},
            upsert=False, multi=True)
        return 0

    def search(self, query):
        expenses = self.db.expenses.find(query)
        return expenses

    def searchOne(self, query):
        expense = self.db.expenses.find_one(query)
        return expense

    def removeSelf(self):
        self.db.expenses.delete_one(self.makeExpense())

    def removeQuery(self, query):
        self.db.expenses.delete_many(query)

    def set(self, expense):
        self.lineid = expense['lineid']
        self.about = expense['about']
        self.name = expense['name']
        self.peoplename = expense['peoplename']
        self.total = expense['total']

    def makeExpense(self):
        expense = {"lineid": self.lineid,
                   "about": self.about,
                   "name": self.name,
                   "peoplename": self.peoplename,
                   "total": self.total}
        return expense

    def aggregate(self, pipeline):
        return self.db.expenses.aggregate(pipeline
                                          )
