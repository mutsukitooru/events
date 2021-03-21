import aiohttp
import asyncio

from .render import RenderEngine
from .rss_watcher import Watcher
from .settings import RSS_CONFIGURE, CHECK_EVERY
from .news import NewsEventHandler
from .releases import ReleaseEventHandler


async def start_watching(render_engine: RenderEngine):
    async with aiohttp.ClientSession() as sess:
        news = NewsEventHandler(sess, render_engine)
        release = ReleaseEventHandler(sess, render_engine)

        news_watcher = Watcher(
            RSS_CONFIGURE['news'],
            CHECK_EVERY,
            news,
        )

        release_watcher = Watcher(
            RSS_CONFIGURE['release'],
            CHECK_EVERY,
            release
        )

        t1 = news_watcher.start()
        t2 = release_watcher.start()

        await asyncio.gather(t1, t2)

