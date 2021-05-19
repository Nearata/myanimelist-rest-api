import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_characters(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "characters"}
    response = await client.get("/anime", params=params)
    characters = response.json()["characters"][0]

    assert type(characters["url"]) == str
    assert type(characters["image_url"]) == str
    assert type(characters["name"]) == str
    assert type(characters["role"]) == str

    va = characters["voice_actors"][0]

    assert type(va["name"]) == str
    assert type(va["language"]) == str
    assert type(va["url"]) == str
    assert type(va["image"]) == str
