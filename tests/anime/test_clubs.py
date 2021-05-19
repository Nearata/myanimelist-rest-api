import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_clubs(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "clubs"}
    response = await client.get("/anime", params=params)
    clubs = response.json()["clubs"][0]

    assert type(clubs["name"]) == str
    assert type(clubs["url"]) == str
    assert type(clubs["members"]) == int
