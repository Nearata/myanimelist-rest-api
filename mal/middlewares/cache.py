from json import loads
from typing import Any

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from mal.config import CACHE
from mal.utils.cache import CacheUtil


class CacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Any) -> Any:
        if not CACHE:
            return await call_next(request)

        path: str = request.scope.get("path", "")

        if path.startswith(("/search", "/top")):
            return await call_next(request)

        cache_util: CacheUtil = request.app.state.cache

        mal_id = request.query_params.get("mal_id", "")
        mal_request = request.query_params.get("mal_request", "")

        cache_key = path.strip("/")
        cache_key += f"{mal_id}{mal_request}"

        if page_number := request.query_params.get("page_number"):
            cache_key += f"{page_number}"

        query = cache_util.query(cache_key)

        exists = await query.exists()
        if not exists:
            return await call_next(request)

        cache = await query.get()
        if cache_util.is_expired(cache):
            await cache.delete()
            return await call_next(request)

        return JSONResponse(loads(cache.json))
