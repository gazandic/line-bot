from datetime import date, time, datetime, timedelta
__all__ = ["checkInputWaktu", "checkInputTanggal", "ImageProcessor", "JsonToQuery", "PengeluaranDetector", "Reminder", "RequestParser", "Sticker", "TextProcessor", "CheckMoney"]

def checkInputWaktu(jam, menit):
    return time(int(jam), int(menit))

def checkInputTanggal(hari, bulan, tahun, jam, menit):
    d = date(int(tahun), int(bulan), int(hari))
    t = checkInputWaktu(jam, menit)
    dt = datetime.combine(d,t)
    td = timedelta(hours=-8)
    dt = dt + td
    print(dt)
    return (dt)
