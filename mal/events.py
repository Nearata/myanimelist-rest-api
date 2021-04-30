from fastapi import FastAPI
from httpx import Client

from .scrapers.anime_scrapers import AnimeScrapers
from .utils.cache import CacheUtil


def startup(app: FastAPI) -> None:
    app.state.session = Client()
    app.state.cache = CacheUtil()
    app.state.animescrapers = AnimeScrapers(app.state.session)


def shutdown(app: FastAPI) -> None:
    app.state.session.close()
