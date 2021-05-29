from json import loads
from typing import Optional

from httpx import AsyncClient, TimeoutException
from starlette.requests import Request
from starlette.responses import JSONResponse

from .config import CACHE, USER_AGENT
from .const import MAL_URL
from .responses import HTTPErrorResponse
from .utils import CacheUtil, get_cache_key


async def cached_response(request: Request) -> Optional[JSONResponse]:
    if not CACHE:
        return None

    cache_key = get_cache_key(request)
    cache_util = CacheUtil()
    query = cache_util.query(cache_key)

    exists = await query.exists()
    if not exists:
        return None

    cache = await query.get()
    if cache_util.is_expired(cache):
        await cache.delete()
        return None

    return JSONResponse(loads(cache.json))


async def mal_response(request: Request) -> Optional[HTTPErrorResponse]:
    excluded_routes = ("/search/anime", "/top/anime")
    url = MAL_URL
    path = request.url.path
    mal_id = request.query_params.get("mal_id", "")

    if path not in excluded_routes:
        url += f"{path}/{mal_id}"

    session: AsyncClient = request.app.state.session

    try:
        response = await session.head(
            url,
            timeout=15,
            headers={"User-Agent": USER_AGENT},
        )
        status_code = response.status_code
    except TimeoutException:
        return HTTPErrorResponse(504)

    if path in excluded_routes:
        return None

    if status_code == 404:
        return HTTPErrorResponse(404)

    if not str(status_code).startswith("2"):
        return HTTPErrorResponse(status_code)

    return None


def get_request(request: Request) -> Request:
    return request
