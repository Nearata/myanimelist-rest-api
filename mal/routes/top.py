from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..dependencies import get_request, mal_response
from ..scrapers import TopScrapers
from ..validators import TopAnimeParameters

router = APIRouter(prefix="/top")


@router.get("/anime")
async def anime(
    params: TopAnimeParameters = Depends(),
    request: Request = Depends(get_request),
) -> JSONResponse:
    if response := await mal_response(request):
        return response

    scrapers: TopScrapers = request.app.state.top_scrapers

    data = await scrapers.anime(params.type, params.page)
    return JSONResponse(data, status_code=201)
