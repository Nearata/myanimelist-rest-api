import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_news(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "news"}
    response = await client.get("/anime", params=params)
    news = response.json()["news"][0]

    assert type(news["url"]) == str
    assert type(news["image_url"]) == str
    assert type(news["title"]) == str
    assert type(news["content"]) == str
    assert type(news["author"]) == str
    assert type(news["author_profile"]) == str
    assert type(news["comments"]) == int
    assert type(news["forum_url"]) == str
