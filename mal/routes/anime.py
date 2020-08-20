from json import dumps
from falcon import Request, Response
from mal.spiders import AnimeSpiders


class AnimeResource:
    def on_get(self, request: Request, response: Response, mal_id: int, mal_request: str) -> None:
        spiders = AnimeSpiders(mal_id)
        data = getattr(spiders, mal_request)()
        response.content_type = "application/json"
        response.body = dumps(data)

    def on_get_2(self, request: Request, response: Response, **kwargs) -> None:
        spiders = AnimeSpiders(kwargs["mal_id"])
        data = getattr(spiders, kwargs["mal_request"])(kwargs["page_number"])
        response.content_type = "application/json"
        response.body = dumps(data)
