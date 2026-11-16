"""Single entry point: `python -m bots.run demo` or `python -m bots.run official`.

Each mode runs as its own process with its own token and service key — the two bots
are never combined in one runtime.
"""
from __future__ import annotations

import asyncio
import logging
import sys


def main() -> None:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s %(message)s")
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "demo":
        from bots.demo_bot import run
    elif mode == "official":
        from bots.official_bot import run
    else:
        raise SystemExit("usage: python -m bots.run [demo|official]")
    try:
        asyncio.run(run())
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    main()
