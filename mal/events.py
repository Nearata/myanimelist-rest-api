from fastapi import FastAPI
from requests import Session

from .config import CACHE
from .database import Cache, db
from .scrapers.anime_scrapers import AnimeScrapers
from .utils.cache import CacheUtil


def startup(app: FastAPI) -> None:
    app.state.session = Session()
    app.state.cache = CacheUtil()
    app.state.animescrapers = AnimeScrapers(app.state.session)
    if CACHE:
        db.connect()
        db.create_tables([Cache])


def shutdown(app: FastAPI) -> None:
    app.state.session.close()
    if CACHE:
        db.close()
