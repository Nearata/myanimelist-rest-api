from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from ..responses import HTTPErrorResponse


class RequireJsonMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        accept = request.headers.get("accept", [])

        if any(i in accept for i in ("application/json", "*/*")):
            return await call_next(request)

        return HTTPErrorResponse(406)
