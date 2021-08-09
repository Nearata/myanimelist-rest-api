import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_top(client: AsyncClient) -> None:
    params = {
        "request": "anime",
        "type": "all",
        "page": "1"
    }
    response = await client.get("/top/anime", params=params)
    top = response.json()["data"][0]

    assert type(top["rank"]) == int
    assert type(top["malId"]) == int
    assert type(top["url"]) == str
    assert type(top["imageUrl"]) == str
    assert type(top["title"]) == str
    assert type(top["episodes"]) == int
    assert type(top["members"]) == int
    assert type(top["score"]) == float
