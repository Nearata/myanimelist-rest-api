import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_clubs(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "clubs"}
    response = await client.get("/anime", params=params)
    clubs = response.json()["data"][0]

    assert isinstance(clubs["name"], str)
    assert isinstance(clubs["url"], str)
    assert isinstance(clubs["members"], int)
