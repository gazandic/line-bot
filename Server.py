from __future__ import unicode_literals

import json
import logging
import traceback
from argparse import ArgumentParser

from flask import Flask, request, abort, jsonify
from linebot.exceptions import InvalidSignatureError

from bawel.handler.telegram.TelegramHandler import TelegramHandler, set_webhook, create_updater
from bawel.handler.line.LineHandler import handle
from bawel.util.FileUtil import make_static_tmp_dir

# gmaps = GoogleMaps(token_google)
# jadwaler = sched.scheduler(time.time, time.sleep)
# reminder = Reminder(jadwaler, lineClient)

# cycling = Cycling(reminder)
# cycling.process()


app = Flask(__name__, static_url_path='', static_folder='bawel/static')


@app.route("/line", methods=['POST'])
def callback_line():
    # get X-Line-Signature header value
    signature = request.headers.get('X-Line-Signature')
    if signature is None:
        response = jsonify(dict(error='X-Line-Signature not found'))
        response.status_code = 400
        return response

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@app.route("/telegram", methods=['POST'])
def callback_telegram():
    update = create_updater()
    message = update.message

    try:
        chat_id = "TG"+message.chat.id
        text = message.text

        if text is not None:
            TelegramHandler.handle_text(chat_id, text)

        join = message.new_chat_members
        if len(join) > 0:
            TelegramHandler.handle_join(chat_id)
    except AttributeError as e:
        logging.error("Access attribute error:\n{json}".format(json=json.dumps(update.to_json())))
        traceback.print_exc()

    return 'OK'


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    # create tmp dir for download content
    make_static_tmp_dir()
    # jadwaler.run()

    set_webhook(request.host_url+'/telegram')
    app.run(debug=options.debug, port=options.port)
