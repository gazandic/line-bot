from __future__ import unicode_literals

from bawel.action.Action import Action
from bawel.constant.UserConstant import *

class UserPromptName(Action):
    def __init__(self):
        super().__init__()

    def act(self, state):
        print("Siapa nama bos ?")
        state = {**state, 'state': STATE_ASK_USERNAME}
        return state

class UserGetName(Action):
    def __init__(self):
        super().__init__()

    def act(self, state, name):
        state = {**state, 'state': STATE_NOTHING, 'name': name}
        return state

class UserPromptLoc(Action):
    def __init__(self):
        super().__init__()

    def act(self, state):
        name = state['name']
        print("Bos %s ada di kota mana ?".format(name))
        state = {**state, 'state': STATE_ASK_USERLOCATION}
        return state

class UserGetLoc(Action):
    def __init__(self):
        super().__init__()

    def act(self, state, loc):
        state = {**state, 'state': STATE_NOTHING, 'loc': loc}
        return state
