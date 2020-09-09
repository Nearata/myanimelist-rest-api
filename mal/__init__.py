from falcon import API
from mal.middleware import *
from mal.routes import AnimeRoute
from mal.error_serializer import ErrorSerializer


def create_app() -> API:
    anime_route = AnimeRoute()

    api = API(middleware=[
        RequireJsonMiddleware(),
        ValidateRouteMiddleware(),
        # CacheMiddleware(),
        MalCheckerMiddleware()
    ])

    api.req_options.strip_url_path_trailing_slash = True
    error_serializer = ErrorSerializer()
    api.set_error_serializer(error_serializer)

    api.add_route(
        "/anime/{mal_id:int}/{mal_request}",
        anime_route
    )
    api.add_route(
        "/anime/{mal_id:int}/{mal_request}/{page_number:int}",
        anime_route,
        suffix="2"
    )
    api.add_route(
        "/anime/search",
        anime_route,
        suffix="search"
    )
    api.add_route(
        "/anime/top/{_type}/{page_number:int}",
        anime_route,
        suffix="top"
    )

    return api
