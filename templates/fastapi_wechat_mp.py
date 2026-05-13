"""Minimal FastAPI webhook for WeChat Official Account passive replies.

Run:
    export WECHAT_MP_TOKEN='your-token'
    uvicorn templates.fastapi_wechat_mp:app --host 0.0.0.0 --port 8000
"""
from __future__ import annotations

import asyncio
import os

from fastapi import FastAPI, Request, Response

from wechat_mp_agent_kit.reply import success_response, text_reply
from wechat_mp_agent_kit.signature import verify_signature
from wechat_mp_agent_kit.xml import message_dedupe_key, parse_wechat_xml

TOKEN = os.environ.get("WECHAT_MP_TOKEN", "")
AI_TIMEOUT_SECONDS = float(os.environ.get("WECHAT_MP_AI_TIMEOUT", "2.5"))

app = FastAPI(title="WeChat Official Account Agent Webhook")
_seen: set[str] = set()


async def call_agent_fast(prompt: str, user_openid: str) -> str:
    """Replace this with your agent harness call.

    Keep this under ~2-3 seconds if you want to use passive replies directly.
    For slow work, enqueue a background job and return success/ack.
    """
    await asyncio.sleep(0)
    return f"收到：{prompt}"


def _verify_request(request: Request) -> bool:
    q = request.query_params
    return verify_signature(
        TOKEN,
        q.get("timestamp"),
        q.get("nonce"),
        q.get("signature"),
    )


@app.get("/wechat/mp/webhook")
async def verify(request: Request) -> Response:
    if not _verify_request(request):
        return Response("invalid signature", status_code=403)
    return Response(request.query_params.get("echostr", ""), media_type="text/plain")


@app.post("/wechat/mp/webhook")
async def webhook(request: Request) -> Response:
    if not _verify_request(request):
        return Response("invalid signature", status_code=403)

    raw = await request.body()
    msg = parse_wechat_xml(raw)
    key = message_dedupe_key(msg)
    if key in _seen:
        return Response(success_response(), media_type="text/plain")
    _seen.add(key)

    if msg.get("MsgType") != "text":
        return Response(
            text_reply(msg.get("FromUserName", ""), msg.get("ToUserName", ""), "第一版先支持文字消息。"),
            media_type="application/xml",
        )

    try:
        answer = await asyncio.wait_for(
            call_agent_fast(msg.get("Content", ""), msg.get("FromUserName", "")),
            timeout=AI_TIMEOUT_SECONDS,
        )
    except asyncio.TimeoutError:
        # Queue background work here if desired. Returning success suppresses
        # WeChat retries and avoids the user-facing service-error prompt.
        return Response(success_response(), media_type="text/plain")

    return Response(
        text_reply(msg.get("FromUserName", ""), msg.get("ToUserName", ""), answer),
        media_type="application/xml",
    )
