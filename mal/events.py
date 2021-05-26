from fastapi import FastAPI
from httpx import AsyncClient

from .config import HTTP2
from .scrapers import AnimeScrapers, TopScrapers
from .utils import SoupUtil


async def startup(app: FastAPI) -> None:
    app.state.session = AsyncClient(http2=HTTP2)

    soup_util = SoupUtil(app.state.session)
    app.state.anime_scrapers = AnimeScrapers(soup_util)
    app.state.top_scrapers = TopScrapers(soup_util)


async def shutdown(app: FastAPI) -> None:
    await app.state.session.aclose()
