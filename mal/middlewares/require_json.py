from http import HTTPStatus
from typing import Any

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RequireJsonMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Any) -> Any:
        accept = request.headers.get("accept", [])

        if any(i in accept for i in ("application/json", "*/*")):
            return await call_next(request)

        http_status = HTTPStatus(406)
        phrase = http_status.phrase
        description = http_status.description
        return JSONResponse({"title": phrase, "description": description}, 406)
