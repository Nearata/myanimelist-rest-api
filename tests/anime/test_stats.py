import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_stats(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "stats"}
    response = await client.get("/anime", params=params)
    stats = response.json()

    summary = stats["data"]["summary"]
    for i in summary.keys():
        assert type(summary[i]) == int

    scores = stats["data"]["scores"]
    for i in scores.keys():
        assert type(scores[i]["percentage"]) == float
        assert type(scores[i]["votes"]) == int
