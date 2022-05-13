import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_details(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "details"}
    response = await client.get("/anime", params=params)
    details = response.json()["data"]

    assert isinstance(details["title"], str)
    assert isinstance(details["pictureUrl"], str)
    assert isinstance(details["trailerUrl"], str)
    assert isinstance(details["synopsis"], str)
    assert isinstance(details["background"], str)
    assert isinstance(details["titleEnglish"], str)
    assert isinstance(details["titleJapanese"], str)
    assert isinstance(details["titleSynonyms"], list)
    assert isinstance(details["type"], str)
    assert isinstance(details["episodes"], int)
    assert isinstance(details["status"], str)
    assert isinstance(details["aired"]["from"], str)
    assert isinstance(details["aired"]["to"], str)
    assert isinstance(details["premiered"], str)
    assert len(details["producers"]) > 0
    assert len(details["licensors"]) > 0
    assert len(details["studios"]) > 0
    assert isinstance(details["source"], str)
    assert len(details["genres"]) > 0
    assert isinstance(details["duration"], str)
    assert isinstance(details["rating"], str)
    assert isinstance(details["score"], float)
    assert isinstance(details["ranked"], str)
    assert isinstance(details["popularity"], str)
    assert isinstance(details["members"], int)
    assert isinstance(details["favorites"], int)
    assert len(details["adaptation"]) > 0
    assert len(details["sideStory"]) > 0
    assert len(details["summary"]) > 0
    assert len(details["openingTheme"]) > 0
    assert len(details["endingTheme"]) > 0
