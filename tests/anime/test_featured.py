import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_featured(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "featured"}
    response = await client.get("/anime", params=params)
    featured = response.json()["featured"][0]

    assert type(featured["image"]) == str
    assert type(featured["url"]) == str
    assert type(featured["title"]) == str
    assert type(featured["content"]) == str
    assert type(featured["writer"]) == str
    assert type(featured["tags"][0]["name"]) == str
