from __future__ import unicode_literals

import sys
import time as t

from datetime import datetime, date, time, timedelta
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
            dta = dt + timedelta(hours=8)
            date = str(datetime.strptime(str(dta),"%Y-%m-%d %H:%M:%S").strftime("tanggal %d/%m jam %H:%M WIB"))
            namajadwal1 = namajadwal.replace("_"," ")
            reminding = "jangan lupa "+date+" ada jadwal "+namajadwal1
            reminder.add(namajadwal+str(state['id']), dt, job, (reminding, state['id'], location,))
            return (state, "acara "+namajadwal1+" telah ditambah")

        except:
            print(sys.exc_info())
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
                    PostbackTemplateAction(label='Lihat pengeluaran', data='/lihatpengeluaran '+event['about']),
                    PostbackTemplateAction(label='Lihat daftar ikut', data='/reportjadwal '+event['about']),
                    PostbackTemplateAction(label='Hapus jadwal', data='/hapusjadwal '+event['about']),
                ])
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
            reminder.modify(namajadwal+str(state['id']), dtime)
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
            reminder.remove(namajadwal+str(state['id']))
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
    def act(self, event_name, state):
        exp = Expense()
        pipeline = [{'$match': {'name': event_name}}, {'$group': {'_id': "$peoplename", 'total': {'$sum': "$total"}}}]

        res = list(exp.aggregate(pipeline))
        if len(res) == 0:
            event_name = event_name.replace("_"," ")
            out = "maaf, tidak ada yang ikut acara "+event_name + " :("
            return (state, out)

        # avg = reduce(lambda x,y: x+float(y['total']), res, 0) / len(res)
        # print(avg)
        def reducer(prev, cur):
            if prev == "":
                prev = "List ikut ("+str(len(res))+" orang)"
            return prev+'\n'+'{0} ikut'.format(cur['_id'])
        out = reduce(reducer, res, '')

        return (state, out)
