from typing import Any

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from ..config import DISABLED_ROUTES
from ..responses import HTTPErrorResponse


class DisabledRoutesMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Any) -> Any:
        path: str = request.scope.get("path", "")
        routes: list[str] = [i.path for i in request.app.routes]

        if path not in routes or path in DISABLED_ROUTES:
            return HTTPErrorResponse(404)

        return await call_next(request)
