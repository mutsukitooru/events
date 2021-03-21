from dataclasses import dataclass


@dataclass(frozen=True)
class NewsEntity:
    title: str
    summary: str
    time: str
    author: str
    brief: str
    icon: str


