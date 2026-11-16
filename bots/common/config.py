"""Bot configuration. Two bots, two tokens, two service keys — never interchangeable."""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class BotConfig:
    mode: str                 # "demo" | "official"
    token: str
    service_key: str
    api_base_url: str
    admin_ids: tuple[int, ...] = (8592332908,)
    api_prefix: str = "/api/v1/telegram/service"
    request_timeout: float = 30.0

    @property
    def is_demo(self) -> bool:
        return self.mode == "demo"

    @property
    def title(self) -> str:
        return "NEXTGEN AI DEMO" if self.is_demo else "NEXTGEN AI"

    def is_admin(self, uid: int) -> bool:
        return uid in self.admin_ids


def load_config(mode: str) -> BotConfig:
    mode = mode.strip().lower()
    if mode not in ("demo", "official"):
        raise SystemExit("mode must be 'demo' or 'official'")
    if mode == "demo":
        token = os.getenv("TELEGRAM_DEMO_BOT_TOKEN", "")
        key = os.getenv("BOT_SERVICE_KEY_DEMO", "demo-service-key-2026")
    else:
        token = os.getenv("TELEGRAM_OFFICIAL_BOT_TOKEN", "")
        key = os.getenv("BOT_SERVICE_KEY_OFFICIAL", "official-service-key-2026")
    if not token:
        raise SystemExit(f"TELEGRAM_{mode.upper()}_BOT_TOKEN is not set")
    if not key:
        raise SystemExit(f"BOT_SERVICE_KEY_{mode.upper()} is not set")
    raw_admins = os.getenv("ADMIN_TELEGRAM_IDS", "8592332908")
    admin_ids: list[int] = []
    for item in raw_admins.split(","):
        item = item.strip()
        if item.isdigit():
            admin_ids.append(int(item))
    return BotConfig(mode=mode, token=token, service_key=key,
                     api_base_url=os.getenv("BOT_API_BASE_URL", "http://127.0.0.1:8000").rstrip("/"),
                     admin_ids=tuple(admin_ids))
