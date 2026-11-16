import asyncio
import logging
import os
import sys

from bots.demo_bot import run as run_demo
from bots.official_bot import run as run_official

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    mode = os.getenv("BOT_MODE", "demo").lower()
    logging.info("Starting NEXTGEN AI Telegram Bot (%s mode) | Dev: Shohjahon Abdullayev", mode)
    if mode == "official":
        asyncio.run(run_official())
    else:
        asyncio.run(run_demo())
