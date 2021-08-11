import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_episodes(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "episodes", "page": 1}
    response = await client.get("/anime", params=params)
    episode = response.json()["data"][0]

    assert isinstance(episode["title"], str)
    assert isinstance(episode["titleRomanji"], str)
    assert isinstance(episode["titleJapanese"], str)
    assert isinstance(episode["number"], int)
    assert isinstance(episode["aired"], str)
    assert isinstance(episode["filler"], bool)
    assert isinstance(episode["recap"], bool)
