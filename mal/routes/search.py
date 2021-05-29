from fastapi import APIRouter, Depends
from httpx import AsyncClient
from starlette.requests import Request
from starlette.responses import JSONResponse

from mal.utils import SoupUtil

from ..dependencies import get_request, mal_response
from ..parsers.search.anime import SearchAnimeParser
from ..validators import SearchParameters

router = APIRouter(prefix="/search")


@router.get("/anime")
async def anime(
    params: SearchParameters = Depends(), request: Request = Depends(get_request)
) -> JSONResponse:
    if response := await mal_response(request):
        return response

    session: AsyncClient = request.app.state.session
    soup_util = SoupUtil(session)

    search = SearchAnimeParser(
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
