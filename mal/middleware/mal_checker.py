from http import HTTPStatus
from falcon import Request, Response, HTTPNotFound, HTTPError
from requests import Session
from requests.exceptions import ReadTimeout
from mal.utils import RequestsUtil


class MalCheckerMiddleware:
    def process_request(self, request: Request, response: Response) -> None:
        with Session() as s:
            try:
                req_response = s.head(f"https://myanimelist.net{request.path}", timeout=15, headers=RequestsUtil.HEADERS)
                req_status_code = req_response.status_code
            except ReadTimeout:
                http_status = HTTPStatus(504)
                status_code = getattr(http_status, "value")
                phrase = getattr(http_status, "phrase")
                raise HTTPError(
                    f"{status_code} {phrase}",
                    title="MyAnimeList may be offline.",
                    description="May be offline or just slow to load"
                )

        if request.path.startswith("/anime/top/") or request.path.startswith("/anime/search"):
            return

        if req_status_code == 404:
            raise HTTPNotFound(title="404 Not Found", description="The anime you are looking doesn't exists on MyAnimeList.")
        elif not str(req_status_code).startswith("2"):
            http_status = HTTPStatus(req_status_code)
            status_code = getattr(http_status, "value")
            phrase = getattr(http_status, "phrase")
            description = getattr(http_status, "description")
            raise HTTPError(
                f"{status_code} {phrase}",
                title=phrase,
                description=description
            )
