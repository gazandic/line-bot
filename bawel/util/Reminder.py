from __future__ import unicode_literals

import datetime
import time

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
        self.scheduler.run()

    def add(self, eid, tm, job, args):
        self.scheduler.enterabs(tm, 1, job, (eid, *args))
        print(self.scheduler.queue)

    def push(self, text, stickerid, lineid):
        self.linebot.push_message(
            lineid, [
                TextSendMessage(text=text),
                StickerSendMessage(
                    package_id=3,
                    sticker_id=stickerid)
            ])

    def remove(self, eid):
        ev = list(filter(lambda ev: ev.argument[0] == eid, self.scheduler.queue))[0]
        self.scheduler.cancel(ev)

    def modify(self, eid, tm):
        self.remove(eid)
        self.add(eid, tm)
