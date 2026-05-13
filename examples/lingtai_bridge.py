"""Example shape for bridging Official Account messages into LingTai.

This file is intentionally a sketch: the exact bridge depends on how the host
wants to wake an agent (internal mailbox drop, HTTP endpoint, queue, etc.).
"""
from __future__ import annotations


def build_lingtai_prompt(incoming: dict[str, str]) -> str:
    return (
        "A WeChat Official Account user sent a message. "
        "Reply concisely in the same language.\n\n"
        f"openid: {incoming.get('FromUserName')}\n"
        f"message: {incoming.get('Content','')}"
    )


async def call_lingtai_agent(incoming: dict[str, str]) -> str:
    """Replace with your LingTai wake/mail/tool invocation."""
    prompt = build_lingtai_prompt(incoming)
    # Example options:
    # - write a mailbox JSON event to a LingTai agent inbox
    # - call a local HTTP bridge
    # - enqueue for a resident orchestrator
    return f"[LingTai bridge placeholder] {prompt[:120]}"
