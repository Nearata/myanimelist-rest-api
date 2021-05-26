from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..dependencies import get_request, mal_response
from ..scrapers import TopScrapers
from ..validators import TopParameters

router = APIRouter(prefix="/top")


@router.get("/anime")
async def anime(
    params: TopParameters = Depends(),
    request: Request = Depends(get_request),
) -> JSONResponse:
    session = request.app.state.session
    if response := await mal_response(session=session, path=router.prefix):
        return response

    scrapers: TopScrapers = request.app.state.top_scrapers

    data = await scrapers.anime(params.type, params.page_number)
    return JSONResponse(data, status_code=201)
