import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_characters(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "characters"}
    response = await client.get("/anime", params=params)
    characters = response.json()["data"][0]

    assert isinstance(characters["url"], str)
    assert isinstance(characters["pictureUrl"], str)
    assert isinstance(characters["name"], str)
    assert isinstance(characters["role"], str)

    va = characters["voiceActors"][0]

    assert isinstance(va["name"], str)
    assert isinstance(va["language"], str)
    assert isinstance(va["url"], str)
    assert isinstance(va["pictureUrl"], str)
