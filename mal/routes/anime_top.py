from json import dumps
from mal.spiders.anime import AnimeSpiders


class AnimeTop:
    def on_get(self, request, response, ttype, page_number):
        spiders = AnimeSpiders()
        data = getattr(spiders, "top")(ttype, page_number)
        response.content_type = "application/json"
        response.body = dumps(data)
