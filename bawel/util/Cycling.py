from __future__ import unicode_literals

import sys
import time as t
import sched

from datetime import datetime, date, time, timedelta
from bawel.model.Event import Event
from bawel.util.Reminder import Reminder


class Cycling(object):
    def __init__(self, reminder):
        self.reminder = reminder

    def process(self):
        def job(eid, text, lineid, location=None, stickerid=180):
            self.reminder.push(text, stickerid, lineid, location)

        eventManager = Event()
        start = datetime.today() + timedelta(days=-1)
        end = datetime.today() + timedelta(days=2)
        events = eventManager.search({"datetime": {"$gte": start, "$lt": end}})
        for event in events:
            if event["datetime"] > (datetime.now() + timedelta(hours=7)):
                location = None
                if event.get("loc"):
                    location = event["loc"]
                date = str(datetime.strptime(str(event["datetime"]), "%Y-%m-%d %H:%M:%S").strftime(
                    "tanggal %d/%m jam %H:%M WIB"))
                dta = event["datetime"] + timedelta(hours=-8)
                namajadwal1 = event["about"].replace("_", " ")
                reminding = "jangan lupa " + date + " ada jadwal " + namajadwal1
                eid = event["about"] + event["lineid"]
                self.reminder.add(eid, dta, job, (reminding, event["lineid"], location,))
        print(self.reminder.scheduler.queue)
        # return 0
