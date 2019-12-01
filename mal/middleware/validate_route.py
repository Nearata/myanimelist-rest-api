from re import match
from falcon import HTTPBadRequest
from falcon import HTTPMissingParam
from falcon import HTTPInvalidParam
from mal.spiders import AnimeSpiders


class ValidateRoute:
    def process_request(self, request, response):
        if match(r"\/(anime)", request.path):
            anime_regex = r"\/(anime)\/(\d{1,5})\/"
            anime_routes = f"({'|'.join([i for i in dir(AnimeSpiders) if not i.startswith('__')])})"
            pattern = anime_regex + anime_routes
            if not match(pattern, request.path):
                raise HTTPBadRequest(
                    title="The route is invalid or incomplete",
                    description="Please double check the documentation."
                )
            if match(anime_regex + r"(reviews|episodes)", request.path):
                if not match(anime_regex + r"(reviews|episodes)\/(\d+)", request.path):
                    raise HTTPMissingParam("page_number")
        elif match(r"\/(search\/anime)", request.path):
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
        elif match(r"\/(top\/anime)\/(all|airing|upcoming|tv|ova|special|bypopularity|favorite)\/(\d+)", request.path):
            pass
        else:
            raise HTTPBadRequest(
                title="The route is invalid or incomplete",
                description="Please double check the documentation."
            )
