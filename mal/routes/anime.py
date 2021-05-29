from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..config import CACHE
from ..dependencies import cached_response, get_request, mal_response
from ..scrapers import AnimeScrapers
from ..utils import CacheUtil, get_cache_key
from ..validators import AnimeParameters

router = APIRouter(prefix="/anime")


@router.get("")
async def anime(
    params: AnimeParameters = Depends(),
    request: Request = Depends(get_request),
) -> JSONResponse:
    mal_id = params.mal_id
    mal_request = params.mal_request
    page_number = params.page_number

    if cached := await cached_response(request):
        return cached

    if response := await mal_response(request):
        return response

    scrapers: AnimeScrapers = request.app.state.anime_scrapers

    if page_number:
        data = await getattr(scrapers, mal_request)(mal_id, page_number)
    else:
        data = await getattr(scrapers, mal_request)(mal_id)

    cache_key = get_cache_key(request)
    if CACHE:
        await CacheUtil().save(cache_key, data)

    return JSONResponse(data, status_code=201)
