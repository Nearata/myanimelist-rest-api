from fastapi import APIRouter, Depends

from ..scrapers.anime_scrapers import AnimeScrapers
from ..state import get_anime
from ..validators import TopParameters

router = APIRouter()


@router.get("/top")
async def anime_top(
    params: TopParameters = Depends(),
    scrapers: AnimeScrapers = Depends(get_anime),
) -> dict:
    data = await scrapers.top(params.type, params.page_number)
    return data
