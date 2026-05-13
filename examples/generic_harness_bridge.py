"""Framework-neutral adapter interface for agent harnesses."""
from __future__ import annotations

from typing import Protocol


class AgentHarness(Protocol):
    async def ask(self, *, user_id: str, text: str, timeout_seconds: float) -> str: ...


async def reply_with_harness(harness: AgentHarness, incoming: dict[str, str], timeout_seconds: float = 2.5) -> str:
    return await harness.ask(
        user_id=incoming.get("FromUserName", ""),
        text=incoming.get("Content", ""),
        timeout_seconds=timeout_seconds,
    )
