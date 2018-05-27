from __future__ import unicode_literals

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    TextSendMessage,
    StickerSendMessage, LocationSendMessage
)

from bawel.client.ChatClient import ChatClient
from bawel.handler.line.LineMiddleware import LineMiddleware


class Line(ChatClient):

    def __init__(self, channel_secret, channel_access_token):
        self.api = LineBotApi(channel_access_token)
        self.handler = WebhookHandler(channel_secret)

    def textMessage(self, text):
        pass

    def stickerMessage(self, stickerId):
        pass

    def imageMessage(self, imageFile):
        pass

    def add(self, event, message=None):
        def decorator(func):
            @self.handler.add(event, message)
            def wrapper(event):
                if LineMiddleware.check_message(self.api, event):
                    func(event)
            return func
        return decorator

    def reply(self, event, messages):
        self.api.reply_message(event.reply_token, messages)

    def send(self, id, text, sticker=None, location=None):
        msg = [TextSendMessage(text=text)]
        if location is not None:
            msg.append(LocationSendMessage(
                latitude=location['lat'],
                longitude=location['lng']
            ))
        if sticker is not None:
            msg.append(StickerSendMessage(package_id=3, sticker_id=sticker))

        self.api.push_message(id, msg)
