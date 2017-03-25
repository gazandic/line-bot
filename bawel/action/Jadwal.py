from __future__ import unicode_literals

from bawel.action.Action import Action

def checkInputWaktu(jam, menit):
    t = time(int(jam), int(menit))

def checkInputTanggal(hari, bulan, tahun, jam, menit):
    d = date(int(tahun), int(bulan), int(hari))
    checkInputWaktu(jam, menit)

# TODO: import job yang dilakukan

class TambahJadwal(Action):
    def act(self, state, namajadwal, hari, bulan, tahun, jam, menit, urgensi, reminder, bossname):
        try:
            self.checkInputTanggal(hari, bulan, tahun, jam, menit)
            ev1 = Event(self.lineid,namajadwal,urgensi,hari,bulan,tahun,jam,menit,0)
            eid = ev1.create()
            reminder.add(eid, datetime.datetime(tahun, bulan, hari, jam, menit), job)

        except ValueError:
            print ("format penulisan '/tambahjadwal namajadwal hari bulan tahun jam menit'")

class LihatJadwal(Action):
    def act(self, state, bossname):
        ev1 = Event(self.lineid,"lol",10,1,1,1,1,1,0)
        events = ev1.search({"lineid":self.lineid})
        for event in events:
            print(event['about'])
            print(event['datetime'])
            print(event['urgency'])
            print(event['fullfiled'])

class UbahJadwal(Action):
    def act(self, state, namajadwal, hari, bulan, tahun, jam, menit, urgensi, reminder, bossname):
        try:
            self.checkInputTanggal(hari, bulan, tahun, jam, menit)
            ev1 = Event(self.lineid,namajadwal,urgensi,hari,bulan,tahun,jam,menit,0)
            eid = ev1.update()
            dtime = ev1.searchOne({ "_id": eid })["datetime"]
            tm = dt.strptime(str(dtime), "%Y-%m-%d %H:%M:%S.%f")
            reminder.modify(eid, tm)

        except ValueError:
            print ("format penulisan '/ubahjadwal namajadwal hari bulan tahun jam menit'  \nnama jadwal tidak dapat diubah")

class HapusJadwal(Action):
    def act(self, state, namajadwal, reminder, bossname):
        ev1 = Event(self.lineid,"lol",10,1,1,1,1,1,0)
        eid = ev1.searchOne({"lineid":self.lineid,"about":namajadwal})
        ev1.removeQuery({"lineid":self.lineid,"about":namajadwal})
        reminder.remove(eid)

class SelesaiJadwal(Action):
    def act(self, state, namajadwal, bossname):
        ev1 = Event(self.lineid,"lol",10,1,1,1,1,1,0)
        eve = ev1.searchOne({"lineid":self.lineid,"about":namajadwal})
        ev1.set(eve)
        ev1.setFulfilled(1)
        ev1.update()

class ReportJadwal(Action):
    def act(self, state, bossname):
        ev1 = Event(self.lineid,"lol",10,1,1,1,1,1,0)
        events = ev1.search({"lineid":self.lineid})
        i = 0
        total = 0
        for event in events:
            total += 1
            if int(event['fullfiled']) == 1:
                i += 1
        percentage = i / total * 100
        print("%.2f",percentage)
