from json import dumps
from mal.spiders.anime.top import get_top


class AnimeTop:
    def on_get(self, request, response, ttype, page_number):
        data = get_top(ttype, page_number)
        response.content_type = "application/json"
        response.body = dumps(data)
