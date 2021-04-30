from fastapi.testclient import TestClient

from . import app

client = TestClient(app)


def test_clubs() -> None:
    response = client.get("/anime/1/clubs")
    clubs = response.json()["clubs"][0]

    assert type(clubs["name"]) == str
    assert type(clubs["url"]) == str
    assert type(clubs["members"]) == int
