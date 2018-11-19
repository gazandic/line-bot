from typing import Union

from linebot.models import TextMessage

from bawel.responses.StickerResponse import StickerResponse
from bawel.responses.TextResponse import TextResponse


def map_to_line_response(resp: Union[TextResponse, StickerResponse]):
    if isinstance(resp, TextResponse):
        return TextMessage(text=resp.text)
    return None
    # elif isinstance(resp, StickerResponse):
    #     return StickerSendMessage()
