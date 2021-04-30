from http import HTTPStatus
from typing import Any

from fastapi import Request
from httpx import Client, ReadTimeout
from starlette.responses import JSONResponse

from mal.utils.requests import RequestsUtil


class MalCheckerMiddleware:
    async def __call__(self, request: Request, call_next: Any) -> Any:
        path: str = request.scope["path"]

        session: Client = request.app.state.session

        try:
            response = session.head(
                f"https://myanimelist.net{path}",
                timeout=15,
                headers=RequestsUtil.HEADERS,
            )
            status_code = response.status_code
        except ReadTimeout:
            http_status = HTTPStatus(504)
            phrase = http_status.phrase
            return JSONResponse(
                {
                    "title": f"504 {phrase}",
                    "description": "May be offline or just slow to load",
                },
                504,
            )

        if path.startswith(("/search", "/top")):
            return await call_next(request)

        if status_code == 404:
            return JSONResponse(
                {
                    "title": "404 Not Found",
                    "description": "The anime you are looking doesn't exists on MyAnimeList.",
                },
                404,
            )

        if not str(status_code).startswith("2"):
            http_status = HTTPStatus(status_code)
            status_code = http_status.value
            phrase = http_status.phrase
            description = http_status.description
            return JSONResponse(
                {"title": f"{status_code} {phrase}", "description": description},
                status_code,
            )

        return await call_next(request)
