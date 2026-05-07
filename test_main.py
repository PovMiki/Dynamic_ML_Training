import pytest
from fastapi.testclient import TestClient
from main import app  # załóżmy, że Twoje API jest w pliku main.py

client = TestClient(app)


def test_predictions_not_none():
    response = client.post("/predict", json={"hours": 5.0})
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_score"] is not None


def test_predictions_length():
    hours_to_test = [1.0, 2.0, 3.0]
    results = []
    for h in hours_to_test:
        response = client.post("/predict", json={"hours": h})
        results.append(response.json()["predicted_score"])

    assert len(results) == len(hours_to_test)
    assert all(isinstance(x, float) for x in results)


def test_predictions_value_range():
    response = client.post("/predict", json={"hours": 10.0})
    data = response.json()
    assert data["predicted_score"] > 0
    response_error = client.post("/predict", json={"hours": -1.0})
    assert response_error.status_code == 400


def test_model_accuracy():
    response = client.post("/predict", json={"hours": 1.0})
    predicted = response.json()["predicted_score"]
    expected = 15.0
    error_margin = abs(predicted - expected) / expected
    assert error_margin < 0.3  #