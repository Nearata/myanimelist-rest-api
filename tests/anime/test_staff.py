from fastapi.testclient import TestClient

from . import app


client = TestClient(app)

def test_staff() -> None:
    response = client.get("/anime/1/staff")
    staff = response.json()["staff"][0]

    for i in staff.keys():
        assert type(staff[i]) == str
