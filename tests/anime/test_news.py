from fastapi.testclient import TestClient

from mal.main import create_app
from mal.config import Config


app = create_app()
client = TestClient(app)

def test_news() -> None:
    Config.CACHE = False

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
