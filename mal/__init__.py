from falcon import API
from mal.middleware import CacheMiddleware
from mal.middleware import RequireJsonMiddleware
from mal.middleware import MalChecker
from mal.middleware import ValidateRouteMiddleware
from mal.routes import AnimeRoute
from mal.error_serializer import ErrorSerializer


def create_app() -> API:
    anime_route = AnimeRoute()

    api = API(middleware=[
        RequireJsonMiddleware(),
        ValidateRouteMiddleware(),
        CacheMiddleware(),
        MalChecker()
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
        "/search/anime",
        anime_route,
        suffix="search"
    )
    api.add_route(
        "/top/anime/{_type}/{page_number:int}",
        anime_route,
        suffix="top"
    )

    return api
