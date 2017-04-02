import requests, os

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

def searchLoc(query):
    token = os.getenv('GOOGLE_MAP_TOKEN', None)
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    params = {"query": query, "key": token}
    res = requests.get(base_url, params=params).json()
    try:
        geo = res['results'][0]['geometry']['location']
        return "{0},{1}".format(geo['lat'], geo['lng'])
    except (KeyError, IndexError):
        return None
