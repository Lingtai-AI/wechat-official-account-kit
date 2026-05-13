#!/usr/bin/env python3
"""Replay a sample WeChat text message to a local webhook.

This is for local smoke tests only. It computes a valid signature for the
chosen token/timestamp/nonce.
"""
from __future__ import annotations

import argparse
import time

import httpx

from wechat_mp_agent_kit.signature import make_signature

SAMPLE = """<xml>
<ToUserName><![CDATA[gh_demo]]></ToUserName>
<FromUserName><![CDATA[o_demo_user]]></FromUserName>
<CreateTime>{ts}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{content}]]></Content>
<MsgId>1234567890123456</MsgId>
</xml>"""


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--url", default="http://127.0.0.1:8000/wechat/mp/webhook")
    p.add_argument("--token", required=True)
    p.add_argument("--content", default="hello")
    args = p.parse_args()
    ts = str(int(time.time()))
    nonce = "demo"
    sig = make_signature(args.token, ts, nonce)
    resp = httpx.post(
        args.url,
        params={"signature": sig, "timestamp": ts, "nonce": nonce},
        content=SAMPLE.format(ts=ts, content=args.content).encode("utf-8"),
        headers={"Content-Type": "application/xml"},
        timeout=10.0,
    )
    print(resp.status_code)
    print(resp.text)


if __name__ == "__main__":
    main()
