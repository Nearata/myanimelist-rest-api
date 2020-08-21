from falcon import API
from mal.middleware import CheckUrlMiddleware
from mal.middleware import RequireJSONMiddleware
from mal.middleware import CacheMiddleware
from mal.middleware import ValidateRouteMiddleware
from mal.routes import AnimeResource
from mal.routes import AnimeSearch
from mal.routes import AnimeTop


def create_app() -> API:
    anime_route = AnimeResource()
    anime_search = AnimeSearch()
    anime_top = AnimeTop()

    api = API(middleware=[
        RequireJSONMiddleware(),
        ValidateRouteMiddleware(),
        CacheMiddleware(),
        CheckUrlMiddleware()
    ])

    api.req_options.strip_url_path_trailing_slash = True

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
        anime_search
    )
    api.add_route(
        "/top/anime/{_type}/{page_number:int}",
        anime_top
    )

    return api
