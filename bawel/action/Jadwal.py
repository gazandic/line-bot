from __future__ import unicode_literals

import sys
import time as t

from datetime import datetime, date, time
from functools import reduce

from bawel.model.Expense import Expense
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
            ev1.create()
            def job(eid, text, lineid, stickerid=180):
                reminder.push(text, stickerid, lineid)
            reminder.add(namajadwal, dt, job, ("jangan lupa 1 jam lagi ada "+namajadwal,state['id'], ))
            namajadwal = namajadwal.replace("_"," ")
            return (state, "acara "+namajadwal+" telah ditambah")
        except:
            print(sys.exc_info())
            return (state, "Maaf kak, bawel ga ngerti, coba nambahjadwalnya kaya gini ya kak'si bawel tolong tambah acara/event/jadwal nonton bareng tanggal 29 Maret jam 5.50 sore'")

class LihatJadwal(Action):
    def act(self, state):
        ev1 = Event()
        events = ev1.search({"lineid":state['id']})

        def printEvent(prev, ev):
            L = [ev['about'],str(ev['datetime']),str(ev['fullfiled'])]
            S = '\n'.join(L)
            return '{0}\n{1}'.format(prev, S)

        if events.count() == 1:
            ev = events[0]
            L = [ev['about'],str(ev['datetime']),str(ev['fullfiled'])]
            S = '\n'.join(L)
            output = '{0}'.format(S)
        elif events.count() > 1:
            output = reduce(printEvent, events)
        else :
            output = "Maaf tidak ada jadwal di database bawel :("

        return (state, output)

class IkutJadwal(Action):
    def act(self, event_name, people_name, state):
        try:
            if Event().searchOne({"lineid":state['id'], "about":event_name}):
                ex1 = Expense(state['id'],
                        'ikut',
                        event_name,
                        people_name,
                        0)
                ex1.create()
                event_name = event_name.replace("_"," ")
                return (state, people_name+" berhasil ikut pada "+event_name)
            else:
                event_name = event_name.replace("_"," ")
                return (state, "acara "+event_name+" belum ada :( ")
        except:
            print(sys.exc_info())
            return (state, "Maaf kak, bawel ga ngerti, coba nambahjadwalnya kaya gini ya kak'si bawel ikut acara/event/jadwal nonton bareng oleh kevin'")

class TakIkutJadwal(Action):
    def act(self, event_name, people_name, state):
        try:
            ex1 = Expense(state['id'],
                    'ikut',
                    event_name,
                    people_name,
                    0)
            ev1 = Expense()
            ev1.removeQuery({"lineid":state['id'],
                "about":'ikut', "name":event_name, "peoplename":people_name})
            event_name = event_name.replace("_"," ")
            return (state, people_name+" tidak jadi ikut pada "+event_name)
        except:
            return (state, "Maaf kak, bawel ga ngerti, coba nambahjadwalnya kaya gini ya kak'si bawel gajadi ikut acara/event/jadwal nonton bareng oleh kevin'")


class UbahJadwal(Action):
    def act(self, namajadwal, hari, bulan, tahun, jam, menit, reminder, state, urgensi=1):
        try:
            dtime = checkInputTanggal(hari, bulan, tahun, jam, menit)
            ev1 = Event(state['id'],namajadwal,urgensi,hari,bulan,tahun,jam,menit,0)
            ev1.update()
            reminder.modify(namajadwal, dtime)
            namajadwal = namajadwal.replace("_"," ")
            return (state, "acara "+namajadwal+" telah diubah")

        except :
            print(sys.exc_info())
            return (state, "Maaf kak, bawel ga ngerti, coba nambahjadwalnya kaya gini ya kak'si bawel tolong ubah acara/event/jadwal nonton bareng tanggal 29 Maret jam 5.50 sore'")


class HapusJadwal(Action):
    def act(self, namajadwal, reminder, state):
        try:
            ev1 = Event()
            ev1.removeQuery({"lineid":state['id'],"about":namajadwal})
            reminder.remove(namajadwal)
            namajadwal = namajadwal.replace("_"," ")
            return (state, "acara "+namajadwal+" telah dihapus")
        except:
            namajadwal = namajadwal.replace("_"," ")
            return (state, "Maaf kak, jadwal "+namajadwal+" tidak ada :( ")

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
