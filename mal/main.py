from functools import partial

from fastapi import FastAPI

from .config import DEBUG
from .events import shutdown, startup
from .middlewares.cache import CacheMiddleware
from .middlewares.disabled_routes import DisabledRoutesMiddleware
from .middlewares.mal_checker import MalCheckerMiddleware
from .middlewares.require_json import RequireJsonMiddleware
from .routes.anime import router as anime_router
from .routes.search import router as search_router
from .routes.top import router as top_router


def create_app() -> FastAPI:
    app = FastAPI(
        debug=DEBUG,
        title="MyAnimeList REST API (Unofficial)",
        docs_url=None,
        redoc_url=None,
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

    app.include_router(anime_router, prefix="/anime", tags=["anime"])
    app.include_router(search_router, prefix="/search", tags=["search"])
    app.include_router(top_router, prefix="/top", tags=["top"])

    return app
