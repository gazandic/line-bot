from __future__ import unicode_literals

from telegram import Bot


class Telegram:

    def __init__(self, token):
        self.bot = Bot(token=token)

    def add(self, event, message=None):
        # def decorator(func):
        #     @self.handler.add(event, message)
        #     def wrapper(event):
        #         if LineMiddleware.check_message(self.api, event):
        #             func(event)
        #     return func
        # return decorator
        pass

    def reply(self, event, messages):
        # self.api.reply_message(event.reply_token, messages)
        pass

    def send(self, chat_id, text, sticker=None, location=None):
        self.bot.sendMessage(chat_id=chat_id, text=text)
