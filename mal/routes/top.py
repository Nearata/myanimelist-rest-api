from fastapi import APIRouter, Depends
from httpx import AsyncClient
from starlette.responses import JSONResponse

from mal.dependencies import mal_response

from ..scrapers import AnimeScrapers
from ..state import get_anime, get_session
from ..validators import TopParameters

router = APIRouter(prefix="/top")


@router.get("")
async def anime_top(
    params: TopParameters = Depends(),
    scrapers: AnimeScrapers = Depends(get_anime),
    session: AsyncClient = Depends(get_session),
) -> JSONResponse:
    if response := await mal_response(session=session, path=router.prefix):
        return response

    data = await scrapers.top(params.type, params.page_number)
    return JSONResponse(data, status_code=201)
