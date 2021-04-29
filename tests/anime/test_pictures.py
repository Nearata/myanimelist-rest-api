from fastapi.testclient import TestClient

from . import app


client = TestClient(app)

def test_pictures() -> None:
    response = client.get("/anime/1/pictures")
    picture = response.json()["pictures"][0]

    assert type(picture["large"]) == str
    assert type(picture["small"]) == str
