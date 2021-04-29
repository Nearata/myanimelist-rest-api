from fastapi.testclient import TestClient

from mal.main import create_app


app = create_app()
client = TestClient(app)

def test_reviews() -> None:
    response = client.get("/anime/1/reviews/1")
    review = response.json()["reviews"][0]

    assert type(review["date"]) == str
    assert type(review["helpful_count"]) == int
    assert type(review["url"]) == str

    reviewer = review["reviewer"]
    assert type(reviewer["profile_url"]) == str
    assert type(reviewer["image_url"]) == str
    assert type(reviewer["username"]) == str

    reviewer_scores = reviewer["scores"]
    for i in reviewer_scores.keys():
        assert type(reviewer_scores[i]) == int
