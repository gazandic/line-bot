from __future__ import unicode_literals

import sys

from functools import reduce

from bawel.action.Action import Action
from bawel.util import checkInputWaktu, checkInputTanggal
from bawel.model.Expense import Expense
from bawel.model.Event import Event

from linebot.models import (
    TemplateSendMessage,
    CarouselTemplate, CarouselColumn, PostbackTemplateAction, URITemplateAction
)

errorCreateUpdatePengeluaran = "coba lagi kak, coba tulis kaya gini 'si bawel tolong tambah/ubah pengeluaran makan siang untuk acara pergi ke jogja sebesar 50000 oleh gazandi' hehe"

class HelpPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, state):
        # TODO:
        return (state, "ntaran")

class TambahPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, event_name, pengeluaran_name, people_name, state, duit=-1):
        if Event().searchOne({"lineid":state['id'], "about":event_name}):
            duit = float(duit)
            if duit < 0:
                state = {**state,
                    'pengeluaran_name': pengeluaran_name,
                    'event_name': event_name,
                    'people_name' : people_name,
                    'before_state' : state['state_id']
                }
                return (state, "Masukkan jumlah duit \nBisa lewat teks atau input bon")

            try:
                ev1 = Expense(state['id'],
                        pengeluaran_name,
                        event_name,
                        people_name,
                        duit)
                ev1.create()
                event_name = event_name.replace("_", " ")
                pengeluaran_name = pengeluaran_name.replace("_", " ")
                return (state, "Pengeluaran "+pengeluaran_name+" telah ditambahkan di acara "+event_name)
            except:
                print(sys.exc_info())
                return (state, errorCreateUpdatePengeluaran)
        else:
            event_name = event_name.replace("_"," ")
            return (state, "acara "+event_name+" belum ada :( ")

class ImageTambahPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, jumlah, path, state):
        ev1 = Expense(state['id'],
                state['pengeluaran_name'],
                state['event_name'],
                state['people_name'],
                jumlah)
        ev1.create()
        ev1.updatePathNota(str(path))
        pengeluaran_name = state['pengeluaran_name'].replace("_"," ")
        state.pop('pengeluaran_name', None)
        state.pop('event_name', None)
        state.pop('people_name', None)
        state.pop('before_state', None)
        return (state, "Pengeluaran "+pengeluaran_name+" berhasil ditambahkan dengan senilai "+jumlah)


class LihatPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, state, event_name=""):
        try:
            ex1 = Expense()
            if event_name == "":
                expenses = ex1.search({"lineid": state['id']})
            else:
                expenses = ex1.search({"lineid": state['id'], "name":event_name})

            if expenses.count() == 0 :
                if event_name == "":
                    output = "Maaf tidak ada pengeluaran di database bawel :("
                else:
                    event_name = event_name.replace("_"," ")
                    output = "Maaf tidak ada pengeluaran di acara "+event_name+" di database bawel :("
                return (state, output)
            licc = []
            ite = 0
            liexpenses = []
            for expense in expenses:
                ite += 1
                about = expense['about'].replace("_"," ")
                event_name = expense['name'].replace("_"," ")[0:20]
                amount = str(expense['total'])
                people_name = str(expense['peoplename'])
                text = "acara "+event_name+" sebesar "+amount+ " oleh "+people_name
                liact = [
                    URITemplateAction(label='Go to line.me', uri='https://line.me'),
                    PostbackTemplateAction(label='ping', data='ping')]
                if expense.get('pathnota') and expense['pathnota'] != "":
                    liact.append(URITemplateAction(label='Go to nota', uri=expense['pathnota']))
                cc = CarouselColumn(text=text, title="Pengeluaran "+about, actions=liact)
                licc.append(cc)
                if ite == 4:
                    carousel_template = CarouselTemplate(columns=licc)
                    template_message = TemplateSendMessage(
                        alt_text='List pengeluaran', template=carousel_template)
                    ite = 0
                    liexpenses.append(template_message)
                    licc = []
            if ite > 0:
                carousel_template = CarouselTemplate(columns=licc)
                template_message = TemplateSendMessage(
                    alt_text='List pengeluaran', template=carousel_template)
                liexpenses.append(template_message)
            return (state, liexpenses)
        except:
            print (sys.exc_info())

class UbahPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, pengeluaran_name, event_name, people_name, duit, state):

        if Event().searchOne({"lineid":state['id'], "about":event_name}):
            try:
                ex1 = Expense(state['id'],pengeluaran_name,event_name,people_name,duit)
                ex1.update()

                pengeluaran_name = pengeluaran_name.replace("_", " ")
                return (state, "Pengeluaran "+pengeluaran_name+" berhasil dirubah")
            except :
                print(sys.exc_info())
                return (state, errorCreateUpdatePengeluaran)
        else:
            event_name = event_name.replace("_"," ")
            return (state, "acara "+event_name+" belum ada :( ")


class HapusPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, event_name, state, pengeluaran_name=""):
        ex1 = Expense()
        if pengeluaran_name == "":
            ex1.removeQuery({"lineid":state['id'],
                "name": event_name})
            event_name = event_name.replace("_", " ")
            return (state, "Semua pengeluaran untuk acara "+event_name+" telah dihapus")
        else :
            ex1.removeQuery({"lineid":state['id'],
                "about" : pengeluaran_name,
                "name": event_name})
            event_name = event_name.replace("_", " ")
            pengeluaran_name = pengeluaran_name.replace("_", " ")
            return (state, "Pengeluaran "+pengeluaran_name+" untuk acara "+event_name+" telah dihapus")

class ReportPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, event_name, state):
        ev1 = Expense()
        # TODO ICAL
        expenses = ev1.search({"lineid":state['id'],"name":event_name})
        # i = 0
        # total = 0
        # for expense in expenses:
        #     total += 1
        #     if int(expense['pathnota']) == 1:
        #         i += 1
        # percentage = i / total * 100
        # print("%.2f",percentage)
