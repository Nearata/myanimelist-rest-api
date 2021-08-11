import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_featured(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "featured"}
    response = await client.get("/anime", params=params)
    featured = response.json()["data"][0]

    assert isinstance(featured["image"], str)
    assert isinstance(featured["url"], str)
    assert isinstance(featured["title"], str)
    assert isinstance(featured["content"], str)
    assert isinstance(featured["writer"], str)
    assert isinstance(featured["tags"][0]["name"], str)
