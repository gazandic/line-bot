from __future__ import unicode_literals

from bawel.action.Action import Action
from bawel.util import checkInputWaktu, checkInputTanggal

from bawel.model.Expense import Expense

class HelpPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, state):
        # TODO:
        return (state, "ntaran")


class TambahPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, event_name, pengeluaran_name,  people_name, state, duit=-1):
        if float(duit) < 0:
            state = {**state,
                'event_name': event_name,
                'pengeluaran_name': pengeluaran_name,
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
            return (state, "Expenses successfuly added")
        except:
            return (state, "format penulisan '/tambahpengeluaran namapengeluaran hari bulan tahun jam menit name'")


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

        state.pop('pengeluaran_name', None)
        state.pop('event_name', None)
        state.pop('people_name', None)
        return (state, "Expenses successfuly added")


class LihatPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, state):
        ev1 = Expense()
        expenses = ev1.search({"lineid": state['id']})

        def printExpense(prev, exp):
            L = [expense['about'],expense['datetime'],expense['name'],expense['peoplename'],expense['pathnota']]
            S = '\n'.join(L)
            return '{0}\n{1}'.format(prev, S)

        output = reduce(printExpense, expenses)
        return (state, output)


class UbahPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, pengeluaran_name, event_name, people_name, duit, state):
        try:
            # checkInputTanggal(hari, bulan, tahun, jam, menit)
            ev1 = Expense(state['id'],pengeluaran_name,event_name,people_name,duit)
            ev1.update()
            return (state, "Expenses successfuly changed")
        except ValueError:
            return (state, "format penulisan '/ubahpengeluaran nama_pengeluaran nama_event hari bulan tahun jam menit name'  \nnama_pengeluaran tidak dapat diubah")


class HapusPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, nama_pengeluaran, state):
        ev1 = Expense()
        ev1.removeQuery({"lineid":state['id'],
            "about":nama_pengeluaran})
        return (state, "Expenses successfuly removed")


class ReportPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, state):
        ev1 = Expense()
        # TODO
        # expenses = ev1.search({"lineid":state['id']})
        # i = 0
        # total = 0
        # for expense in expenses:
        #     total += 1
        #     if int(expense['pathnota']) == 1:
        #         i += 1
        # percentage = i / total * 100
        # print("%.2f",percentage)
