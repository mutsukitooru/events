import os
import random
import base64
import asyncio

from string import ascii_letters, punctuation
from logging import getLogger
from typing import Optional, Union

from jinja2 import Environment, FileSystemLoader
from selenium.webdriver import Firefox, FirefoxOptions as Options

from .news import NewsEntity
from .releases import ReleaseEntity

CHARACTERS = list(ascii_letters) + list(punctuation)
TARGET_URL = f"file://{os.getcwd()}/serve/{{}}.html"
CSS_PATH = "../templates.css"

logger = getLogger("render-engine")


def random_name():
    random.shuffle(CHARACTERS)
    file_name = "".join(CHARACTERS[:11])
    new = str(base64.urlsafe_b64encode(file_name.encode("utf-8")), "utf-8").replace("=", "")
    return new


def _get_driver(path: str) -> Firefox:
    options = Options()
    options.headless = True
    return Firefox(executable_path=path, options=options)


class RenderEngine:
    def __init__(self, path: str, driver_path: str):
        self.env = Environment(
            loader=FileSystemLoader(path)
        )

        self.loop = asyncio.get_event_loop()

        self._driver_path = driver_path
        self._driver: Optional[Firefox] = None
        logger.info("driver created")

        self._driver_event = asyncio.Lock()
        self._watcher: Optional[asyncio.Future] = None

        if not os.path.exists("./out"):
            os.mkdir("./out")

    async def start(self):
        self._driver = await self.loop.run_in_executor(
            None,
            _get_driver,
            self._driver_path,
        )
        self._watcher = self.loop.create_task(self._reload_driver())

    def shutdown(self):
        self._watcher.cancel()
        self._driver.close()

    async def _reload_driver(self):
        while True:
            await asyncio.sleep(60 * 60)  # 1 hour

            async with self._driver_event:
                logger.info("reloading driver")
                self._driver.close()
                self._driver = await self.loop.run_in_executor(
                    None,
                    _get_driver,
                    self._driver_path,
                )
                logger.info("driver reload successful")

    def _render(self, type_: str):
        url = TARGET_URL.format(type_)
        logger.info(f"rendering image on url: {url!r}")
        self._driver.get(url)

        out = f"{os.getcwd()}/out/{type_}/{random_name()}.png"
        target = self._driver.find_element_by_id("rendered")
        target.screenshot(out)
        logger.info(f"created image {out!r}")

    async def render(self, type_: str, payload: Union[NewsEntity, ReleaseEntity]):
        logger.info(f"rendering html {type_!r}")
        template = self.env.get_template(f"{type_}.html")
        out = template.render(**payload.__dict__)
        logger.info(f"rendered html {type_!r}")

        if not os.path.exists(f"./serve"):
            logger.info("no serving directory, making on instead")
            os.mkdir(f"./serve")

        with open(f"./serve/{type_}.html", "w+", encoding="UTF-8") as file:
            file.write(out)
        logger.info("written to serving file")

        if not os.path.exists(f"./out/{type_}"):
            logger.info("no output directory, making on instead")
            os.mkdir(f"./out/{type_}")

        async with self._driver_event:
            logger.info("acquired render lock, clear to render")
            await self.loop.run_in_executor(
                None,
                self._render,
                type_,
            )


