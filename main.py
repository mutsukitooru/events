import asyncio

from events import start_watching, RenderEngine

engine = RenderEngine("./templates")

if __name__ == '__main__':
    asyncio.run(start_watching(engine))
