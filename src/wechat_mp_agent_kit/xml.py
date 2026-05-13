"""Safe-ish XML parsing helpers for WeChat Official Account messages."""
from __future__ import annotations

from typing import Any

try:
    from defusedxml import ElementTree as ET
except Exception:  # pragma: no cover - dependency is declared, fallback for copy-paste use
    import xml.etree.ElementTree as ET  # type: ignore


def _strip_ns(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


def parse_wechat_xml(data: bytes | str) -> dict[str, str]:
    """Parse a WeChat XML message into a flat dict of text fields.

    The common Official Account message payloads are shallow. For nested nodes
    (e.g. ScanCodeInfo) this helper returns the direct child text only; extend
    it if you need rich event parsing.
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    root = ET.fromstring(data)
    out: dict[str, str] = {}
    for child in list(root):
        key = _strip_ns(child.tag)
        out[key] = child.text or ""
    return out


def message_dedupe_key(msg: dict[str, Any]) -> str:
    """Return a retry-dedupe key.

    Official guidance: use MsgId for ordinary messages; use FromUserName +
    CreateTime for events that do not carry MsgId.
    """
    if msg.get("MsgId"):
        return f"msg:{msg['MsgId']}"
    return f"event:{msg.get('FromUserName','')}:{msg.get('CreateTime','')}"
