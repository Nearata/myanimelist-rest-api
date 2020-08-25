from falcon import Request, Response
from falcon.errors import HTTPError


class ErrorSerializer:
    def __call__(self, request: Request, response: Response, exception: HTTPError) -> None:
        response.body = exception.to_json()
        response.content_type = "application/json"
