from __future__ import unicode_literals

import datetime
import time

from datetime import datetime as dt

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

def reminder_job(line_bot_api, message="Morning honey :))) Howdy?", interval=0):
    line_bot_api.push_message("U39166bd6890a58b174c92aed76983241", TextMessage(text=message))

    if interval != 0:
        t = dt.combine(dt.now() + interval, daily_time)
        scheduler.enterabs(time.mktime(t.timetuple()), 1, job, (line_bot_api, message,))
