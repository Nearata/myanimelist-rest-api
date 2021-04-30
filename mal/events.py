from fastapi import FastAPI
from requests import Session

from mal.config import CACHE
from mal.database import Cache, db
from mal.utils import CacheUtil


def startup(app: FastAPI) -> None:
    app.state.session = Session()
    app.state.cache = CacheUtil()
    if CACHE:
        db.connect()
        db.create_tables([Cache])


def shutdown(app: FastAPI) -> None:
    app.state.session.close()
    if CACHE:
        db.close()
