import random

from linebot.models import MessageEvent, LocationMessage, ImageMessage, SourceGroup, TextSendMessage, SourceUser, \
    SourceRoom, JoinEvent, PostbackEvent, TextMessage, TemplateSendMessage, LocationSendMessage, StickerSendMessage

from bawel.util.Sticker import randomPrivate


class LineMiddleware:
    def check_message(self, line_bot_api, event) -> bool:
        profile = line_bot_api.get_profile(event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text='Maaf, kak ' + profile.display_name +
                    ' bot ini fokus pada asisten grup, undang bawel ke grup kak'
                ),
                StickerSendMessage(
                    package_id=3,
                    sticker_id=random.choice(randomPrivate))
            ]
        )

        return False
        

    def is_private_message(self, event):
        return isinstance(event.source, SourceUser)