from __future__ import unicode_literals

import json
import logging

from bawel.constant.StateConstant import *
from bawel.model.User import User


class RequestParser:

    @staticmethod
    def parse(text, state):
        try:
            line_id = state['uid']

            us = User()
            user = us.searchOne({"lineid": line_id})

            if not user:
                us.setLineId({"lineid": line_id})
                us.create()
            else:
                us.set(user)

            state, param = RequestParser.choose_menu(text, state)

            return state, param

        except KeyError:
            logging.error(json.dumps(state))
            return {**state, 'state_id': STATE_UNKNOWN}, [""]

    @staticmethod
    def choose_menu(text, state):
        cmd = text.split()
        param = cmd[1:]
        cmd = cmd[0]

        try:
            return {**state, 'state_id': REQUEST_STATE[cmd]}, param
        except IndexError:
            return {**state, 'state_id': STATE_UNKNOWN}, param
