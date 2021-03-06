from fastapi.testclient import TestClient

from mal.main import create_app
from mal.config import Config


app = create_app()
client = TestClient(app)

def test_recommendations() -> None:
    Config.CACHE = False

    response = client.get("/anime/1/recommendations")
    recommendation = response.json()["recommendations"][0]

    assert type(recommendation["image_url"]) == str
    assert type(recommendation["title"]) == str
    assert type(recommendation["url"]) == str
    assert type(recommendation["recommendation_url"]) == str
    assert type(recommendation["mal_id"]) == int
