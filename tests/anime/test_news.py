import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_news(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "news"}
    response = await client.get("/anime", params=params)
    news = response.json()["data"][0]

    assert isinstance(news["url"], str)
    assert isinstance(news["imageUrl"], str)
    assert isinstance(news["title"], str)
    assert isinstance(news["content"], str)
    assert isinstance(news["author"], str)
    assert isinstance(news["authorProfile"], str)
    assert isinstance(news["comments"], int)
    assert isinstance(news["forumUrl"], str)
