from __future__ import unicode_literals

from bawel.constant.StateConstant import *
from bawel.model.User import User


class RequestParser:
    def parse(self, text, state):
        lineid = state['id']
        us = User()
        user = us.searchOne({"lineid": lineid})

        if not user:
            us.setLineId({"lineid": lineid})
            us.create()
        else:
            us.set(user)

        state, param = self.chooseMenu(text, state)

        return (state, param)

    def chooseMenu(self, text, state):
        cmd = text.split()
        param = cmd[1:]
        cmd = cmd[0]

        try:
            return {**state, 'state_id': REQUEST_STATE[cmd]}, param
        except IndexError:
            return {**state, 'state_id': STATE_UNKNOWN}, param
