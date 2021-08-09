import pytest
from httpx import AsyncClient

from ..util import DEFAULT_PARAMS


@pytest.mark.asyncio
async def test_details(client: AsyncClient) -> None:
    params = DEFAULT_PARAMS | {"mal_request": "details"}
    response = await client.get("/anime", params=params)
    details = response.json()["data"]

    assert type(details["title"]) == str
    assert type(details["image"]) == str
    assert type(details["trailer"]) == str
    assert type(details["synopsis"]) == str
    assert type(details["background"]) == str

    alternative_titles = details["alternativeTitles"]
    assert type(alternative_titles["english"]) == str
    assert type(alternative_titles["japanese"]) == str
    assert type(alternative_titles["synonyms"]) == list

    information = details["information"]
    assert type(information["type"]) == str
    assert type(information["episodes"]) == int
    assert type(information["status"]) == str
    assert type(information["aired"]["from"]) == str
    assert type(information["aired"]["to"]) == str
    assert type(information["premiered"]) == str

    producer = information["producers"][0]
    assert type(producer["name"]) == str
    assert type(producer["url"]) == str
    assert type(producer["malId"]) == int

    licensor = information["licensors"][0]
    assert type(licensor["name"]) == str
    assert type(licensor["url"]) == str
    assert type(licensor["malId"]) == int

    studio = information["studios"][0]
    assert type(studio["name"]) == str
    assert type(studio["url"]) == str
    assert type(studio["malId"]) == int

    assert type(information["source"]) == str

    genre = information["genres"][0]
    assert type(genre["name"]) == str
    assert type(genre["malId"]) == int

    assert type(information["duration"]) == int
    assert type(information["rating"]) == str

    statistics = details["statistics"]
    assert type(statistics["score"]) == float
    assert type(statistics["ranked"]) == int
    assert type(statistics["popularity"]) == int
    assert type(statistics["members"]) == int
    assert type(statistics["favorites"]) == int

    related_anime = details["relatedAnime"]
    adaptation = related_anime["adaptation"][0]
    assert type(adaptation["title"]) == str
    assert type(adaptation["type"]) == str
    assert type(adaptation["malId"]) == int

    assert type(details["openingTheme"][0]["title"]) == str
    assert type(details["endingTheme"][0]["title"]) == str
