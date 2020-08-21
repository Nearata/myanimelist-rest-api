from re import match
from falcon import HTTPBadRequest
from falcon import HTTPMissingParam
from falcon import HTTPInvalidParam
from falcon import HTTPNotFound
from falcon import Request
from falcon import Response
from mal.spiders import AnimeSpiders


class ValidateRouteMiddleware:
    route_invalid_incomplete = "The route is invalid or incomplete."
    double_check_docs = "Please double check the documentation."
    wiki_base_url = "https://github.com/Nearata/myanimelist-rest-api/wiki"

    def process_request(self, request: Request, response: Response) -> None:
        anime_route = r"\/(anime)"
        search_route = r"\/(search)"
        top_route = r"\/(top)"
        if match(anime_route, request.path):
            self.__validate_anime_route(anime_route, request)
        elif match(search_route, request.path):
            self.__validate_search_route(search_route, request)
        elif match(top_route, request.path):
            self.__validate_top_route(top_route, request)
        else:
            raise HTTPBadRequest(
                title=self.route_invalid_incomplete,
                description=self.double_check_docs,
                href=self.wiki_base_url
            )

    def __validate_anime_route(self, anime_route: str, request: Request) -> None:
        anime_regex = anime_route + r"\/(\d{1,5})\/"
        anime_routes = f"({'|'.join([i for i in dir(AnimeSpiders) if not i.startswith('__')])})"
        pattern = anime_regex + anime_routes
        if not match(pattern, request.path):
            raise HTTPBadRequest(
                title=self.route_invalid_incomplete,
                description=self.double_check_docs
            )

        if match(anime_regex + r"(reviews|episodes)", request.path) and not match(anime_regex + r"(reviews|episodes)\/(\d+)", request.path):
            raise HTTPMissingParam("page_number")

    def __validate_search_route(self, search_route: str, request: Request) -> None:
        search_anime = r"\/anime"
        if not match(search_route + search_anime, request.path):
            raise HTTPNotFound(
                title="Route not found.",
                description=self.double_check_docs,
                href=f"{self.wiki_base_url}/Search-Route"
            )

        if not request.get_param("query", required=True):
            raise HTTPInvalidParam(
                msg="It cannot be empty.",
                param_name="query"
            )

        if len(request.get_param("query")) < 3:
            raise HTTPInvalidParam(
                msg="Must be minimum 3 letters.",
                param_name="query"
            )

    def __validate_top_route(self, top_route: str, request: Request) -> None:
        top_anime = r"\/anime"
        if not match(top_route + top_anime, request.path):
            raise HTTPNotFound(
                title="Route not found.",
                description=self.double_check_docs,
                href=f"{self.wiki_base_url}/Top-Route"
            )

        regex = top_route + top_anime + r"\/(all|airing|upcoming|tv|ova|special|bypopularity|favorite)"
        if not match(regex, request.path):
            raise HTTPBadRequest(
                title=self.route_invalid_incomplete,
                description=self.double_check_docs,
                href=f"{self.wiki_base_url}/Top-Route"
            )

        if not match(regex + r"\/(\d+)", request.path):
            raise HTTPMissingParam("page_number")
