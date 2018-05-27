from __future__ import unicode_literals

import sys
from functools import reduce

from linebot.models import (
    TemplateSendMessage,
    CarouselTemplate, CarouselColumn, PostbackTemplateAction, URITemplateAction
)

from bawel.action.Action import Action
from bawel.model.Event import Event
from bawel.model.Expense import Expense

errorCreateUpdatePengeluaran = "coba lagi kak, coba tulis kaya gini 'si bawel tolong tambah/ubah pengeluaran <makan siang>(nama_pengeluaran) untuk acara <pergi ke jogja>(nama_acara) sebesar 50000 oleh Kevin' hehe"


class TambahPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, event_name, pengeluaran_name, people_name, state, duit=-1):
        if Event().searchOne({"lineid": state['id'], "about": event_name}):
            duit = float(duit)
            if duit < 0:
                state = {**state,
                         'pengeluaran_name': pengeluaran_name,
                         'event_name': event_name,
                         'people_name': people_name,
                         'before_state': state['state_id']
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
                return (state, "Pengeluaran " + pengeluaran_name + " telah ditambahkan di acara " + event_name)
            except:
                print(sys.exc_info())
                return (state, errorCreateUpdatePengeluaran)
        else:
            event_name = event_name.replace("_", " ")
            return (state, "acara " + event_name + " belum ada :( ")


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
        pengeluaran_name = state['pengeluaran_name'].replace("_", " ")
        state.pop('pengeluaran_name', None)
        state.pop('event_name', None)
        state.pop('people_name', None)
        state.pop('before_state', None)
        return (state, "Pengeluaran " + pengeluaran_name + " berhasil ditambahkan dengan senilai " + jumlah)


class LihatPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, state, event_name=""):
        try:
            ex1 = Expense()
            if event_name == "":
                expenses = ex1.search({"lineid": state['id']})
            else:
                expenses = ex1.search({"lineid": state['id'], "name": event_name})

            if expenses.count() == 0:
                if event_name == "":
                    output = "Maaf tidak ada pengeluaran di database bawel :("
                else:
                    event_name = event_name.replace("_", " ")
                    output = "Maaf tidak ada pengeluaran di acara " + event_name + " di database bawel :("
                return (state, output)
            licc = []
            ite = 0
            ikut = 9
            liexpenses = []
            for expense in expenses:
                if expense['about'] == "ikut":
                    continue
                ite += 1
                about = "Pengeluaran " + expense['about'].replace("_", " ")
                event_name = expense['name'].replace("_", " ")[0:20]
                amount = str(expense['total'])[0:10]
                people_name = str(expense['peoplename'])[0:10]
                text = "acara " + event_name + " sebesar " + amount + " oleh " + people_name
                report = '/reportpengeluaran ' + expense['name']
                hapus = '/hapuspengeluaran ' + expense['name'] + " " + expense['about']
                actionli = [
                    PostbackTemplateAction(label='Report Pengeluaran', data=report),
                    # PostbackTemplateAction(label='Hapus Pengeluaran', data=hapus)
                ]
                if expense.get('pathnota') and expense['pathnota'] != "":
                    actionli.append(URITemplateAction(label='go to nota', uri=expense['pathnota']))
                else:
                    actionli.append(URITemplateAction(label='tidak ada nota', uri='http://google.com'))

                cc = CarouselColumn(text=text, title=about, actions=actionli)
                licc.append(cc)
                if ite == 4:
                    carousel_template = CarouselTemplate(columns=licc)
                    template_message = TemplateSendMessage(
                        alt_text='List pengeluaran', template=carousel_template)
                    ite = 0
                    liexpenses.append(template_message)
                    licc = []
            if len(licc) == 0 and len(liexpenses) == 0:
                if event_name == "":
                    output = "Maaf tidak ada pengeluaran di database bawel :("
                else:
                    event_name = event_name.replace("_", " ")
                    output = "Maaf tidak ada pengeluaran di acara " + event_name + " di database bawel :("
                return (state, output)
            if ite > 0:
                carousel_template = CarouselTemplate(columns=licc)
                template_message = TemplateSendMessage(
                    alt_text='List pengeluaran', template=carousel_template)
                liexpenses.append(template_message)
            return (state, liexpenses)
        except:
            print(sys.exc_info())


class UbahPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, event_name, pengeluaran_name, people_name, duit, state):

        if Event().searchOne({"lineid": state['id'], "about": event_name}):
            try:
                ex1 = Expense(state['id'], pengeluaran_name, event_name, people_name, duit)
                ex1.update()

                pengeluaran_name = pengeluaran_name.replace("_", " ")
                return (state, "Pengeluaran " + pengeluaran_name + " berhasil dirubah")
            except:
                print(sys.exc_info())
                return (state, errorCreateUpdatePengeluaran)
        else:
            event_name = event_name.replace("_", " ")
            return (state, "acara " + event_name + " belum ada :( ")


class HapusPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, event_name, state, pengeluaran_name=""):
        ex1 = Expense()
        if pengeluaran_name == "":
            ex1.removeQuery({"lineid": state['id'],
                             "name": event_name})
            event_name = event_name.replace("_", " ")
            return (state, "Semua pengeluaran untuk acara " + event_name + " telah dihapus")
        else:
            ex1.removeQuery({"lineid": state['id'],
                             "about": pengeluaran_name,
                             "name": event_name})
            event_name = event_name.replace("_", " ")
            pengeluaran_name = pengeluaran_name.replace("_", " ")
            return (state, "Pengeluaran " + pengeluaran_name + " untuk acara " + event_name + " telah dihapus")


class ReportPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, event_name, state):
        exp = Expense()
        pipeline = [{'$match': {'name': event_name}}, {'$group': {'_id': "$peoplename", 'total': {'$sum': "$total"}}}]

        res = list(exp.aggregate(pipeline))
        if len(res) == 0:
            event_name = event_name.replace("_", " ")
            out = "maaf, tidak ada pengeluaran untuk " + event_name + " :("
            return (state, out)
        print(res)
        avg = reduce(lambda x, y: x + float(y['total']), res, 0) / len(res)
        print(avg)

        def reducer(prev, cur):
            diff = cur['total'] - avg
            if prev == "":
                prev = "List bayar membayar"
            if (diff > 0):
                return prev + '\n' + 'si {0} dapet {1}'.format(cur['_id'], "%.0f" % diff)
            return prev + '\n' + ' si {0} harus bayar {1}'.format(cur['_id'], "%.0f" % abs(diff))

        out = reduce(reducer, res, '')

        return (state, out)
