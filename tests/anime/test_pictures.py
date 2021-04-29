from fastapi.testclient import TestClient

from mal.main import create_app


app = create_app()
client = TestClient(app)

def test_pictures() -> None:
    response = client.get("/anime/1/pictures")
    picture = response.json()["pictures"][0]

    assert type(picture["large"]) == str
    assert type(picture["small"]) == str
