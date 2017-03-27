from __future__ import unicode_literals

from bawel.action.Action import Action

class HelpPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, state):
        # TODO:
        return (state, "ntaran")

class TambahPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, state, namapengeluaran, hari, bulan, tahun, jam, menit, name):
        try:
            self.checkInputTanggal(hari, bulan, tahun, jam, menit)
            ev1 = Expense(self.lineid,namapengeluaran,name,hari,bulan,tahun,jam,menit,0)
            ev1.create()
            return (state, "Expenses successfuly added")
        except ValueError:
            return (state, "format penulisan '/tambahpengeluaran namapengeluaran hari bulan tahun jam menit name'")

class LihatPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, state):
        ev1 = Expense(self.lineid,"lol","nama",1,1,1,1,1,0)
        expenses = ev1.search({"lineid":self.lineid})
        def printExpense(prev, exp):
            L = [expense['about'],expense['datetime'],expense['name'],expense['pathnota']]
            S = '\n'.join(L)
            return '{0}\n{1}'.format(prev, S)

        output = reduce(printExpense, expenses)
        return (state, output)

class UbahPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, state, namapengeluaran, hari, bulan, tahun, jam, menit, name):
        try:
            self.checkInputTanggal(hari, bulan, tahun, jam, menit)
            ev1 = Expense(self.lineid,namapengeluaran,name,hari,bulan,tahun,jam,menit,0)
            ev1.update()
            return (state, "Expenses successfuly changed")
        except ValueError:
            return (state, "format penulisan '/ubahpengeluaran namapengeluaran hari bulan tahun jam menit name'  \nnama pengeluaran tidak dapat diubah")

class HapusPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, state, namapengeluaran):
        ev1 = Expense(self.lineid,"lol","nama",1,1,1,1,1,0)
        ev1.removeQuery({"lineid":self.lineid,"about":namapengeluaran})
        return (state, "Expenses successfuly removed")

class ReportPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, state):
        ev1 = Expense(self.lineid,"lol","nama",1,1,1,1,1,0)
        # TODO
        # expenses = ev1.search({"lineid":self.lineid})
        # i = 0
        # total = 0
        # for expense in expenses:
        #     total += 1
        #     if int(expense['pathnota']) == 1:
        #         i += 1
        # percentage = i / total * 100
        # print("%.2f",percentage)
