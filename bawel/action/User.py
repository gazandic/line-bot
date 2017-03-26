from __future__ import unicode_literals

from bawel.action.Action import Action
from bawel.constant.UserConstant import *

class UserPromptName(Action):
    def __init__(self):
        super().__init__()

    def act(self, state):
        state = {**state, 'state_id': STATE_ASK_USERNAME}
        return (state, "Siapa nama bos?")

class UserGetName(Action):
    def __init__(self):
        super().__init__()

    def act(self, state, name):
        state = {**next_state, 'name': name}
        return (state, "Siap bos %s".format(name))

class UserPromptLoc(Action):
    def __init__(self):
        super().__init__()

    def act(self, state):
        name = state['name']
        state = {**state, 'state_id': STATE_ASK_USERLOCATION}
        return (state, "Bos %s ada di kota mana ?".format(name))

class UserGetLoc(Action):
    def __init__(self):
        super().__init__()

    def act(self, state, loc):
        state = {**next_state, 'loc': loc}
        return (state, "Siap bos %s".format(name))
