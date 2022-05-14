import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_search(client: AsyncClient) -> None:
    params = {
        "query": "tokyo",
        "columns": "a,b,c,d,e,f,g"
    }
    response = await client.get("/search/anime", params=params)
    data = response.json()["data"][0]

    assert isinstance(data["pictureUrl"], str)
    assert isinstance(data["id"], int)
    assert isinstance(data["title"], str)
    assert isinstance(data["type"], str)
    assert isinstance(data["episodes"], int)
    assert isinstance(data["score"], float)
    assert isinstance(data["startDate"], str)
    assert isinstance(data["endDate"], str)
    assert isinstance(data["members"], int)
    assert isinstance(data["rated"], str)
