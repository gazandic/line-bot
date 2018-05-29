from typing import Union

from bawel.responses.TextResponse import TextResponse


def map_to_tg_response(resp: Union[TextResponse]):
    if isinstance(resp, TextResponse):
        return resp.text
    return None
    # elif isinstance(resp, StickerResponse):
    #     return StickerSendMessage()
