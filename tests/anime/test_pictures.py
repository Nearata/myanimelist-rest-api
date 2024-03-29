import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_pictures(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "pictures"}
    response = await client.get("/anime", params=params)
    picture = response.json()["data"][0]

    assert isinstance(picture["large"], str)
    assert isinstance(picture["small"], str)
