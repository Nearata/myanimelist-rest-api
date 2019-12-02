from re import match
from falcon import HTTPBadRequest
from falcon import HTTPMissingParam
from falcon import HTTPInvalidParam
from falcon import HTTPNotFound
from mal.spiders import AnimeSpiders


class ValidateRoute:
    def process_request(self, request, response):
        anime_route = r"\/(anime)"
        search_route = r"\/(search)"
        top_route = r"\/(top)"
        if match(anime_route, request.path):
            anime_regex = anime_route + r"\/(\d{1,5})\/"
            anime_routes = f"({'|'.join([i for i in dir(AnimeSpiders) if not i.startswith('__')])})"
            pattern = anime_regex + anime_routes
            if not match(pattern, request.path):
                raise HTTPBadRequest(
                    title="The route is invalid or incomplete.",
                    description="Please double check the documentation."
                )
            if match(anime_regex + r"(reviews|episodes)", request.path):
                if not match(anime_regex + r"(reviews|episodes)\/(\d+)", request.path):
                    raise HTTPMissingParam("page_number")
        elif match(search_route, request.path):
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
                    description="Please double check the documentation.",
                    href="https://github.com/Nearata/myanimelist-rest-api/wiki/Search-Route"
                )
        elif match(top_route, request.path):
            top_anime = r"\/anime"
            if match(top_route + top_anime, request.path):
                regex = top_route + top_anime + r"\/(all|airing|upcoming|tv|ova|special|bypopularity|favorite)"
                if match(regex, request.path):
                    if not match(regex + r"\/(\d+)", request.path):
                        raise HTTPMissingParam("page_number")
                else:
                    raise HTTPBadRequest(
                        title="The route is invalid or incomplete.",
                        description="Please double check the documentation.",
                        href="https://github.com/Nearata/myanimelist-rest-api/wiki/Top-Route"
                    )
            else:
                raise HTTPNotFound(
                    title="Route not found.",
                    description="Please double check the documentation.",
                    href="https://github.com/Nearata/myanimelist-rest-api/wiki/Top-Route"
                )
        else:
            raise HTTPBadRequest(
                title="The route is invalid or incomplete.",
                description="Please double check the documentation.",
                href="https://github.com/Nearata/myanimelist-rest-api/wiki"
            )
