import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_moreinfo(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "moreinfo"}
    response = await client.get("/anime", params=params)
    moreinfo = response.json()["data"]

    assert type(moreinfo) == str
