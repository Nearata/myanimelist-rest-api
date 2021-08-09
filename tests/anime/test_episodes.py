import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_episodes(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "episodes", "page": 1}
    response = await client.get("/anime", params=params)
    episode = response.json()["data"][0]

    assert type(episode["title"]) == str
    assert type(episode["titleRomanji"]) == str
    assert type(episode["titleJapanese"]) == str
    assert type(episode["number"]) == int
    assert type(episode["aired"]) == str
    assert type(episode["filler"]) == bool
    assert type(episode["recap"]) == bool
