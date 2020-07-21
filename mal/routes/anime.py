from json import dumps
from mal.spiders import AnimeSpiders


class AnimeResource:
    def on_get(self, request, response, mal_id, mal_request):
        spiders = AnimeSpiders(mal_id)
        data = getattr(spiders, mal_request)()
        response.content_type = "application/json"
        response.body = dumps(data)

    def on_get_2(self, request, response, **kwargs):
        spiders = AnimeSpiders(kwargs['mal_id'])
        data = getattr(spiders, kwargs['mal_request'])(kwargs['page_number'])
        response.content_type = "application/json"
        response.body = dumps(data)
