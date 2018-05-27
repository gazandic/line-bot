from __future__ import unicode_literals

from bawel.constant.StateConstant import *
from bawel.model.User import User


class RequestParser:

    @staticmethod
    def parse(text, state):
        line_id = state['id']
        us = User()
        user = us.searchOne({"lineid": line_id})

        if not user:
            us.setLineId({"lineid": line_id})
            us.create()
        else:
            us.set(user)

        state, param = RequestParser.choose_menu(text, state)

        return state, param

    @staticmethod
    def choose_menu(text, state):
        cmd = text.split()
        param = cmd[1:]
        cmd = cmd[0]

        try:
            return {**state, 'state_id': REQUEST_STATE[cmd]}, param
        except IndexError:
            return {**state, 'state_id': STATE_UNKNOWN}, param
