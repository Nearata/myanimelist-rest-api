from fastapi.testclient import TestClient

from . import app


client = TestClient(app)

def test_featured() -> None:
    response = client.get("/anime/1/featured")
    featured = response.json()["featured"][0]

    assert type(featured["image"]) == str
    assert type(featured["url"]) == str
    assert type(featured["title"]) == str
    assert type(featured["content"]) == str
    assert type(featured["writer"]) == str
    assert type(featured["tags"][0]["name"]) == str
