"""Small access_token cache helper for phase-2 active APIs."""
from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path

import httpx

TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"


@dataclass
class AccessTokenCache:
    appid: str
    secret: str
    cache_path: Path
    skew_seconds: int = 300

    def get(self) -> str:
        cached = self._read()
        now = int(time.time())
        if cached and cached.get("access_token") and cached.get("expires_at", 0) > now + self.skew_seconds:
            return str(cached["access_token"])
        token, expires_in = self._fetch()
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(json.dumps({
            "access_token": token,
            "expires_at": now + int(expires_in),
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        return token

    def _read(self) -> dict | None:
        try:
            return json.loads(self.cache_path.read_text(encoding="utf-8"))
        except Exception:
            return None

    def _fetch(self) -> tuple[str, int]:
        resp = httpx.get(TOKEN_URL, params={
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.secret,
        }, timeout=15.0)
        resp.raise_for_status()
        data = resp.json()
        if data.get("errcode"):
            raise RuntimeError(f"WeChat access_token error: {data}")
        return data["access_token"], int(data.get("expires_in", 7200))
