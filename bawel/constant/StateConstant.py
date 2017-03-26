from bawel.action.Help import *
from bawel.action.Jadwal import *
from bawel.action.Pengeluaran import *

STATE_UNKNOWN = -1
STATE_NOTHING = 0
STATE_ASK_USERNAME = 1
STATE_ASK_USERLOCATION = 2
STATE_INPUT_USERNAME = 3
STATE_INPUT_USERLOCATION = 4
STATE_HELP_ALL = 5
STATE_HELP_JADWAL = 6
STATE_HELP_HABIT = 7
STATE_HELP_PENGELUARAN = 8
STATE_ADD_JADWAL = 9
STATE_SHOW_JADWAL = 10
STATE_MODIFY_JADWAL = 11
STATE_DELETE_JADWAL = 12
STATE_REPORT_JADWAL = 13
STATE_ADD_PENGELUARAN = 14
STATE_SHOW_PENGELUARAN = 15
STATE_MODIFY_PENGELUARAN = 16
STATE_DELETE_PENGELUARAN = 17
STATE_REPORT_PENGELUARAN = 18
# STATE_EVENT_MENU =
# STATE_HABIT_MENU =
# STATE_USER_MENU =
# STATE_EVENT_ADD =
# STATE_EVENT_UPDATE =
# STATE_EVENT_HABIT =
# STATE_EVENT_DELETE =
# STATE_EVENT_ADD_NOABOUT =
# STATE_EVENT_ADD_NODATETIME =
# STATE_EVENT_ADD_NODATET =
# STATE_EVENT_ADD_NOTIME =
# STATE_EVENT_ADD_NOURGENCY =
# STATE_HABIT_ADD =
# STATE_HABIT_UPDATE =
# STATE_HABIT_SEARCH =
# STATE_HABIT_DELETE =

ACTION_MAPPER = {
    STATE_HELP_ALL: HelpAll,
    STATE_HELP_JADWAL: HelpJadwal,
    STATE_HELP_HABIT: HelpHabit,
    STATE_HELP_PENGELUARAN: HelpPengeluaran,
    STATE_ADD_JADWAL: TambahJadwal,
    STATE_SHOW_JADWAL: LihatJadwal,
    STATE_MODIFY_JADWAL: UbahJadwal,
    STATE_DELETE_JADWAL: HapusJadwal,
    # STATE_: SelesaiJadwal,
    STATE_REPORT_JADWAL: ReportJadwal,
    # '/tambahhabit': self.tambahhabitCommand,
    # '/lihathabit': self.lihathabitCommand,
    # '/ubahhabit': self.ubahhabitCommand,
    # '/hapushabit': self.hapushabitCommand,
    # '/selesaihabit': self.selesaihabitCommand,
    # '/reporthabit': self.reporthabitCommand,
    STATE_ADD_PENGELUARAN: TambahPengeluaran,
    STATE_SHOW_PENGELUARAN: LihatPengeluaran,
    STATE_MODIFY_PENGELUARAN: UbahPengeluaran,
    STATE_DELETE_PENGELUARAN: HapusPengeluaran,
    # '/selesaipengeluaran': self.selesaipengeluaranCommand,
    STATE_REPORT_PENGELUARAN: ReportPengeluaran
}

REQUEST_STATE = {
    '/help': STATE_HELP_ALL,
    '/jadwal': STATE_HELP_JADWAL,
    '/habit': STATE_HELP_HABIT,
    '/pengeluaran': STATE_HELP_PENGELUARAN,
    '/tambahjadwal': STATE_ADD_JADWAL,
    '/lihatjadwal': STATE_SHOW_JADWAL,
    '/ubahjadwal': STATE_MODIFY_JADWAL,
    '/hapusjadwal': STATE_DELETE_JADWAL,
    # '/selesaijadwal': #,
    '/reportjadwal': STATE_REPORT_JADWAL,
    # '/tambahhabit': #,
    # '/lihathabit': #,
    # '/ubahhabit': #,
    # '/hapushabit': #,
    # '/selesaihabit': #,
    # '/reporthabit': #,
    '/tambahpengeluaran': STATE_ADD_PENGELUARAN,
    '/lihatpengeluaran': STATE_SHOW_PENGELUARAN,
    '/ubahpengeluaran': STATE_MODIFY_PENGELUARAN,
    '/hapuspengeluaran': STATE_DELETE_PENGELUARAN,
    # '/selesaipengeluaran': #,
    '/reportpengeluaran': STATE_REPORT_PENGELUARAN
}
