__all__ = ["checkInputWaktu", "checkInputTanggal", "ImageProcessor", "JsonToQuery", "PengeluaranDetector", "Reminder", "RequestParser", "Sticker", "TextProcessor"]

def checkInputWaktu(jam, menit):
    return time(int(jam)-1, int(menit))

def checkInputTanggal(hari, bulan, tahun, jam, menit):
    d = date(int(tahun), int(bulan), int(hari))
    t = checkInputWaktu(jam, menit)
    dt = datetime.combine(d,t)
    return dt
