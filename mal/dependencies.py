from json import loads
from typing import Optional

from httpx import AsyncClient, TimeoutException
from starlette.responses import JSONResponse

from .config import CACHE, USER_AGENT
from .responses import HTTPErrorResponse
from .utils.cache import CacheUtil
from .validators import AnimeParameters


async def cached_response(
    params: AnimeParameters, cache_util: CacheUtil, cache_key: str
) -> Optional[JSONResponse]:
    if not CACHE:
        return None

    if page_number := params.page_number:
        cache_key += str(page_number)

    query = cache_util.query(cache_key)

    exists = await query.exists()
    if not exists:
        return None

    cache = await query.get()
    if cache_util.is_expired(cache):
        await cache.delete()
        return None

    return JSONResponse(loads(cache.json))


async def mal_response(
    mal_id: int, session: AsyncClient, path: str
) -> Optional[HTTPErrorResponse]:
    try:
        response = await session.head(
            f"https://myanimelist.net{path}/{mal_id}",
            timeout=15,
            headers={"User-Agent": USER_AGENT},
        )
        status_code = response.status_code
    except TimeoutException:
        return HTTPErrorResponse(504)

    if path.startswith(("/search", "/top")):
        return None

    if status_code == 404:
        return HTTPErrorResponse(404)

    if not str(status_code).startswith("2"):
        return HTTPErrorResponse(status_code)

    return None
