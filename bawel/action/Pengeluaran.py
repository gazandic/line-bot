from __future__ import unicode_literals

from bawel.action.Action import Action

class HelpPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, state, bossname):
        print("ntaran")
        return state

class TambahPengeluaran(Action):
    def act(self, state, namapengeluaran, hari, bulan, tahun, jam, menit, name, bossName):
        try:
            self.checkInputTanggal(hari, bulan, tahun, jam, menit)
            ev1 = Expense(self.lineid,namapengeluaran,name,hari,bulan,tahun,jam,menit,0)
            ev1.create()
        except ValueError:
            print ("format penulisan '/tambahpengeluaran namapengeluaran hari bulan tahun jam menit name'")

class LihatPengeluaran(Action):
    def act(self, state, bossName):
        ev1 = Expense(self.lineid,"lol","nama",1,1,1,1,1,0)
        expenses = ev1.search({"lineid":self.lineid})
        for expense in expenses:
            print(expense['about'])
            print(expense['datetime'])
            print(expense['name'])
            print(expense['pathnota'])

class UbahPengeluaran(Action):
    def act(self, state, namapengeluaran, hari, bulan, tahun, jam, menit, name, bossName):
        try:
            self.checkInputTanggal(hari, bulan, tahun, jam, menit)
            ev1 = Expense(self.lineid,namapengeluaran,name,hari,bulan,tahun,jam,menit,0)
            ev1.update()
        except ValueError:
            print ("format penulisan '/ubahpengeluaran namapengeluaran hari bulan tahun jam menit name'  \nnama pengeluaran tidak dapat diubah")

class HapusPengeluaran(Action):
    def act(self, state, namapengeluaran, bossName):
        ev1 = Expense(self.lineid,"lol","nama",1,1,1,1,1,0)
        ev1.removeQuery({"lineid":self.lineid,"about":namapengeluaran})

class ReportPengeluaran(Action):
    def act(self, state, bossName):
        ev1 = Expense(self.lineid,"lol","nama",1,1,1,1,1,0)
        # expenses = ev1.search({"lineid":self.lineid})
        # i = 0
        # total = 0
        # for expense in expenses:
        #     total += 1
        #     if int(expense['pathnota']) == 1:
        #         i += 1
        # percentage = i / total * 100
        # print("%.2f",percentage)
