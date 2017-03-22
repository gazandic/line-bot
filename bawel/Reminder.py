from __future__ import unicode_literals

class Reminder:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.scheduler.run()

# daily_time = datetime.time(23,22)
# first_time = dt.combine(dt.now(), daily_time)

# time, priority, callable, *args
# scheduler.enterabs(time.mktime(first_time.timetuple()), 1, job, (line_bot_api, "Morning honey :))) Howdy?",))
