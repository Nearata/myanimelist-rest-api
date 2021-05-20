from typing import Any

from fastapi import Request
from httpx import AsyncClient, TimeoutException
from starlette.middleware.base import BaseHTTPMiddleware

from ..config import USER_AGENT
from ..responses import HTTPErrorResponse


class MalCheckerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Any) -> Any:
        path: str = request.scope.get("path", "")

        if not request.query_params.keys():
            return await call_next(request)

        mal_id = request.query_params.get("mal_id", "")

        session: AsyncClient = request.app.state.session
        try:
            response = await session.head(
                f"https://myanimelist.net{path}/{mal_id}",
                timeout=15,
                headers={"User-Agent": USER_AGENT},
            )
            status_code = response.status_code
        except TimeoutException:
            return HTTPErrorResponse(504)

        if path.startswith(("/search", "/top")):
            return await call_next(request)

        if status_code == 404:
            return HTTPErrorResponse(404)

        if not str(status_code).startswith("2"):
            return HTTPErrorResponse(status_code)

        return await call_next(request)
