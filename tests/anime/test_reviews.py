import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_reviews(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "reviews", "page": 1}
    response = await client.get("/anime", params=params)
    review = response.json()["data"][0]

    assert isinstance(review["date"], str)
    assert isinstance(review["helpfulCount"], int)
    assert isinstance(review["url"], str)

    reviewer = review["reviewer"]
    assert isinstance(reviewer["profileUrl"], str)
    assert isinstance(reviewer["imageUrl"], str)
    assert isinstance(reviewer["username"], str)

    reviewer_scores = reviewer["scores"]
    for i in reviewer_scores.keys():
        assert isinstance(reviewer_scores[i], int)
