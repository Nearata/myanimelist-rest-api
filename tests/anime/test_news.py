import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_news(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "news"}
    response = await client.get("/anime", params=params)
    news = response.json()["data"][0]

    assert type(news["url"]) == str
    assert type(news["imageUrl"]) == str
    assert type(news["title"]) == str
    assert type(news["content"]) == str
    assert type(news["author"]) == str
    assert type(news["authorProfile"]) == str
    assert type(news["comments"]) == int
    assert type(news["forumUrl"]) == str
