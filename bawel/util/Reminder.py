from __future__ import unicode_literals

import datetime
import time

from datetime import datetime as dt
from sched import scheduler

class Reminder:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.scheduler.run()

    def add(self, eid, tm, job):
        self.scheduler.enterabs(tm, 1, job, (eid,))

    def remove(self, eid):
        ev = list(filter(lambda ev: ev.argument[0] == eid, self.scheduler.queue))[0]
        self.scheduler.cancel(ev)

    def modify(self, eid, tm):
        self.remove(eid)
        self.add(eid, tm)
