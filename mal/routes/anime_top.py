from json import dumps
from mal.spiders.anime import AnimeSpiders


class AnimeTop:
    def on_get(self, request, response, _type, page_number):
        spiders = AnimeSpiders()
        data = spiders.top(_type, page_number)
        response.content_type = "application/json"
        response.body = dumps(data)
