from json import dumps
from falcon import Request, Response
from mal.spiders.anime import AnimeSpiders


class AnimeTop:
    def on_get(self, request: Request, response: Response, _type: str, page_number: int) -> None:
        spiders = AnimeSpiders()
        data = spiders.top(_type, page_number)
        response.content_type = "application/json"
        response.body = dumps(data)
