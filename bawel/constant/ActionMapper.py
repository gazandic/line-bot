from bawel.action.Help import HelpAll, HelpJadwal, HelpHabit, HelpPengeluaran
from bawel.action.Jadwal import TambahJadwal, LihatJadwal, UbahJadwal, HapusJadwal, ReportJadwal, IkutJadwal, \
    TakIkutJadwal
from bawel.action.Pengeluaran import TambahPengeluaran, LihatPengeluaran, UbahPengeluaran, HapusPengeluaran, \
    ReportPengeluaran, ImageTambahPengeluaran
from bawel.constant.StateConstant import STATE_HELP_ALL, STATE_HELP_JADWAL, STATE_HELP_HABIT, STATE_HELP_PENGELUARAN, \
    STATE_ADD_JADWAL, STATE_SHOW_JADWAL, STATE_MODIFY_JADWAL, STATE_DELETE_JADWAL, STATE_REPORT_JADWAL, \
    STATE_ADD_PENGELUARAN, STATE_SHOW_PENGELUARAN, STATE_MODIFY_PENGELUARAN, STATE_DELETE_PENGELUARAN, \
    STATE_REPORT_PENGELUARAN, STATE_IKUT_JADWAL, STATE_GAIKUT_JADWAL, STATE_IMAGE_ADD_PENGELUARAN

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
    STATE_REPORT_PENGELUARAN: ReportPengeluaran,
    STATE_IKUT_JADWAL: IkutJadwal,
    STATE_GAIKUT_JADWAL: TakIkutJadwal,
    STATE_IMAGE_ADD_PENGELUARAN: ImageTambahPengeluaran
}