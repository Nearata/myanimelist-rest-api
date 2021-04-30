from json import loads
from typing import Any

from fastapi import Request
from starlette.responses import JSONResponse

from mal.config import CACHE
from mal.utils import CacheUtil


class CacheMiddleware:
    async def __call__(self, request: Request, call_next: Any) -> Any:
        if not CACHE:
            return await call_next(request)

        path: str = request.scope["path"]

        if path.startswith(("/search", "/top/")):
            return await call_next(request)

        cache: CacheUtil = request.app.state.cache
        cache_key = path.replace("/", "")
        get_cache = cache.get_or_none(cache_key)

        if not get_cache:
            return await call_next(request)

        if cache.is_expired(get_cache.expire):
            cache.delete(cache_key)
            return await call_next(request)

        return JSONResponse(loads(get_cache.json))
