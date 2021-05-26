from fastapi import FastAPI
from httpx import AsyncClient

from .config import HTTP2
from .scrapers import AnimeScrapers


async def startup(app: FastAPI) -> None:
    app.state.session = AsyncClient(http2=HTTP2)
    app.state.animescrapers = AnimeScrapers(app.state.session)


async def shutdown(app: FastAPI) -> None:
    await app.state.session.aclose()
