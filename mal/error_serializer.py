from falcon import Request, Response
from falcon.errors import HTTPError


def serializer(request: Request, response: Response, exception: HTTPError) -> None:
    response.body = exception.to_json()
    response.content_type = "application/json"
