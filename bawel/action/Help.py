from __future__ import unicode_literals

from bawel.action.Action import Action

class HelpAll(Action):
    def __init__(self):
        super().__init__()

    def act(self, state):
        S = """Halo kak, bingung si bawel bisa ngapain aja ?
si bawel bisa ngatur acara kakak dan ingetin kakaknya kalo udah 1 jam sebelumnya, untuk lebih keponya bisa dengan ketik '/jadwal'
bisa juga ngatur pengeluaran bos,  untuk lebih keponya ketik '/pengeluaran'
bisa juga baca foto pengeluaran yang kakak berikan dengan upload fotonyaa pas input pengeluaran hehe """
        return (state, S)

class HelpJadwal(Action):
    def __init__(self):
        super().__init__()

    def act(self, state):
        S = """Si bawel bisa bantu nambah atau ubah acara bisa ketik kek gini'si bawel tolong dong tambah/ubah jadwal pergi ke jogja tanggal 5 April jam 3:50 sore'
            bisa juga lihat acara yang ada dengan kaya gini 'si bawel kita mau lihat jadwal'
            lihat yang ikut acara siapa saja dengan gini 'si bawel aku mau report event namaevent'
            atau ikut acara pake 'si bawel mau nih ikut acara namajadwal oleh Kevin(nama kakak)'
            bisa juga ga jadi ikut acara 'si bawel aku gajadi ikut jadwal namajadwal oleh Kevin(nama kakak)'
            dan hapus acara 'si bawel kita mau hapus jadwal namajadwal' """

        return (state, S)

class HelpPengeluaran(Action):
    def __init__(self):
        super().__init__()

    def act(self, state):
        # TODO:
        S = """Si bawel bisa bantu nambah atau ubah pengeluaran bisa ketik kaya 'si bawel tolong dong tambah/ubah pengeluaran makan siang untuk acara pergi ke jogja sebesar 50000 oleh Kevin'
            bisa juga lihat acara yang ada dengan ketik 'si bawel kita mau lihat jadwal'
            atau lihat pembagian pengeluaran pake 'si bawel aku mau report pengeluaran pergi ke jogja(namapengeluaran)'
            dan hapus pengeluaran 'si bawel kita mau hapus pengeluaran pergi ke jakarta(namapengeluaran)' """

        return (state, "ntaran")

class HelpHabit(Action):
    def __init__(self):
        super().__init__()

    def act(self, state):
        S = """Bos mau nambah habit bos ketik '/tambahhabit namahabit jam menit hari'

bisa juga lihat habit bos dengan ketik '/lihathabit'

dan ubahhabit bos dengan ketik '/ubahhabit namahabit jam menit hari'

bos juga bisa hapus habit bos dengan ketik '/hapushabit namahabit' """

        return (state, S)
