from json import dumps
from mal.spiders import AnimeSpiders


class AnimeResource:
    def on_get(self, request, response, mal_id, mal_request):
        spiders = AnimeSpiders()
        data = getattr(spiders, mal_request)(mal_id)
        response.content_type = "application/json"
        response.body = dumps(data)

    def on_get_2(self, request, response, mal_id, mal_request, page_number):
        spiders = AnimeSpiders()
        data = getattr(spiders, mal_request)(mal_id, page_number)
        response.content_type = "application/json"
        response.body = dumps(data)
