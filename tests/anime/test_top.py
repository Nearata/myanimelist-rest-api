import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_top(client: AsyncClient) -> None:
    params = {
        "request": "anime",
        "type": "all",
        "page_number": "1"
    }
    response = await client.get("/top", params=params)
    top = response.json()["results"][0]

    assert type(top["rank"]) == int
    assert type(top["mal_id"]) == int
    assert type(top["url"]) == str
    assert type(top["image_url"]) == str
    assert type(top["title"]) == str
    assert type(top["episodes"]) == int
    assert type(top["members"]) == int
    assert type(top["score"]) == float
