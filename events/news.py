from dataclasses import dataclass
from aiohttp import ClientSession

from .render import RenderEngine
from .settings import API_KEY


@dataclass(frozen=True)
class NewsEntity:
    title: str
    summary: str
    time: str
    author: str
    brief: str
    icon: str


class NewsEventHandler:
    def __init__(self, session: ClientSession, renderer: RenderEngine):
        self.renderer = renderer
        self.session = session

    async def __call__(self, payload: dict):
        ...

