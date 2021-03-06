from fastapi.testclient import TestClient

from mal.main import create_app
from mal.config import Config


app = create_app()
client = TestClient(app)

def test_top() -> None:
    Config.CACHE = False

    response = client.get("/top/anime/all/1")
    top = response.json()["results"][0]

    assert type(top["rank"]) == int
    assert type(top["mal_id"]) == int
    assert type(top["url"]) == str
    assert type(top["image_url"]) == str
    assert type(top["title"]) == str
    assert type(top["episodes"]) == int
    assert type(top["members"]) == int
    assert type(top["score"]) == float
