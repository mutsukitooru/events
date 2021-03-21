import aiohttp
import asyncio
import feedparser

from collections import deque
from datetime import timedelta
from typing import Optional
from logging import getLogger

logger = getLogger("rss-watcher")


class Watcher:
    def __init__(self, rss_feed: str, check_every: timedelta, callback):
        self.feed = rss_feed
        self.interval = check_every.total_seconds()
        self.cb = callback
        self.session: Optional[aiohttp.ClientSession] = None
        self._task: Optional[asyncio.Future] = None
        self._previous_results = deque(maxlen=10)

    async def start(self):
        self.session = aiohttp.ClientSession()
        self._task = asyncio.create_task(self._watch())

    async def _watch(self):
        while True:
            await asyncio.sleep(self.interval)
            await self._get_rss()

    async def _get_rss(self):
        async with self.session.get(self.feed) as resp:
            if resp.status >= 400:
                logger.info(f"got unexpected response: {resp.status!r}, full response: {resp!r}")
                return

            rss = await resp.read()
            await self._parse(rss)

    async def _parse(self, rss: bytes):
        feed = feedparser.parse(rss)
        entries = feed['entries']

        for entry in entries:
            if entry['id'] in self._previous_results:
                break  # we've cleared all the new feeds

            await self.cb(entry)
            self._previous_results.append(entry['id'])
