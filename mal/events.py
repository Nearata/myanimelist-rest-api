from fastapi import FastAPI
from httpx import AsyncClient

from .config import HTTP2
from .scrapers import AnimeScrapers
from .utils import SoupUtil


async def startup(app: FastAPI) -> None:
    app.state.session = AsyncClient(http2=HTTP2)

    soup_util = SoupUtil(app.state.session)
    app.state.animescrapers = AnimeScrapers(soup_util)


async def shutdown(app: FastAPI) -> None:
    await app.state.session.aclose()
