from http import HTTPStatus
from typing import Any

from fastapi import Request
from starlette.responses import JSONResponse

from mal.config import DISABLED_ROUTES


class DisabledRoutesMiddleware:
    async def __call__(self, request: Request, call_next: Any) -> Any:
        path: str = request.scope["path"]

        http_status = HTTPStatus(404)
        phrase = http_status.phrase
        description = http_status.description

        if any(i in path for i in DISABLED_ROUTES):
            return JSONResponse(
                {"title": f"404 {phrase}", "description": description}, 404
            )

        return await call_next(request)
