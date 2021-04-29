from json import loads
from typing import Any

from fastapi import Request
from starlette.responses import JSONResponse

from mal.config import Config
from mal.utils import CacheUtil


class CacheMiddleware:
    async def __call__(self, request: Request, call_next: Any) -> Any:
        if not Config.CACHE:
            return await call_next(request)

        path: str = request.scope["path"]

        if path.startswith(("/search", "/top/")):
            return await call_next(request)

        cache_key = path.replace("/", "")
        get_cache = CacheUtil.get_or_none(cache_key)

        if not get_cache:
            return await call_next(request)

        if CacheUtil.is_expired(get_cache.expire):
            CacheUtil.delete(cache_key)
            return await call_next(request)

        return JSONResponse(loads(get_cache.json))
