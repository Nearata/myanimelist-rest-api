from fastapi.testclient import TestClient

from mal.main import create_app
from mal.config import Config


app = create_app()
client = TestClient(app)

def test_clubs() -> None:
    Config.CACHE = False

    response = client.get("/anime/1/clubs")
    clubs = response.json()["clubs"][0]

    assert type(clubs["name"]) == str
    assert type(clubs["url"]) == str
    assert type(clubs["members"]) == int
