"""NEXTGEN AI — DEMO bot (long polling).

Opens a session on the seeded DEMO organization automatically so that anyone can
try the product. It is read-only: no uploads, no access to real enterprises.
"""
from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bots.common.api import BackendClient
from bots.common.config import load_config
from bots.common.handlers import SessionCache, build_router

log = logging.getLogger("nextgen.bot.demo")


async def run() -> None:
    cfg = load_config("demo")
    api = BackendClient(cfg)
    bot = Bot(token=cfg.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(build_router(cfg, api, SessionCache()))
    log.info("DEMO bot starting (read-only, DEMO organization only)")
    try:
        await dp.start_polling(bot, allowed_updates=["message", "callback_query"])
    finally:
        await api.close()
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run())
