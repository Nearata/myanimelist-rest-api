from fastapi import APIRouter, Depends
from httpx import AsyncClient

from ..scrapers.anime.search import Search as AnimeSearch
from ..state import get_session
from ..validators import SearchParameters

router = APIRouter()


@router.get("/search")
async def anime_search(
    params: SearchParameters = Depends(), session: AsyncClient = Depends(get_session)
) -> dict:
    search = AnimeSearch(
        session,
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
    return data
