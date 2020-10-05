from fastapi.testclient import TestClient

from mal.main import create_app
from mal.config import Config


app = create_app()
client = TestClient(app)

def test_details() -> None:
    Config.CACHE = False

    response = client.get("/anime/1/details")
    details = response.json()["details"]

    assert type(details["title"]) == str
    assert type(details["image"]) == str
    assert type(details["trailer"]) == str
    assert type(details["synopsis"]) == str
    assert type(details["background"]) == str

    alternative_titles = details["alternative_titles"]
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
    assert type(producer["mal_id"]) == int

    licensor = information["licensors"][0]
    assert type(licensor["name"]) == str
    assert type(licensor["url"]) == str
    assert type(licensor["mal_id"]) == int

    studio = information["studios"][0]
    assert type(studio["name"]) == str
    assert type(studio["url"]) == str
    assert type(studio["mal_id"]) == int

    assert type(information["source"]) == str

    genre = information["genres"][0]
    assert type(genre["name"]) == str
    assert type(genre["mal_id"]) == int

    assert type(information["duration"]) == int
    assert type(information["rating"]) == str

    statistics = details["statistics"]
    assert type(statistics["score"]) == float
    assert type(statistics["ranked"]) == int
    assert type(statistics["popularity"]) == int
    assert type(statistics["members"]) == int
    assert type(statistics["favorites"]) == int

    related_anime = details["related_anime"]
    adaptation = related_anime["adaptation"][0]
    assert type(adaptation["title"]) == str
    assert type(adaptation["type"]) == str
    assert type(adaptation["mal_id"]) == int

    assert type(details["opening_theme"][0]["title"]) == str
    assert type(details["ending_theme"][0]["title"]) == str
