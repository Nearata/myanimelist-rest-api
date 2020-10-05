from fastapi.testclient import TestClient

from mal.main import create_app
from mal.config import Config


app = create_app()
client = TestClient(app)

def test_featured() -> None:
    Config.CACHE = False

    response = client.get("/anime/1/featured")
    featured = response.json()["featured"][0]

    assert type(featured["image"]) == str
    assert type(featured["url"]) == str
    assert type(featured["title"]) == str
    assert type(featured["content"]) == str
    assert type(featured["writer"]) == str
    assert type(featured["tags"][0]["name"]) == str
