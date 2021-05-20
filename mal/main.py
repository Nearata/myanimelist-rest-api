from functools import partial

from fastapi import FastAPI

from .config import DEBUG
from .events import shutdown, startup
from .exceptions import ValidationException, validation_exception_handler
from .middlewares.disabled_routes import DisabledRoutesMiddleware
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
        openapi_url=None,
        swagger_ui_oauth2_redirect_url=None,
    )

    app.add_middleware(DisabledRoutesMiddleware)
    app.add_middleware(RequireJsonMiddleware)

    app.add_exception_handler(ValidationException, validation_exception_handler)

    app.add_event_handler("startup", partial(startup, app))
    app.add_event_handler("shutdown", partial(shutdown, app))

    app.include_router(anime_router)
    app.include_router(search_router)
    app.include_router(top_router)

    return app
