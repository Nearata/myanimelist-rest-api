from typing import Any
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_search(client: AsyncClient) -> None:
    params: dict[str, Any] = {"query": "tokyo", "columns": "a,b,c,d,e,f,g", "page": 2}
    response = await client.get("/search/anime", params=params)
    json = response.json()
    links = json["links"]
    data = json["data"][0]

    assert isinstance(links["self"], str)
    assert isinstance(links["next"], str)
    assert isinstance(links["previous"], str)
    assert isinstance(links["last"], str)

    assert len(data) > 0

    assert "pictureUrl" in data
    assert "id" in data
    assert "title" in data
    assert "type" in data
    assert "episodes" in data
    assert "score" in data
    assert "startDate" in data
    assert "endDate" in data
    assert "members" in data
    assert "rated" in data

    assert isinstance(data["pictureUrl"], str)
    assert isinstance(data["id"], int)
    assert isinstance(data["title"], str)
    assert isinstance(data["type"], str)
    assert isinstance(data["episodes"], int)
    assert isinstance(data["score"], float)
    assert isinstance(data["startDate"], str)
    assert isinstance(data["endDate"], str)
    assert isinstance(data["members"], int)
    assert isinstance(data["rated"], str)
