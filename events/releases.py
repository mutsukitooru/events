from dataclasses import dataclass
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from .render import RenderEngine
from .settings import API_KEY


@dataclass(frozen=True)
class ReleaseEntity:
    title: str
    episode: int
    rating: int
    description: str
    tags: list


def _clean_desc(desc: str):
    soup = BeautifulSoup(desc, 'lxml')
    maybe_clean = soup.text.replace("\n", " ").replace("\t", " ")
    while "  " in maybe_clean:
        maybe_clean = maybe_clean.replace("  ", " ")
    return maybe_clean


class ReleaseEventHandler:
    def __init__(self, session: ClientSession, renderer: RenderEngine):
        self.renderer = renderer
        self.session = session

    async def __call__(self, payload: dict):
        title = payload['crunchyroll_seriestitle']
        episode_title = payload['crunchyroll_episodetitle']
        episode_num = int(payload['crunchyroll_episodenumber'])
        desc = _clean_desc(payload['summary'])

