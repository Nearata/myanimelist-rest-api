from http import HTTPStatus
from re import search
from falcon import HTTPError, Request, Response
from requests import Session
from requests.exceptions import ReadTimeout


class CheckUrlMiddleware:
    def process_request(self, request: Request, response: Response) -> None:
        regex_list = [
            search(r"\/(anime)\/([0-9]{1,5})", request.uri),
            search(r"\/(search)\/(anime)\?.*", request.uri),
            search(r"\/(top)\/(anime)\/(\w+)\/([0-9])", request.uri)
        ]
        res = None
        with Session() as s:
            for i in regex_list:
                if not i:
                    continue

                try:
                    res = s.head(f"https://myanimelist.net{i.group()}", timeout=15, headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
                    })
                except ReadTimeout:
                    http_status = HTTPStatus(504)
                    status_code = getattr(http_status, "value")
                    phrase = getattr(http_status, "phrase")
                    description = getattr(http_status, "description")
                    raise HTTPError(
                        f"{status_code} {phrase}",
                        phrase,
                        description,
                        code=status_code
                    )

        http_status = HTTPStatus(res.status_code) if res else None
        if res and not str(http_status.value).startswith("2"):
            status_code = getattr(http_status, "value")
            phrase = getattr(http_status, "phrase")
            description = getattr(http_status, "description")
            raise HTTPError(
                f"{status_code} {phrase}",
                phrase,
                description,
                code=status_code
            )
