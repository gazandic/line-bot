from datetime import date, time, datetime, timedelta

__all__ = ["check_time_input", "check_date_input", "JsonToQuery", "ExpenseDetector.py", "Reminder", "RequestParser",
           "Sticker", "TextProcessor", "CheckMoney"]


def check_time_input(jam, menit):
    return time(int(jam), int(menit))


def check_date_input(hari, bulan, tahun, jam, menit):
    d = date(int(tahun), int(bulan), int(hari))
    t = check_time_input(jam, menit)
    dt = datetime.combine(d, t)
    td = timedelta(hours=-8)
    dt = dt + td
    # print(dt)
    return dt
