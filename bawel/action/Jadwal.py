from __future__ import unicode_literals

from functools import reduce
from datetime import datetime, date, time

from bawel.action.Action import Action
from bawel.model.event import Event

def checkInputWaktu(jam, menit):
    t = time(int(jam), int(menit))

def checkInputTanggal(hari, bulan, tahun, jam, menit):
    d = date(int(tahun), int(bulan), int(hari))
    checkInputWaktu(jam, menit)

# def normalizeParamJadwal(param, reminder):
#     if len(param) == 8:
#         param.append(1)         # default
#     param.append(reminder)
#     return param

# TODO: import job yang dilakukan

class TambahJadwal(Action):
    def act(self, namajadwal, hari, bulan, tahun, jam, menit, reminder, state, urgensi=1):
        try:
            checkInputTanggal(hari, bulan, tahun, jam, menit)
            ev1 = Event(self.lineid,namajadwal,urgensi,hari,bulan,tahun,jam,menit,0)
            eid = ev1.create()
            reminder.add(eid, datetime.datetime(tahun, bulan, hari, jam, menit), job)
            return (state, "Event successfuly added")

        except ValueError:
            return (state, "format penulisan '/tambahjadwal namajadwal hari bulan tahun jam menit'")

class LihatJadwal(Action):
    def act(self, state):
        ev1 = Event(self.lineid,"lol",10,1,1,1,1,1,0)
        events = ev1.search({"lineid":self.lineid})

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
            ev1 = Event(self.lineid,namajadwal,urgensi,hari,bulan,tahun,jam,menit,0)
            eid = ev1.update()
            dtime = ev1.searchOne({ "_id": eid })["datetime"]
            tm = dt.strptime(str(dtime), "%Y-%m-%d %H:%M:%S.%f")
            reminder.modify(eid, tm)
            return (state, "Event changed successfully")

        except ValueError:
            return (state, "format penulisan '/ubahjadwal namajadwal hari bulan tahun jam menit'  \nnama jadwal tidak dapat diubah")

class HapusJadwal(Action):
    def act(self, namajadwal, reminder, state):
        ev1 = Event(self.lineid,"lol",10,1,1,1,1,1,0)
        eid = ev1.searchOne({"lineid":self.lineid,"about":namajadwal})
        ev1.removeQuery({"lineid":self.lineid,"about":namajadwal})
        reminder.remove(eid)
        return (state, "Event removed successfully")

# class SelesaiJadwal(Action):
#     def act(self, namajadwal, state):
#         ev1 = Event(self.lineid,"lol",10,1,1,1,1,1,0)
#         eve = ev1.searchOne({"lineid":self.lineid,"about":namajadwal})
#         ev1.set(eve)
#         ev1.setFulfilled(1)
#         ev1.update()

class ReportJadwal(Action):
    def act(self, state):
        ev1 = Event(self.lineid,"lol",10,1,1,1,1,1,0)
        events = ev1.search({"lineid":self.lineid})
        i = 0
        total = 0
        for event in events:
            total += 1
            if int(event['fullfiled']) == 1:
                i += 1
        percentage = i / total * 100
        return (state, "%.2f".format(percentage))
