from re import match
from falcon import HTTPBadRequest
from falcon import HTTPMissingParam
from falcon import HTTPInvalidParam
from falcon import HTTPNotFound
from falcon import Request
from falcon import Response
from mal.scrapers import AnimeScrapers


class ValidateRouteMiddleware:
    route_invalid_incomplete = "The route is invalid or incomplete."
    double_check_docs = "Please double check the documentation."
    wiki_base_url = "https://github.com/Nearata/myanimelist-rest-api/wiki"

    def process_request(self, request: Request, response: Response) -> None:
        anime_route = r"\/anime"

        if match(anime_route, request.path):
            self.__validate_anime_route(anime_route, request)
        else:
            raise HTTPBadRequest(
                title=self.route_invalid_incomplete,
                description=self.double_check_docs,
                href=self.wiki_base_url
            )

    def __validate_anime_route(self, anime_route: str, request: Request) -> None:
        top_route = anime_route + r"\/top"
        if match(top_route, request.path):
            self.__validate_top_route(top_route, request.path)
            return

        search_route = anime_route + r"\/search"
        if match(search_route, request.path):
            self.__validate_search_route(request)
            return

        anime_regex = anime_route + r"\/(\d{1,5})\/"
        anime_routes = f"({'|'.join([i for i in dir(AnimeScrapers) if not i.startswith('__')])})"
        pattern = anime_regex + anime_routes

        if not match(pattern, request.path):
            raise HTTPBadRequest(
                title=self.route_invalid_incomplete,
                description=self.double_check_docs
            )

        if match(anime_regex + r"(reviews|episodes)", request.path) and not match(anime_regex + r"(reviews|episodes)\/(\d+)", request.path):
            raise HTTPMissingParam("page_number")

    def __validate_search_route(self, request: Request) -> None:
        if not match(r"\/anime\b\/search\b", request.path):
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

    def __validate_top_route(self, top_route: str, path: str) -> None:
        if not match(r"\/anime\b\/top\b", path):
            raise HTTPBadRequest(
                title=self.route_invalid_incomplete,
                description=self.double_check_docs
            )

        regex = top_route + r"\b\/(all|airing|upcoming|tv|movie|ova|ona|special|bypopularity|favorite)\b"
        if not match(regex, path):
            raise HTTPBadRequest(
                title=self.route_invalid_incomplete,
                description=self.double_check_docs,
                href=f"{self.wiki_base_url}/Top-Route"
            )

        page_number_regex = regex + r"\/(\d+)"
        if not match(page_number_regex, path):
            raise HTTPMissingParam("page_number")
