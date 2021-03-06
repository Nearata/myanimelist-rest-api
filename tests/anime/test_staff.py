from fastapi.testclient import TestClient

from mal.main import create_app
from mal.config import Config


app = create_app()
client = TestClient(app)

def test_staff() -> None:
    Config.CACHE = False

    response = client.get("/anime/1/staff")
    staff = response.json()["staff"][0]

    for i in staff.keys():
        assert type(staff[i]) == str
