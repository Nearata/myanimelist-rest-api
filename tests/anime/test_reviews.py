import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_reviews(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "reviews", "page": 1}
    response = await client.get("/anime", params=params)
    review = response.json()["data"][0]

    assert type(review["date"]) == str
    assert type(review["helpfulCount"]) == int
    assert type(review["url"]) == str

    reviewer = review["reviewer"]
    assert type(reviewer["profileUrl"]) == str
    assert type(reviewer["imageUrl"]) == str
    assert type(reviewer["username"]) == str

    reviewer_scores = reviewer["scores"]
    for i in reviewer_scores.keys():
        assert type(reviewer_scores[i]) == int
