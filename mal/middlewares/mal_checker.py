from http import HTTPStatus
from typing import Any

from fastapi import Request
from httpx import AsyncClient, TimeoutException
from starlette.responses import JSONResponse

from ..config import USER_AGENT


class MalCheckerMiddleware:
    async def __call__(self, request: Request, call_next: Any) -> Any:
        path: str = request.scope.get("path", "")

        if not request.query_params.keys():
            return await call_next(request)

        mal_id = request.query_params.get("mal_id", "")
        mal_request = request.query_params.get("mal_request", "")

        session: AsyncClient = request.app.state.session
        try:
            response = await session.head(
                f"https://myanimelist.net{path}/{mal_id}/_/{mal_request}",
                timeout=15,
                headers={"User-Agent": USER_AGENT},
            )
            status_code = response.status_code
        except TimeoutException:
            http_status = HTTPStatus(504)
            return JSONResponse(
                {
                    "title": f"504 {http_status.phrase}",
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
