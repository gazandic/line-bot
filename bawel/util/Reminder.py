from __future__ import unicode_literals

import datetime
import time
import threading
import sys

from datetime import datetime as dt
from sched import scheduler
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, URITemplateAction, PostbackTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

class Reminder:
    def __init__(self, scheduler, linebot):
        self.scheduler = scheduler
        self.linebot = linebot

    def add(self, eid, tm, job, args):
        self.scheduler.enterabs(tm, 1, job, (eid, *args))
        print(self.scheduler.queue)
        def worker_main():
            newsched = self.scheduler
            newsched.run()
        worker_thread = threading.Thread(target=worker_main)
        worker_thread.start()

    def push(self, text, stickerid, lineid):
        self.linebot.push_message(
            lineid, [
                TextSendMessage(text=text),
                StickerSendMessage(
                    package_id=3,
                    sticker_id=stickerid)
            ])

    def remove(self, eid):
        try:
            ev = list(filter(lambda ev: ev.argument[0] == eid, self.scheduler.queue))[0]
            job, args = ev.action, ev.argument
            self.scheduler.cancel(ev)
            print(args)
            return (job, args)
        except:
            print(sys.exc_info())

    def modify(self, eid, tm):
        job, args = self.remove(eid)
        self.add(eid, tm, job, args[1:])

def job(eid, text, lineid, stickerid=180):
    reminder.push(text, stickerid, lineid)
