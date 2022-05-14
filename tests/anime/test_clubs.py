import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_clubs(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "clubs"}
    response = await client.get("/anime", params=params)
    data = response.json()["data"]

    assert len(data) > 0

    assert isinstance(data[0]["name"], str)
    assert isinstance(data[0]["url"], str)
    assert isinstance(data[0]["members"], int)
