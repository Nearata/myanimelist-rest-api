from fastapi import APIRouter, Depends
from httpx import AsyncClient
from starlette.responses import JSONResponse

from ..config import CACHE
from ..dependencies import cached_response, mal_response
from ..scrapers import AnimeScrapers
from ..state import CacheUtil, get_anime, get_cache, get_session
from ..validators import AnimeParameters

router = APIRouter(prefix="/anime")


@router.get("")
async def anime(
    params: AnimeParameters = Depends(),
    cache_util: CacheUtil = Depends(get_cache),
    scrapers: AnimeScrapers = Depends(get_anime),
    session: AsyncClient = Depends(get_session),
) -> JSONResponse:
    mal_id = params.mal_id
    mal_request = params.mal_request
    page_number = params.page_number
    prefix = router.prefix
    cache_key = f"{prefix.strip('/')}{mal_id}{mal_request}"

    if cached := await cached_response(
        cache_util=cache_util, cache_key=cache_key, page_number=page_number
    ):
        return cached

    if response := await mal_response(mal_id=mal_id, session=session, path=prefix):
        return response

    if page_number:
        cache_key += str(page_number)
        data = await getattr(scrapers, mal_request)(mal_id, page_number)
    else:
        data = await getattr(scrapers, mal_request)(mal_id)

    if CACHE:
        await cache_util.save(cache_key, data)

    return JSONResponse(data, status_code=201)
