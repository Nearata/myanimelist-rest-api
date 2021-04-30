from fastapi import Request

from mal.utils import CacheUtil


def get_cache(request: Request) -> CacheUtil:
    return request.app.state.cache
