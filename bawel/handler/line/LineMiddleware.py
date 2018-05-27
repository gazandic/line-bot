import random

from linebot.models import TextSendMessage, SourceUser, \
    StickerSendMessage

from bawel.util.Sticker import line_sticker_nums


class LineMiddleware:
    @staticmethod
    def check_message(line_bot_api, event) -> bool:
        profile = line_bot_api.get_profile(event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text='Maaf, kak ' + profile.display_name +
                         ' bot ini fokus pada asisten grup, undang bawel ke grup kak'
                ),
                StickerSendMessage(
                    package_id=3,
                    sticker_id=random.choice(line_sticker_nums))
            ]
        )

        return False

    @staticmethod
    def is_private_message(event) -> bool:
        return isinstance(event.source, SourceUser)
