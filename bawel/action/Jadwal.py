from __future__ import unicode_literals

import sys
import time as t

from datetime import datetime, date, time
from functools import reduce

from bawel.action.Action import Action
from bawel.model.Event import Event
from bawel.util import checkInputWaktu, checkInputTanggal

# def normalizeParamJadwal(param, reminder):
#     if len(param) == 8:
#         param.append(1)         # default
#     param.append(reminder)
#     return param

# TODO: import job yang dilakukan

class TambahJadwal(Action):
    def act(self, namajadwal, hari, bulan, tahun, jam, menit, reminder, state, urgensi=1):
        try:
            dt = checkInputTanggal(hari, bulan, tahun, jam, menit)
            ev1 = Event(state['id'],namajadwal,urgensi,hari,bulan,tahun,jam,menit,0)
            eid = ev1.create()
            # print("created")
            def job(eid, text, lineid, stickerid=180):
                reminder.push(text, stickerid, lineid)

            reminder.add(eid, t.mktime(dt.timetuple()), job, ("jangan lupa 1 jam lagi ada "+namajadwal,state['id'], ))
            return (state, "Event successfuly added")

        except ValueError:
            # print(sys.exc_info())
            return (state, "format penulisan '/tambahjadwal namajadwal hari bulan tahun jam menit'")


class LihatJadwal(Action):
    def act(self, state):
        ev1 = Event()
        events = ev1.search({"lineid":state['id']})

        def printEvent(prev, ev):
            L = [event['about'],event['datetime'],event['urgency'],event['fullfiled']]
            S = '\n'.join(L)
            return '{0}\n{1}'.format(prev, S)

        output = reduce(printEvent, events)
        return (state, output)


class UbahJadwal(Action):
    def act(self, namajadwal, hari, bulan, tahun, jam, menit, reminder, state, urgensi=1):
        try:
            checkInputTanggal(hari, bulan, tahun, jam, menit)
            ev1 = Event(state['id'],namajadwal,urgensi,hari,bulan,tahun,jam,menit,0)
            eid = ev1.update()
            dtime = ev1.searchOne({ "_id": eid })["datetime"]
            tm = dt.strptime(str(dtime), "%Y-%m-%d %H:%M:%S")
            reminder.modify(eid, tm)
            return (state, "Event changed successfully")

        except ValueError:
            return (state, "format penulisan '/ubahjadwal namajadwal hari bulan tahun jam menit'  \nnama jadwal tidak dapat diubah")


class HapusJadwal(Action):
    def act(self, namajadwal, reminder, state):
        ev1 = Event()
        eid = ev1.searchOne({"lineid":state['id'],"about":namajadwal})
        ev1.removeQuery({"lineid":state['id'],"about":namajadwal})
        reminder.remove(eid)
        return (state, "Event removed successfully")

# class SelesaiJadwal(Action):
#     def act(self, namajadwal, state):
#         ev1 = Event(state['id'],"lol",10,1,1,1,1,1,0)
#         eve = ev1.searchOne({"lineid":state['id'],"about":namajadwal})
#         ev1.set(eve)
#         ev1.setFulfilled(1)
#         ev1.update()

class ReportJadwal(Action):
    def act(self, state):
        ev1 = Event()
        events = ev1.search({"lineid":state['id']})
        i = 0
        total = 0
        for event in events:
            total += 1
            if int(event['fullfiled']) == 1:
                i += 1
        percentage = i / total * 100
        return (state, "%.2f".format(percentage))
