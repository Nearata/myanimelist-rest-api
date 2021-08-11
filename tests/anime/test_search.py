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
    result = response.json()["data"][0]

    assert isinstance(result["malId"], int)
    assert isinstance(result["url"], str)
    assert isinstance(result["imageUrl"], str)
    assert isinstance(result["title"], str)
    assert isinstance(result["type"], str)
    assert isinstance(result["episodes"], int)
    assert isinstance(result["score"], float)
    assert isinstance(result["startDate"], str)
    assert isinstance(result["endDate"], str)
    assert isinstance(result["members"], int)
    assert isinstance(result["rated"], str)
