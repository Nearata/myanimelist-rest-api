from datetime import datetime
from re import search
from json import dumps, loads
from falcon import Request, Response
from mal.cache import Cache


class CacheMiddleware:
    def __init__(self) -> None:
        self.cache = Cache("anime", "documents")

    def process_request(self, request: Request, response: Response) -> None:
        if request.path.startswith("/anime/search") or request.path.startswith("/anime/top/"):
            return

        resource, mal_id, mal_request = self.__get_params(request.path)

        if not resource == "anime":
            return

        cache_response = self.cache.find_cache(mal_id, mal_request)

        if mal_request not in cache_response:
            return

        response.complete = True
        response.set_header("Content-Type", "application/json")
        response.body = dumps(cache_response)

    def process_response(self, request: Request, response: Response, res: object, request_succeeded: bool) -> None:
        if not request_succeeded or request.path.startswith("/anime/search") or request.path.startswith("/anime/top/"):
            return

        resource, mal_id, mal_request = self.__get_params(request.path)

        if not resource == "anime":
            return

        cache_response = self.cache.find_cache(mal_id, mal_request)

        if mal_request not in cache_response:
            data = loads(response.body)
            data.update(cache_response)
            data.update({"created_at": datetime.utcnow()})
            self.cache.insert_cache(data)

    def __get_params(self, request_path: str) -> tuple:
        match = search(r"/(?P<resource>.*)/(?P<mal_id>.*)/(?P<mal_request>.*)", request_path)
        return (match.group("resource"), match.group("mal_id"), match.group("mal_request"))
