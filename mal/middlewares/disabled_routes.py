from http import HTTPStatus
from typing import Any

from fastapi import Request
from fastapi.routing import APIRoute
from starlette.responses import JSONResponse

from mal.config import DISABLED_ROUTES


class DisabledRoutesMiddleware:
    async def __call__(self, request: Request, call_next: Any) -> Any:
        path: str = request.scope.get("path", "")
        routes: list[str] = [i.path for i in request.app.routes]

        if path not in routes or path in DISABLED_ROUTES:
            http_status = HTTPStatus(404)
            phrase = http_status.phrase
            description = http_status.description
            return JSONResponse(
                {"title": f"404 {phrase}", "description": description}, 404
            )

        return await call_next(request)
