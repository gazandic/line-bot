from typing import Dict

from bawel.model.BaseMongo import BaseMongo

import json


class State(BaseMongo):
    def __init__(self, uid: str = "", state: Dict = {}):
        super().__init__()
        self.uid = uid
        self.state = state

    def create(self):
        payload = self.make_state()
        if self.search_one(payload):
            return 0
        id = self.db.state.insert_one(payload).inserted_id
        return payload if id is not None else None

    def search(self, query):
        states = self.db.state.find(query)
        return states

    def search_one(self, query):
        expense = self.db.state.find_one(query)
        return expense

    def remove_self(self):
        self.db.state.delete_one(self.make_state())

    def remove_query(self, query):
        self.db.state.delete_many(query)

    def update(self):
        state = self.search_one({"uid": self.uid})
        self.db.expenses.update(
            {
                '_id': state['_id']
            },
            {
                "$set": {
                    "uid": self.uid,
                    "state": json.dumps(self.state)
                }
            },
            upsert=False, multi=True)
        return 0

    def make_state(self):
        state = {
            "uid": self.uid,
            "state": json.dumps(self.state)
        }
        return state

# ev1 = State("123",{'mata':[123, 456], 'sapi': 'sei'})
# ev1.create()
