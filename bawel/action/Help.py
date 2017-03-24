from __future__ import unicode_literals

from bawel.action.Action import Action

class HelpAll(Action):
    def __init__(self):
        super().__init__()

    def act(self, state, bossname):
        print(
"""Halo bos, bingung sekretaris bos {0} bisa ngapain aja ?
sekretaris bos {0} bisa ngatur acara bos dengan ketik '/acara' dan ingetin bos
bisa juga ngatur habit bos dengan ketik '/habit' dan bakal berisikin bos tiap bos ngelakuin itu
bisa juga ngatur pengeluaran bos dengan ketik '/pengeluaran'
bisa juga baca foto yang bos berikan dengan upload foto bapak hehe """
.format(bossname)
        )

        return state

class HelpJadwal(Action):
    def __init__(self):
        super().__init__()

    def act(self, state, bossname):
        print(
"""Bos kalo bos {0} mau nambah acara bisa ketik '/tambahjadwal namajadwal hari bulan tahun jam menit'
bisa juga lihat schedule bos dengan ketik '/lihatjadwal'
bos juga bisa reschedule bos dengan ketik '/ubahjadwal namajadwal hari bulan tahun jam menit'
dan hapus schedule bos dengan ketik '/selesaijadwal namajadwal'
dan hapus schedule bos dengan ketik '/reportjadwal'
dan hapus schedule bos dengan ketik '/hapusjadwal namajadwal'
"""
.format(bossname)
        )

        return state

class HelpPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, state, bossname):
        print("ntaran")
        return state

class HelpHabit(Action):
    def __init__(self):
        super().__init__()

    def act(self, state, bossname):
        print(
"""Bos {0} mau nambah habit bos ketik '/tambahhabit namahabit jam menit hari'
bisa juga lihat habit bos dengan ketik '/lihathabit'
dan ubahhabit bos dengan ketik '/ubahhabit namahabit jam menit hari'
bos juga bisa hapus habit bos dengan ketik '/hapushabit namahabit' """
.format(bossname)
        )

        return state
