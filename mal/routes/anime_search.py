from json import dumps
from mal.spiders.anime.search import search


class AnimeSearch:
    def on_get(self, request, response):
        if "type" in request.params:
            anime_type = request.params["type"]

        if "score" in request.params:
            anime_score = request.params["score"]

        if "status" in request.params:
            anime_status = request.params["status"]

        if "producer" in request.params:
            anime_producer = request.params["producer"]

        if "rated" in request.params:
            anime_rated = request.params["rated"]

        if "start_month" in request.params:
            anime_s_month = request.params["start_month"]

        if "start_day" in request.params:
            anime_s_day = request.params["start_day"]

        if "start_year" in request.params:
            anime_s_year = request.params["start_year"]

        if "end_month" in request.params:
            anime_e_month = request.params["end_month"]

        if "end_day" in request.params:
            anime_e_day = request.params["end_day"]

        if "end_year" in request.params:
            anime_e_year = request.params["end_year"]

        results = search(
            request.params["query"],
            anime_type,
            anime_score,
            anime_status,
            anime_producer,
            anime_rated,
            anime_s_month,
            anime_s_day,
            anime_s_year,
            anime_e_month,
            anime_e_day,
            anime_e_year
        )
        response.content_type = "application/json"
        response.body = dumps(results)
