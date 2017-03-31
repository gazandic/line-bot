from __future__ import unicode_literals

import sys

from functools import reduce

from bawel.action.Action import Action
from bawel.util import checkInputWaktu, checkInputTanggal
from bawel.model.Expense import Expense
from bawel.model.Event import Event

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
                    'people_name' : people_name
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

    def act(self, jumlah, state):
        ev1 = Expense(state['id'],
                state['pengeluaran_name'],
                state['event_name'],
                state['people_name'],
                jumlah)
        ev1.create()
        pengeluaran_name = state['pengeluaran_name'].replace("_"," ")
        state.pop('pengeluaran_name', None)
        state.pop('event_name', None)
        state.pop('people_name', None)
        return (state, "Pengeluaran "+pengeluaran_name+" berhasil ditambahkan dengan senilai "+amount)


class LihatPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, state, event_name=""):
        ex1 = Expense()
        if event_name == "":
            expenses = ex1.search({"lineid": state['id']})
        else:
            expenses = ex1.search({"lineid": state['id'], "name":event_name})

        def printExpense(prev, expense):
            L = [expense['about'],expense['name'],expense['peoplename']]
            S = '\n'.join(L)
            return '{0}\n{1}'.format(prev, S)

        if expenses.count() == 1:
            expense = expenses[0]
            L = [expense['about'],expense['name'],expense['peoplename']]
            S = '\n'.join(L)
            output = '{0}'.format(S)

        elif expenses.count() > 1:
            output = reduce(printExpense, expenses)

        else :
            if event_name == "":
                output = "Maaf tidak ada pengeluaran di database bawel :("
            else:
                event_name = event_name.replace("_"," ")
                output = "Maaf tidak ada pengeluaran di acara "+event_name+" di database bawel :("
        return (state, output)


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
