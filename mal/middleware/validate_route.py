from re import match
from falcon import HTTPBadRequest
from falcon import HTTPMissingParam
from falcon import HTTPInvalidParam
from falcon import HTTPNotFound
from mal.spiders import AnimeSpiders


class ValidateRoute:
    route_invalid_incomplete = "The route is invalid or incomplete."
    double_check_docs = "Please double check the documentation."
    wiki_base_url = "https://github.com/Nearata/myanimelist-rest-api/wiki"

    def process_request(self, request, response):
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

    def __validate_anime_route(self, anime_route, request):
        anime_regex = anime_route + r"\/(\d{1,5})\/"
        anime_routes = f"({'|'.join([i for i in dir(AnimeSpiders) if not i.startswith('__')])})"
        pattern = anime_regex + anime_routes
        if not match(f"{pattern}$", request.path):
            raise HTTPBadRequest(
                title=self.route_invalid_incomplete,
                description=self.double_check_docs
            )
        if match(anime_regex + r"(reviews|episodes)", request.path) and not match(anime_regex + r"(reviews|episodes)\/(\d+)", request.path):
            raise HTTPMissingParam("page_number")

    def __validate_search_route(self, search_route, request):
        search_anime = r"\/anime"
        if match(search_route + search_anime, request.path):
            if request.get_param("query", required=True):
                if len(request.get_param("query")) < 3:
                    raise HTTPInvalidParam(
                        msg="Must be minimum 3 letters.",
                        param_name="query"
                    )
            else:
                raise HTTPInvalidParam(
                    msg="It cannot be empty.",
                    param_name="query"
                )
        else:
            raise HTTPNotFound(
                title="Route not found.",
                description=self.double_check_docs,
                href=f"{self.wiki_base_url}/Search-Route"
            )

    def __validate_top_route(self, top_route, request):
        top_anime = r"\/anime"
        if match(top_route + top_anime, request.path):
            regex = top_route + top_anime + r"\/(all|airing|upcoming|tv|ova|special|bypopularity|favorite)"
            if match(regex, request.path):
                if not match(regex + r"\/(\d+)", request.path):
                    raise HTTPMissingParam("page_number")
            else:
                raise HTTPBadRequest(
                    title=self.route_invalid_incomplete,
                    description=self.double_check_docs,
                    href=f"{self.wiki_base_url}/Top-Route"
                )
        else:
            raise HTTPNotFound(
                title="Route not found.",
                description=self.double_check_docs,
                href=f"{self.wiki_base_url}/Top-Route"
            )
