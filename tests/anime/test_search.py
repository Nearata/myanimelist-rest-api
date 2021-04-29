from fastapi.testclient import TestClient

from . import app


client = TestClient(app)

def test_search() -> None:
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
