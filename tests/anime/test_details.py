import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_details(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "details"}
    response = await client.get("/anime", params=params)
    details = response.json()["data"]

    assert isinstance(details["title"], str)
    assert isinstance(details["image"], str)
    assert isinstance(details["trailer"], str)
    assert isinstance(details["synopsis"], str)
    assert isinstance(details["background"], str)

    alternative_titles = details["alternativeTitles"]
    assert isinstance(alternative_titles["english"], str)
    assert isinstance(alternative_titles["japanese"], str)
    assert isinstance(alternative_titles["synonyms"], list)

    information = details["information"]
    assert isinstance(information["type"], str)
    assert isinstance(information["episodes"], int)
    assert isinstance(information["status"], str)
    assert isinstance(information["aired"]["from"], str)
    assert isinstance(information["aired"]["to"], str)
    assert isinstance(information["premiered"], str)

    producer = information["producers"][0]
    assert isinstance(producer["name"], str)
    assert isinstance(producer["url"], str)
    assert isinstance(producer["malId"], int)

    licensor = information["licensors"][0]
    assert isinstance(licensor["name"], str)
    assert isinstance(licensor["url"], str)
    assert isinstance(licensor["malId"], int)

    studio = information["studios"][0]
    assert isinstance(studio["name"], str)
    assert isinstance(studio["url"], str)
    assert isinstance(studio["malId"], int)

    assert isinstance(information["source"], str)

    genre = information["genres"][0]
    assert isinstance(genre["name"], str)
    assert isinstance(genre["malId"], int)

    assert isinstance(information["duration"], int)
    assert isinstance(information["rating"], str)

    statistics = details["statistics"]
    assert isinstance(statistics["score"], float)
    assert isinstance(statistics["ranked"], int)
    assert isinstance(statistics["popularity"], int)
    assert isinstance(statistics["members"], int)
    assert isinstance(statistics["favorites"], int)

    adaptation = details["relatedAnime"]["adaptation"][0]
    assert isinstance(adaptation["title"], str)
    assert isinstance(adaptation["type"], str)
    assert isinstance(adaptation["malId"], int)

    assert isinstance(details["openingTheme"][0]["title"], str)
    assert isinstance(details["endingTheme"][0]["title"], str)
