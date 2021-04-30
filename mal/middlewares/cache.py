from json import loads
from typing import Any

from fastapi import Request
from starlette.responses import JSONResponse

from mal.config import CACHE
from mal.utils.cache import CacheUtil


class CacheMiddleware:
    async def __call__(self, request: Request, call_next: Any) -> Any:
        if not CACHE:
            return await call_next(request)

        path: str = request.scope["path"]

        if path.startswith(("/search", "/top/")):
            return await call_next(request)

        cache_util: CacheUtil = request.app.state.cache
        cache_key = path.replace("/", "")
        query = cache_util.query(cache_key)

        exists = await query.exists()
        if not exists:
            return await call_next(request)

        cache = await query.get()
        if cache_util.is_expired(cache):
            await cache.delete()
            return await call_next(request)

        return JSONResponse(loads(cache.json))
