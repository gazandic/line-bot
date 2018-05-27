from __future__ import unicode_literals

import sys
import threading
import time


def worker_once(reminder):
    reminder.scheduler.run()


def worker_repeated(reminder, callback, args):
    worker_once(reminder)
    callback(*args)


class Reminder:
    def __init__(self, scheduler, linebot):
        self.scheduler = scheduler
        self.linebot = linebot

    def add_repeated(self, eid, tm, job, interval, args):
        self.scheduler.enterabs(tm, 1, job, (eid, *args))
        next_time = tm + interval
        tm = time.mktime(tm.timetuple())
        next_time = time.mktime(next_time.timetuple())

        worker_thread = threading.Thread(target=worker_repeated,
                                         kwargs={
                                             'reminder': self, 'callback': self.add_repeated,
                                             'args': (eid, tm, job, interval, args)
                                         })
        worker_thread.start()

    def add(self, eid, tm, job, args):
        tm = time.mktime(tm.timetuple())
        self.scheduler.enterabs(tm, 1, job, (eid, *args))

        worker_thread = threading.Thread(target=worker_once,
                                         kwargs={'reminder': self})
        worker_thread.start()

    def push(self, text, stickerid, lineid, location=None):
        self.linebot.push_message(lineid, text, stickerid, location)

    def remove(self, eid):
        try:
            ev = list(filter(lambda ev: ev.argument[0] == eid, self.scheduler.queue))[0]
            job, args = ev.action, ev.argument
            self.scheduler.cancel(ev)
            print(args)
            return job, args
        except:
            print(sys.exc_info())

    def modify(self, eid, tm):
        job, args = self.remove(eid)
        self.add(eid, tm, job, args[1:])
