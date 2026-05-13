"""Passive reply XML builders."""
from __future__ import annotations

import time


def _cdata(text: str) -> str:
    """Wrap text in CDATA, safely splitting embedded ]]> sequences."""
    return "<![CDATA[" + str(text).replace("]]>", "]]]]><![CDATA[>") + "]]>"


def text_reply(to_user: str, from_user: str, content: str, create_time: int | None = None) -> str:
    """Build a passive text reply XML body.

    Args:
        to_user: incoming FromUserName (user OpenID)
        from_user: incoming ToUserName (public account ID)
        content: text visible to the user
        create_time: unix timestamp; defaults to now
    """
    ts = int(create_time or time.time())
    return (
        "<xml>"
        f"<ToUserName>{_cdata(to_user)}</ToUserName>"
        f"<FromUserName>{_cdata(from_user)}</FromUserName>"
        f"<CreateTime>{ts}</CreateTime>"
        f"<MsgType>{_cdata('text')}</MsgType>"
        f"<Content>{_cdata(content)}</Content>"
        "</xml>"
    )


def image_reply(to_user: str, from_user: str, media_id: str, create_time: int | None = None) -> str:
    ts = int(create_time or time.time())
    return (
        "<xml>"
        f"<ToUserName>{_cdata(to_user)}</ToUserName>"
        f"<FromUserName>{_cdata(from_user)}</FromUserName>"
        f"<CreateTime>{ts}</CreateTime>"
        f"<MsgType>{_cdata('image')}</MsgType>"
        "<Image>"
        f"<MediaId>{_cdata(media_id)}</MediaId>"
        "</Image>"
        "</xml>"
    )


def success_response() -> str:
    """Tell WeChat the event was accepted but no passive message is returned."""
    return "success"
