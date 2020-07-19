from json import dumps
from mal.spiders.anime.search import Search


class AnimeSearch:
    def on_get(self, request, response):
        search = Search(
            query=request.get_param("query"),
            type=request.get_param("type", default=0),
            score=request.get_param("score", default=0),
            status=request.get_param("status", default=0),
            producer=request.get_param("producer", default=0),
            rated=request.get_param("rated", default=0),
            start_day=request.get_param("start_day", default=0),
            start_month=request.get_param("start_month", default=0),
            start_year=request.get_param("start_year", default=0),
            end_day=request.get_param("end_day", default=0),
            end_month=request.get_param("end_month", default=0),
            end_year=request.get_param("end_year", default=0),
            genres=request.get_param("genres", default=0),
            genres_exclude=request.get_param("genres_exclude", default=0),
            columns=request.get_param("columns", default=0)
        )
        response.content_type = "application/json"
        response.body = dumps(search.get())
