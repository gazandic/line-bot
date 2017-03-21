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

    def setText(self, text):
        self.text = text

    def setLineid(self, lineid):
        self.lineid = lineid

    def parse(self):
        us = User(self.lineid,"undefined","undefined",UserConstant.STATE_UNKNOWN_USERNAME)
        user = us.searchOne({"lineid":self.lineid})
        if not user:
            return us.create()
        us.set(user)
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
        us.setName(self.text)
        us.setState(UserConstant.STATE_UNKNOWN_USERLOCATION)
        us.update()

    def default(self):
        print("lol")

    def askLocation(self, us):
        bossName = str(us.getName())
        print("bos "+bossName+" ada di kota mana ?")
        us.setLocation(self.text)
        us.setState(UserConstant.STATE_KNOWN_USER)
        us.update()

    def chooseMenu(self, us):
        print(us.getName())
        bossName = str(us.getName())
        if self.text == "/help":
            print("Halo bos, bingung sekretaris bos "+bossName+" bisa ngapain aja ?")
            print("sekretaris bos "+bossName+" bisa ngatur acara bos dengan ketik '/acara' dan ingetin bos ")
            print("bisa juga ngatur habit bos dengan ketik '/habit' dan bakal berisikin bos tiap bos ngelakuin itu")
            print("bisa juga ngatur pengeluaran bos dengan ketik '/pengeluaran' ")
            print("bisa juga baca foto yang bos berikan dengan upload foto bapak hehe ")

        elif self.text == "/acara":
            print("Bos kalo bos "+bossName+" mau nambah acara bos ketik '/tambahjadwal namajadwal hari bulan tahun jam menit' ")
            print("bisa juga lihat schedule bos dengan ketik '/lihatjadwal'")
            print("bos juga bisa reschedule bos dengan ketik '/ubahjadwal namajadwal hari bulan tahun jam menit'")
            print("dan hapus schedule bos dengan ketik '/selesaijadwal namajadwal' ")
            print("dan hapus schedule bos dengan ketik '/reportjadwal' ")
            print("dan hapus schedule bos dengan ketik '/hapusjadwal namajadwal' ")

        elif self.text == "/habit":
            print("Bos "+bossName+" mau nambah habit bos ketik '/tambahhabit namahabit jam menit hari' ")
            print("bisa juga lihat habit bos dengan ketik '/lihathabit'")
            print("dan ubahhabit bos dengan ketik '/ubahhabit namahabit jam menit hari'")
            print("bos juga bisa hapus habit bos dengan ketik '/hapushabit namahabit' ")

        elif self.text == "/pengeluaran":
            print("ntaran")

        elif "/tambahjadwal" in self.text:
            self.tambahjadwal()

        elif "/lihatjadwal" == self.text:
            self.lihatjadwal()

        elif "/ubahjadwal" in self.text:
            self.ubahjadwal()

        elif "/hapusjadwal" in self.text:
            self.hapusjadwal()

        elif "/selesaijadwal" in self.text:
            self.selesaijadwal()

        elif "/reportjadwal" == self.text:
            self.reportjadwal()

        else:
            print("halo bos, sekretaris bos "+bossName+ " kurang paham, coba ketik /help ya bos :)")

    def tambahjadwal(self):
        s = self.text.split(" ")
        if (s[0] == '/tambahjadwal'):
            try:
                self.checkTambahJadwal(s)
                ev1 = Event(self.lineid,s[1],s[7],s[2],s[3],s[4],s[5],s[6],0)
                ev1.create()
            except ValueError:
                print ("format penulisan '/tambahjadwal namajadwal hari bulan tahun jam menit'")

    def selesaijadwal(self):
        s = self.text.split(" ")
        if (s[0] == '/selesaijadwal'):
            ev1 = Event(self.lineid,"lol",10,1,1,1,1,1,0)
            eve = ev1.searchOne({"lineid":self.lineid,"about":s[1]})
            ev1.set(eve)
            ev1.setFulfilled(1)
            ev1.update()

    def ubahjadwal(self):
        s = self.text.split(" ")
        if (s[0] == '/ubahjadwal'):
            try:
                self.checkTambahJadwal(s)
                ev1 = Event(self.lineid,s[1],s[7],s[2],s[3],s[4],s[5],s[6],0)
                ev1.update()
            except ValueError:
                print ("format penulisan '/ubahjadwal namajadwal hari bulan tahun jam menit' , nama jadwal tidak dapat diubah")

    def reportjadwal(self):
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

    def hapusjadwal(self):
        s = self.text.split(" ")
        if (s[0] == '/hapusjadwal'):
            ev1 = Event(self.lineid,"lol",10,1,1,1,1,1,0)
            ev1.removeQuery({"lineid":self.lineid,"about":s[1]})

    def checkTambahJadwal(self, s):
        d = date(int(s[4]), int(s[3]), int(s[2]))
        t = time(int(s[5]), int(s[6]))

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
