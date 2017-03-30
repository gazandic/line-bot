from __future__ import unicode_literals

from datetime import (
    datetime, date, time
)

from bawel.action.Action import dispatch_action
from bawel.constant.StateConstant import *
from bawel.model.User import User
from bawel.model.Event import Event
from bawel.model.Expense import Expense

class RequestParser:

    def parse(self, text, state):
        lineid = state['id']
        us = User()
        user = us.searchOne({"lineid":lineid})

        # TODO
        # if 'id' not in state:

        if not user:
            return us.create()
        us.set(user)

        state, param = self.chooseMenu(text, state)
        # if state['state_id'] == STATE_UNKNOWN:
        #     return (state, ())
        # print("halo bos, sekretaris bos "+bossName+ " kurang paham, coba ketik /help ya bos :)")

        # if 'name' not in state or not state['name']:
        #     state = {
        #         state_id: STATE_ASK_USERNAME,
        #         next_state: state,
        #         next_param: param
        #     }
        # elif 'loc' not in state or not state['loc']:
        #     state = {
        #         state_id: STATE_ASK_LOC,
        #         next_state: state
        #         next_param: param
        #     }
        # else:
        #     # TODO: hayo
        #     pass

        return (state, param)

    def chooseMenu(self, text, state):
        cmd = text.split()
        param = cmd[1:]
        cmd = cmd[0]

        try:
            return ({**state, 'state_id': REQUEST_STATE[cmd]}, param)
        except IndexError:
            return ({**state, 'state_id': STATE_UNKNOWN}, param)

# TEST SUITE
#
# stp = RequestParser()
# stp.parse("/help", {})
# stp.parse("/tambahjadwal date 10 3 2017 10 30 10", {})
# stp.parse("/lihatjadwal", {})
# stp.parse("/ubahjadwal date 30 4 2017 13 30 3", {})
# stp.parse("/lihatjadwal", {})
# stp.parse("/selesaijadwal date", {})
# stp.parse("/reportjadwal", {})
# stp.parse("/hapusjadwal date", {})
# stp.parse("/lihatjadwal", {})
# stp.parse("/lihatpengeluaran", {})
