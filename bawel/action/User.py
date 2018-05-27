from __future__ import unicode_literals

from bawel.action.Action import Action
from bawel.constant.StateConstant import *

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
        state = {**state.next_state, 'loc': loc, 'next_param': state.next_param}
        return (state, "Siap bos %s".format(name))
