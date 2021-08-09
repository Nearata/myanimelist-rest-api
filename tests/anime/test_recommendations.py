import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_recommendations(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "recommendations"}
    response = await client.get("/anime", params=params)
    recommendation = response.json()["data"][0]

    assert type(recommendation["imageUrl"]) == str
    assert type(recommendation["title"]) == str
    assert type(recommendation["url"]) == str
    assert type(recommendation["recommendationUrl"]) == str
    assert type(recommendation["malId"]) == int
