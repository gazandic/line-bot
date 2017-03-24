from __future__ import unicode_literals

from datetime import datetime,date,time

import bawel.constant.UserConstant

from bawel.action.Action import dispatch_action
from bawel.action.Help import *
from bawel.action.Jadwal import *
from bawel.action.Pengeluaran import *

# from bawel.model.User import User
# from bawel.model.Event import Event
# from bawel.model.Expense import Expense

class RequestParser:
    self.command = {
        '/help': HelpAll,
        '/jadwal': HelpJadwal,
        '/habit': HelpHabit,
        '/pengeluaran': HelpPengeluaran,
        '/tambahjadwal': TambahJadwal,
        '/lihatjadwal': LihatJadwal,
        '/ubahjadwal': UbahJadwal,
        '/hapusjadwal': HapusJadwal,
        '/selesaijadwal': SelesaiJadwal,
        '/reportjadwal': ReportJadwal,
        # '/tambahhabit': self.tambahhabitCommand,
        # '/lihathabit': self.lihathabitCommand,
        # '/ubahhabit': self.ubahhabitCommand,
        # '/hapushabit': self.hapushabitCommand,
        # '/selesaihabit': self.selesaihabitCommand,
        # '/reporthabit': self.reporthabitCommand,
        '/tambahpengeluaran': TambahPengeluaran,
        '/lihatpengeluaran': LihatPengeluaran,
        '/ubahpengeluaran': UbahPengeluaran,
        '/hapuspengeluaran': HapusPengeluaran,
        # '/selesaipengeluaran': self.selesaipengeluaranCommand,
        '/reportpengeluaran': ReportPengeluaran
    }

    def parse(self, text):
        lineid = self.state.id
        us = User(lineid, "undefined", "undefined",
                UserConstant.STATE_UNKNOWN_USERNAME)
        user = us.searchOne({"lineid":lineid})
        user = us.searchOne({"lineid":lineid})
        if not user:
            return us.create()
        us.set(user)
        if 'name' not in state or not state['name']:
            return dispatch_action(UserPromptName, state)
        elif 'loc' not in state or not state['loc']:
            return dispatch_action(UserPromptLoc, state)
        elif user['state'] == UserConstant.STATE_KNOWN_USER:
            return self.chooseMenu(us)
        else:
            return self.default()

    def default(self):
        print("lol")

    def chooseMenu(self, us):
        cmd = self.text.split()
        param = cmd[1:]
        cmd = cmd[0]
        bossName = str(self.us.getName())
        param.append(bossName)
        try:
            self.command[cmd](*param)
        except IndexError:
            print("halo bos, sekretaris bos "+bossName+ " kurang paham, coba ketik /help ya bos :)")



stp = StateTextParser("/help", "2783718371823718")
stp.parse()
stp.setText("/tambahjadwal date 10 3 2017 10 30 10")
stp.parse()
stp.setText("/lihatjadwal")
stp.parse()
stp.setText("/ubahjadwal date 30 4 2017 13 30 3")
stp.parse()
stp.setText("/lihatjadwal")
stp.parse()
stp.setText("/selesaijadwal date")
stp.parse()
stp.setText("/reportjadwal")
stp.parse()
stp.setText("/hapusjadwal date")
stp.parse()
stp.setText("/lihatjadwal")
stp.parse()


stp.setText("/lihatpengeluaran")
stp.parse()
