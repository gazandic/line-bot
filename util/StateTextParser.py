import sys
sys.path.insert(0, "../model")
from User import User
from Event import Event
sys.path.insert(1, "../constant")
import UserConstant
from datetime import datetime,date,time

class StateTextParser:
    def __init__(self, text, lineid):
        self.text = text
        self.lineid = lineid
        self.command = {
            '/help': self.helpCommand,
            '/acara': self.acaraCommand,
            '/habit': self.habitCommand,
            '/pengeluaran': self.pengeluaranCommand,
            '/tambahjadwal': self.tambahjadwalCommand,
            '/lihatjadwal': self.lihatjadwalCommand,
            '/ubahjadwal': self.ubahjadwalCommand,
            '/hapusjadwal': self.hapusjadwalCommand,
            '/selesaijadwal': self.selesaijadwalCommand,
            '/reportjadwal': self.reportjadwalCommand
        };

    def setText(self, text):
        self.text = text

    def setLineid(self, lineid):
        self.lineid = lineid

    def parse(self):
        self.us = User(self.lineid,"undefined","undefined",UserConstant.STATE_UNKNOWN_USERNAME)
        user = self.us.searchOne({"lineid":self.lineid})
        user = self.us.searchOne({"lineid":self.lineid})
        if not user:
            return self.us.create()
        self.us.set(user)
        if user['state'] == UserConstant.STATE_UNKNOWN_USERNAME:
            return self.askUsername(us)
        elif user['state'] == UserConstant.STATE_UNKNOWN_USERLOCATION:
            return self.askLocation(us)
        elif user['state'] == UserConstant.STATE_KNOWN_USER:
            return self.chooseMenu(us)
        else:
            return self.default()

    def askUsername(self, us):
        print("Siapa nama bos ?")
        self.us.setName(self.text)
        self.us.setState(UserConstant.STATE_UNKNOWN_USERLOCATION)
        self.us.update()
        def default(self):

        print("lol")

    def askLocation(self, us):
        bossName = str(self.us.getName())
        print("bos "+bossName+" ada di kota mana ?")
        self.us.setLocation(self.text)
        self.us.setState(UserConstant.STATE_KNOWN_USER)
        self.us.update()

    def helpCommand(self, bossName):
        print("Halo bos, bingung sekretaris bos "+bossName+" bisa ngapain aja ?")
        print("sekretaris bos "+bossName+" bisa ngatur acara bos dengan ketik '/acara' dan ingetin bos ")
        print("bisa juga ngatur habit bos dengan ketik '/habit' dan bakal berisikin bos tiap bos ngelakuin itu")
        print("bisa juga ngatur pengeluaran bos dengan ketik '/pengeluaran' ")
        print("bisa juga baca foto yang bos berikan dengan upload foto bapak hehe ")

    def acaraCommand(self, bossName):
        print("Bos kalo bos "+bossName+" mau nambah acara bos ketik '/tambahjadwal namajadwal hari bulan tahun jam menit' ")
        print("bisa juga lihat schedule bos dengan ketik '/lihatjadwal'")
        print("bos juga bisa reschedule bos dengan ketik '/ubahjadwal namajadwal hari bulan tahun jam menit'")
        print("dan hapus schedule bos dengan ketik '/selesaijadwal namajadwal' ")
        print("dan hapus schedule bos dengan ketik '/reportjadwal' ")
        print("dan hapus schedule bos dengan ketik '/hapusjadwal namajadwal' ")

    def habitCommand(self, bossName):
        print("Bos "+bossName+" mau nambah habit bos ketik '/tambahhabit namahabit jam menit hari' ")
        print("bisa juga lihat habit bos dengan ketik '/lihathabit'")
        print("dan ubahhabit bos dengan ketik '/ubahhabit namahabit jam menit hari'")
        print("bos juga bisa hapus habit bos dengan ketik '/hapushabit namahabit' ")

    def pengeluaranCommand(self, bossName):
        # TODO: BIKIN SESUATU
        print("ntaran")

    def tambahjadwalCommand(self, namajadwal, hari, bulan, tahun, jam, menit, urgensi, bossName):
        self.tambahjadwal(namajadwal, hari, bulan, tahun, jam, menit, urgensi, bossName)

    def lihatjadwalCommand(self, bossName):
        self.lihatjadwal(bossName)

    def ubahjadwalCommand(self, namajadwal, hari, bulan, tahun, jam, menit, urgensi, bossName):
        self.ubahjadwal(namajadwal, hari, bulan, tahun, jam, menit, urgensi, bossName)

    def hapusjadwalCommand(self, namajadwal, bossName):
        self.hapusjadwal(namajadwal, bossName)

    def selesaijadwalCommand(self, namajadwal, bossName):
        self.selesaijadwal(namajadwal, bossName)

    def reportjadwalCommand(self, bossName):
        self.reportjadwal(bossName)

    def chooseMenu(self, us):
        cmd = self.text.split()
        param = cmd[1:]
        cmd = cmd[0]
        bossName = str(self.us.getName())
        param.append(bossName)
        try:
            self.command[cmd](*param)
        except IndexError:
            print("halo bos, sekretaris bos "+bossName+ " kurang paham, coba ketik /help ya bos :)")

    def tambahjadwal(self, namajadwal, hari, bulan, tahun, jam, menit, urgensi, bossName):
        try:
            self.checkTambahJadwal(hari, bulan, tahun, jam, menit)
            ev1 = Event(self.lineid,namajadwal,urgensi,hari,bulan,tahun,jam,menit,0)
            ev1.create()
        except ValueError:
            print ("format penulisan '/tambahjadwal namajadwal hari bulan tahun jam menit'")

    def selesaijadwal(self, namajadwal, bossName):
        ev1 = Event(self.lineid,"lol",10,1,1,1,1,1,0)
        eve = ev1.searchOne({"lineid":self.lineid,"about":namajadwal})
        ev1.set(eve)
        ev1.setFulfilled(1)
        ev1.update()

    def ubahjadwal(self, namajadwal, hari, bulan, tahun, jam, menit, urgensi, bossName):
        try:
            self.checkTambahJadwal(hari, bulan, tahun, jam, menit)
            ev1 = Event(self.lineid,namajadwal,urgensi,hari,bulan,tahun,jam,menit,0)
            ev1.update()
        except ValueError:
            print ("format penulisan '/ubahjadwal namajadwal hari bulan tahun jam menit'  \nnama jadwal tidak dapat diubah")

    def reportjadwal(self, bossName):
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

    def lihatjadwal(self):
        ev1 = Event(self.lineid,"lol",10,1,1,1,1,1,0)
        events = ev1.search({"lineid":self.lineid})
        for event in events:
            print(event['about'])
            print(event['datetime'])
            print(event['urgency'])
            print(event['fullfiled'])

    def hapusjadwal(self, namajadwal, bossName):
        ev1 = Event(self.lineid,"lol",10,1,1,1,1,1,0)
        ev1.removeQuery({"lineid":self.lineid,"about":namajadwal})

    def checkTambahJadwal(self, hari, bulan, tahun, jam, menit):
        d = date(int(tahun), int(bulan), int(hari))
        t = time(int(jam), int(menit))

stp = StateTextParser("/help", "2783718371823718")
stp.parse()
stp.setText("/tambahjadwal briefLomba 25 3 2017 10 30 10")
stp.parse()
stp.setText("/lihatjadwal")
stp.parse()
stp.setText("/ubahjadwal briefLomba 30 4 2017 13 30 3")
stp.parse()
stp.setText("/lihatjadwal")
stp.parse()
stp.setText("/selesaijadwal briefLomba")
stp.parse()
stp.setText("/reportjadwal")
stp.parse()
stp.setText("/hapusjadwal briefLomba")
stp.parse()
stp.setText("/lihatjadwal")
stp.parse()
