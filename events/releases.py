from dataclasses import dataclass


@dataclass(frozen=True)
class NewsEntity:
    title: str
    episode: int
    rating: int
    description: str
    tags: list
