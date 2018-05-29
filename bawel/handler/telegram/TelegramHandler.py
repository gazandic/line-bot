import os, sys, logging

from flask import request
from telegram import Update

from bawel.handler.core.ContentHandler import ContentHandler
from bawel.state.StateManager import StateManager

from bawel.responses.mapper.Telegram import map_to_tg_response

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
        if text is None:
            return

        user_state = StateManager.fetch(chat_id)
        updated_state, responses = ContentHandler.handle_text(user_state.state, text, None)

        if responses is not None:
            pure_responses = filter(lambda x: x is not None, map(map_to_tg_response, responses))
            for el in pure_responses:
                client.send(chat_id, el)

        StateManager.update(chat_id, updated_state)
