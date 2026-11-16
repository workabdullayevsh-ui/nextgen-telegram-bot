"""Thin typed client for the backend service plane.

Every call carries the bot's own service key and mode. No organization id is ever
sent: the backend derives the tenant from the linked Telegram account.
"""
from __future__ import annotations

from typing import Any

import httpx

from bots.common.config import BotConfig


class BotAPIError(Exception):
    def __init__(self, code: str, message: str, status: int = 0):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status


class BackendClient:
    def __init__(self, cfg: BotConfig):
        self.cfg = cfg
        self._client = httpx.AsyncClient(
            base_url=cfg.api_base_url + cfg.api_prefix,
            headers={"X-Bot-Service-Key": cfg.service_key, "X-Bot-Mode": cfg.mode},
            timeout=cfg.request_timeout,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def _request(self, method: str, path: str, **kwargs) -> Any:
        try:
            resp = await self._client.request(method, path, **kwargs)
        except httpx.HTTPError as exc:
            raise BotAPIError("network", "Backend bilan aloqa yo'q. Keyinroq urinib ko'ring.") from exc
        if resp.status_code >= 400:
            try:
                err = resp.json().get("error", {})
            except ValueError:
                err = {}
            raise BotAPIError(err.get("code", "http_error"),
                              err.get("message", f"Xatolik ({resp.status_code})"),
                              resp.status_code)
        if "application/json" in resp.headers.get("content-type", ""):
            return resp.json()
        return resp.content

    # ---- session -------------------------------------------------------
    async def demo_session(self, telegram_user_id: int, username: str | None) -> dict:
        return await self._request("POST", "/demo-session",
                                   json={"telegram_user_id": telegram_user_id,
                                         "telegram_username": username})

    async def link(self, telegram_user_id: int, username: str | None, code: str) -> dict:
        return await self._request("POST", "/link", params={"code": code},
                                   json={"telegram_user_id": telegram_user_id,
                                         "telegram_username": username})

    async def me(self, telegram_user_id: int) -> dict:
        return await self._request("GET", "/me", params={"telegram_user_id": telegram_user_id})

    async def unlink(self, telegram_user_id: int) -> dict:
        return await self._request("POST", "/unlink",
                                   json={"telegram_user_id": telegram_user_id})

    # ---- data ----------------------------------------------------------
    async def dashboard(self, uid: int, period: str = "month") -> dict:
        return await self._request("GET", "/dashboard",
                                   params={"telegram_user_id": uid, "period": period})

    async def anomalies(self, uid: int, limit: int = 5) -> dict:
        return await self._request("GET", "/anomalies",
                                   params={"telegram_user_id": uid, "limit": limit})

    async def forecast(self, uid: int, horizon_days: int = 30) -> dict:
        return await self._request("GET", "/forecast",
                                   params={"telegram_user_id": uid, "horizon_days": horizon_days})

    async def chat(self, uid: int, question: str, language: str) -> dict:
        return await self._request("POST", "/chat",
                                   json={"telegram_user_id": uid, "question": question,
                                         "language": language})

    async def notifications(self, uid: int, limit: int = 10) -> dict:
        return await self._request("GET", "/notifications",
                                   params={"telegram_user_id": uid, "limit": limit})

    async def report(self, uid: int, kind: str = "dashboard", fmt: str = "pdf",
                     period: str = "month") -> dict:
        return await self._request("POST", "/report",
                                   params={"telegram_user_id": uid, "kind": kind,
                                           "fmt": fmt, "period": period})

    async def download_report(self, uid: int, report_id: str) -> bytes:
        return await self._request("GET", f"/report/{report_id}",
                                   params={"telegram_user_id": uid})

    async def upload(self, uid: int, filename: str, content: bytes,
                     content_type: str = "text/csv") -> dict:
        return await self._request("POST", "/upload",
                                   data={"telegram_user_id": str(uid)},
                                   files={"file": (filename, content, content_type)})

    async def set_language(self, uid: int, language: str) -> dict:
        return await self._request("POST", "/language",
                                   params={"telegram_user_id": uid, "language": language})

    async def toggle_alerts(self, uid: int) -> dict:
        return await self._request("POST", "/alerts", params={"telegram_user_id": uid})

    async def admin_stats(self, uid: int) -> dict:
        return await self._request("GET", "/admin-stats", params={"telegram_user_id": uid})
