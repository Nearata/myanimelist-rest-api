from json import dumps
from mal.spiders.anime.search import search


class AnimeSearch:
    def on_get(self, request, response):
        results = search(
            request.params["query"],
            request.get_param("type", default=0),
            request.get_param("score", default=0),
            request.get_param("status", default=0),
            request.get_param("producer", default=0),
            request.get_param("rated", default=0),
            request.get_param("start_day", default=0),
            request.get_param("start_month", default=0),
            request.get_param("start_year", default=0),
            request.get_param("end_day", default=0),
            request.get_param("end_month", default=0),
            request.get_param("end_year", default=0)
        )
        response.content_type = "application/json"
        response.body = dumps(results)
