import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_top(client: AsyncClient) -> None:
    params = {"request": "anime", "type": "all", "page": "1"}
    response = await client.get("/top/anime", params=params)
    top = response.json()["data"][0]

    assert isinstance(top["rank"], int)
    assert isinstance(top["malId"], int)
    assert isinstance(top["url"], str)
    assert isinstance(top["imageUrl"], str)
    assert isinstance(top["title"], str)
    assert isinstance(top["episodes"], int)
    assert isinstance(top["members"], int)
    assert isinstance(top["score"], float)
