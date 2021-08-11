import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_staff(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "staff"}
    response = await client.get("/anime", params=params)
    staff = response.json()["data"][0]

    for i in staff.keys():
        assert isinstance(staff[i], str)
