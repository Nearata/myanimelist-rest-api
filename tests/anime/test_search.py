import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_search(client: AsyncClient) -> None:
    params = {
        "request": "anime",
        "query": "kimetsu no yaiba",
        "columns": "a,b,c,d,e,f,g"
    }
    response = await client.get("/search/anime", params=params)
    result = response.json()["results"][0]

    assert type(result["mal_id"]) == int
    assert type(result["url"]) == str
    assert type(result["image_url"]) == str
    assert type(result["title"]) == str
    assert type(result["type"]) == str
    assert type(result["episodes"]) == int
    assert type(result["score"]) == float
    assert type(result["start_date"]) == str
    assert type(result["end_date"]) == str
    assert type(result["members"]) == int
    assert type(result["rated"]) == str
