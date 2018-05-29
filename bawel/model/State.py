import json
from typing import Dict

from bawel.model.BaseMongo import BaseMongo


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
        return list(map(self.parse_state, states))

    def search_one(self, query):
        state = self.db.state.find_one(query)
        if state is None: 
            return State(query["uid"], {"uid": query["uid"], "before_state": {}})
            
        return self.parse_state(state)

    def remove_self(self):
        self.db.state.delete_one(self.make_state())

    def remove_query(self, query):
        self.db.state.delete_many(query)

    def set_state(self, state):
        self.state = {**self.state, **state}

    def parse_state(self, state_row):
        return State(state_row['uid'], json.loads(state_row['state']))

    def update(self):
        state = self.search_one({"uid": self.uid})
        self.db.expenses.update(
            {
                '_id': state.uid
            },
            {
                "$set": {
                    "uid": state.uid,
                    "state": json.dumps(state.state)
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
