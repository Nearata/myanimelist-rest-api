from fastapi.testclient import TestClient

from mal.main import create_app
from mal.config import Config


app = create_app()
client = TestClient(app)

def test_characters() -> None:
    Config.CACHE = False

    response = client.get("/anime/1/characters")
    characters = response.json()["characters"][0]

    assert type(characters["url"]) == str
    assert type(characters["image_url"]) == str
    assert type(characters["name"]) == str
    assert type(characters["role"]) == str

    va = characters["voice_actors"][0]

    assert type(va["name"]) == str
    assert type(va["language"]) == str
    assert type(va["url"]) == str
    assert type(va["image"]) == str
