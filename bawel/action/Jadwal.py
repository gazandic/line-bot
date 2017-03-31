from __future__ import unicode_literals

import sys
import time as t

from datetime import datetime, date, time
from functools import reduce

from bawel.model.Expense import Expense
from bawel.action.Action import Action
from bawel.model.Event import Event
from bawel.util import checkInputWaktu, checkInputTanggal

from linebot.models import (
    TemplateSendMessage,
    CarouselTemplate, CarouselColumn, PostbackTemplateAction, URITemplateAction
)



class TambahJadwal(Action):
    def act(self, namajadwal, hari, bulan, tahun, jam, menit, reminder, state, location=None):

        def job(eid, text, lineid, location=None, stickerid=180):
            reminder.push(text, stickerid, lineid, location)

        try:
            dt = checkInputTanggal(hari, bulan, tahun, jam, menit)
            ev1 = Event(state['id'],namajadwal,hari,bulan,tahun,jam,menit,location,0)
            ev1.create()

            reminder.add(namajadwal, dt, job, ("jangan lupa 1 jam lagi ada "+namajadwal, state['id'], location,))
            namajadwal = namajadwal.replace("_"," ")
            return (state, "acara "+namajadwal+" telah ditambah")

        except:
            return (state, "Maaf kak, bawel ga ngerti, coba nambahjadwalnya kaya gini ya kak'si bawel tolong tambah acara/event/jadwal nonton bareng tanggal 29 Maret jam 5.50 sore'")


class LihatJadwal(Action):
    def act(self, state):
        try:
            ev1 = Event()
            events = ev1.search({"lineid":state['id']})
            if events.count() == 0 :
                output = "Maaf tidak ada jadwal di database bawel :("
                return (state, output)
            licc = []
            ite = 0
            lievent = []
            for event in events:
                ite += 1
                about = event['about'].replace("_"," ")
                date = str(datetime.strptime(str(event['datetime']),"%Y-%m-%d %H:%M:%S").strftime("%d-%m %H:%M"))
                text = "Acara tentang "+about+" diadakan pada "+str(date)
                cc = CarouselColumn(text=text, title=about, actions=[
                    URITemplateAction(label='Go to line.me', uri='https://line.me'),
                    PostbackTemplateAction(label='ping', data='ping')])
                licc.append(cc)
                if ite == 4:
                    carousel_template = CarouselTemplate(columns=licc)
                    template_message = TemplateSendMessage(
                        alt_text='List jadwal', template=carousel_template)
                    ite = 0
                    lievent.append(template_message)
                    licc = []
            if ite > 0:
                carousel_template = CarouselTemplate(columns=licc)
                template_message = TemplateSendMessage(
                    alt_text='List jadwal', template=carousel_template)
                lievent.append(template_message)
            return (state, lievent)
        except:
            print (sys.exc_info())

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
    def act(self, namajadwal, hari, bulan, tahun, jam, menit, reminder, state):
        try:
            dtime = checkInputTanggal(hari, bulan, tahun, jam, menit)
            ev1 = Event(state['id'],namajadwal,hari,bulan,tahun,jam,menit,0)
            ev1.update()
            print('nande')
        except :
            print(sys.exc_info())
            return (state, "Maaf kak, bawel ga ngerti, coba nambahjadwalnya kaya gini ya kak'si bawel tolong ubah acara/event/jadwal nonton bareng tanggal 29 Maret jam 5.50 sore'")
        try:
            reminder.modify(namajadwal, dtime)
            namajadwal = namajadwal.replace("_"," ")
            return (state, "acara "+namajadwal+" telah diubah")
        except:
            print(sys.exc_info())
            namajadwal = namajadwal.replace("_"," ")
            return (state, "acara "+namajadwal+" telah diubah")

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
