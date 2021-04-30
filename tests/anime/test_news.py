from fastapi.testclient import TestClient

from . import app

client = TestClient(app)


def test_news() -> None:
    response = client.get("/anime/1/news")
    news = response.json()["news"][0]

    assert type(news["url"]) == str
    assert type(news["image_url"]) == str
    assert type(news["title"]) == str
    assert type(news["content"]) == str
    assert type(news["author"]) == str
    assert type(news["author_profile"]) == str
    assert type(news["comments"]) == int
    assert type(news["forum_url"]) == str
