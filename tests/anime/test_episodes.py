from fastapi.testclient import TestClient

from mal.main import create_app
from mal.config import Config


app = create_app()
client = TestClient(app)

def test_episodes() -> None:
    Config.CACHE = False

    response = client.get("/anime/1/episodes/1")
    episode = response.json()["episodes"][0]

    assert type(episode["title"]) == str
    assert type(episode["title_romanji"]) == str
    assert type(episode["title_japanese"]) == str
    assert type(episode["number"]) == int
    assert type(episode["aired"]) == str
    assert type(episode["filler"]) == bool
    assert type(episode["recap"]) == bool
