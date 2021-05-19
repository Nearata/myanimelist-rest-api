import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_recommendations(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "recommendations"}
    response = await client.get("/anime", params=params)
    recommendation = response.json()["recommendations"][0]

    assert type(recommendation["image_url"]) == str
    assert type(recommendation["title"]) == str
    assert type(recommendation["url"]) == str
    assert type(recommendation["recommendation_url"]) == str
    assert type(recommendation["mal_id"]) == int
