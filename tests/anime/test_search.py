from fastapi.testclient import TestClient

from mal.main import create_app
from mal.config import Config


app = create_app()
client = TestClient(app)

def test_search() -> None:
    Config.CACHE = False

    response = client.get("/search/anime?query=kimetsu no yaiba&columns=a,b,c,d,e,f,g")
    result = response.json()["results"][0]

    assert type(result["mal_id"]) == int
    assert type(result["url"]) == str
    assert type(result["image_url"]) == str
    assert type(result["title"]) == str
    assert type(result["type"]) == str
    assert type(result["episodes"]) == int
    assert type(result["score"]) == float
    assert type(result["start_date"]) == str
    assert type(result["end_date"]) == str
    assert type(result["members"]) == int
    assert type(result["rated"]) == str
