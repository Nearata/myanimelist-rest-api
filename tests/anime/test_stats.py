from fastapi.testclient import TestClient

from mal.main import create_app


app = create_app()
client = TestClient(app)

def test_stats() -> None:
    response = client.get("/anime/1/stats")
    stats = response.json()

    summary = stats["summary"]
    for i in summary.keys():
        assert type(summary[i]) == int

    scores = stats["scores"]
    for i in scores.keys():
        assert type(scores[i]["percentage"]) == float
        assert type(scores[i]["votes"]) == int
