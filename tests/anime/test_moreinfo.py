from fastapi.testclient import TestClient

from mal.main import create_app
from mal.config import Config


app = create_app()
client = TestClient(app)

def test_moreinfo() -> None:
    Config.CACHE = False

    response = client.get("/anime/1/moreinfo")
    moreinfo = response.json()["more_info"]

    assert type(moreinfo) == str
