from fastapi.testclient import TestClient

from . import app


client = TestClient(app)

def test_moreinfo() -> None:
    response = client.get("/anime/1/moreinfo")
    moreinfo = response.json()["more_info"]

    assert type(moreinfo) == str
