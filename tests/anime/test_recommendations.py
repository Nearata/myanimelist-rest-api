import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_recommendations(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "recommendations"}
    response = await client.get("/anime", params=params)
    recommendation = response.json()["data"][0]

    assert isinstance(recommendation["imageUrl"], str)
    assert isinstance(recommendation["title"], str)
    assert isinstance(recommendation["url"], str)
    assert isinstance(recommendation["recommendationUrl"], str)
    assert isinstance(recommendation["malId"], int)
