import os, sys, logging

from flask import request
from telegram import Update

from bawel.client.Telegram import Telegram

bot_name = "Bawel"

# get bot_token from your environment variable
bot_token = os.getenv('TELEGRAM_TOKEN', '')
if bot_token is None:
    print('Specify TELEGRAM_TOKEN as environment variable.')
    sys.exit(1)

client = Telegram(bot_token)


def create_updater():
    # retrieve the message in JSON and then transform it to Telegram object
    return Update.de_json(request.get_json(force=True), client.bot)

def set_webhook(url: str) -> str:
    s = client.bot.setWebhook(url)
    if s:
        logging.info("{} WebHook Setup OK!".format(bot_name))
    else:
        logging.info("{} WebHook Setup Failed!".format(bot_name))

class TelegramHandler:
    @staticmethod
    def handle_text(chat_id: str, text: str):
        # client.
        client.send(chat_id, text)