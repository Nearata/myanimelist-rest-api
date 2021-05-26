from mal.utils import SoupUtil
from fastapi import APIRouter, Depends
from httpx import AsyncClient
from starlette.responses import JSONResponse

from ..dependencies import get_session, mal_response
from ..parsers.anime.search import Search as AnimeSearch
from ..validators import SearchParameters

router = APIRouter(prefix="/search")


@router.get("/anime")
async def anime(
    params: SearchParameters = Depends(), session: AsyncClient = Depends(get_session)
) -> JSONResponse:
    if response := await mal_response(session=session, path=router.prefix):
        return response

    soup_util = SoupUtil(session)

    search = AnimeSearch(
        soup_util,
        query=params.query,
        type=params.type,
        score=params.score,
        status=params.status,
        producer=params.producer,
        rated=params.rated,
        start_day=params.start_day,
        start_month=params.start_month,
        start_year=params.start_year,
        end_day=params.end_day,
        end_month=params.end_month,
        end_year=params.end_year,
        genres=params.genres,
        genres_exclude=params.genres_exclude,
        columns=params.columns,
    )
    data = await search()
    return JSONResponse(data, status_code=201)
