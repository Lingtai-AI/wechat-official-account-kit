"""Customer-service message helpers for slow async replies (phase 2)."""
from __future__ import annotations

import httpx

CUSTOM_SEND_URL = "https://api.weixin.qq.com/cgi-bin/message/custom/send"


async def send_text(access_token: str, openid: str, content: str) -> dict:
    """Send a customer-service text message.

    This only works when the Official Account has the relevant permission and
    the user is within the allowed customer-service interaction window.
    """
    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.post(
            CUSTOM_SEND_URL,
            params={"access_token": access_token},
            json={
                "touser": openid,
                "msgtype": "text",
                "text": {"content": content},
            },
        )
        resp.raise_for_status()
        data = resp.json()
    if data.get("errcode") not in (0, None):
        raise RuntimeError(f"WeChat customer-service send failed: {data}")
    return data
