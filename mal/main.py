from fastapi import FastAPI

from mal.middlewares import CacheMiddleware
from mal.middlewares import DisabledRoutesMiddleware
from mal.middlewares import MalCheckerMiddleware
from mal.middlewares import RequireJsonMiddleware
from mal.routes import anime_router
from mal.routes import search_router
from mal.routes import top_router


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
