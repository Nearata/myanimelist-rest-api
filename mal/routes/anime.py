from json import dumps
from falcon import Request, Response
from mal.scrapers import AnimeScrapers
from mal.anime import Search


class AnimeRoute:
    content_type = "application/json"

    def on_get(self, request: Request, response: Response, mal_id: int, mal_request: str) -> None:
        scrapers = AnimeScrapers(mal_id)
        data = getattr(scrapers, mal_request)()
        response.content_type = self.content_type
        response.body = dumps(data)

    def on_get_2(self, request: Request, response: Response, **kwargs) -> None:
        scrapers = AnimeScrapers(kwargs["mal_id"])
        data = getattr(scrapers, kwargs["mal_request"])(kwargs["page_number"])
        response.content_type = self.content_type
        response.body = dumps(data)

    def on_get_search(self, request: Request, response: Response) -> None:
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
        response.content_type = self.content_type
        response.body = dumps(search())

    def on_get_top(self, request: Request, response: Response, _type: str, page_number: int) -> None:
        scrapers = AnimeScrapers()
        data = scrapers.top(_type, page_number)
        response.content_type = self.content_type
        response.body = dumps(data)
