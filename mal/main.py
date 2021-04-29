from functools import partial

from fastapi import FastAPI
from requests import Session

from mal.config import CACHE
from mal.database import Database
from mal.middlewares import (CacheMiddleware, DisabledRoutesMiddleware,
                             MalCheckerMiddleware, RequireJsonMiddleware)
from mal.routes import anime_router, search_router, top_router


def startup(app: FastAPI) -> None:
    app.state.session = Session()
    if CACHE:
        Database.connect()

def shutdown(app: FastAPI) -> None:
    app.state.session.close()
    if CACHE:
        Database.close()

def create_app() -> FastAPI:
    app = FastAPI(
        title="MyAnimeList REST API (Unofficial)",
        docs_url=None,
        redoc_url=None
    )

    cache = CacheMiddleware()
    mal_checker = MalCheckerMiddleware()
    require_json = RequireJsonMiddleware()
    disabled_routes = DisabledRoutesMiddleware()

    app.middleware("http")(mal_checker)
    app.middleware("http")(cache)
    app.middleware("http")(disabled_routes)
    app.middleware("http")(require_json)

    app.add_event_handler("startup", partial(startup, app))
    app.add_event_handler("shutdown", partial(shutdown, app))

    app.include_router(
        anime_router,
        prefix="/anime",
        tags=["anime"]
    )
    app.include_router(
        search_router,
        prefix="/search",
        tags=["search"]
    )
    app.include_router(
        top_router,
        prefix="/top",
        tags=["top"]
    )

    return app
