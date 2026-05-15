from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chargers_endpoint_returns_charger_list():
    response = client.get("/chargers")

    assert response.status_code == 200
    assert "chargers" in response.json()
    assert len(response.json()["chargers"]) >= 1


def test_recommend_endpoint_returns_recommendation():
    response = client.get(
        "/recommend",
        params={
            "distance_km": 2,
            "availability": 5,
            "congestion": 0.2
        }
    )

    assert response.status_code == 200
    assert "recommendation" in response.json()
    assert "score" in response.json()


def test_recommend_endpoint_rejects_invalid_input():
    response = client.get(
        "/recommend",
        params={
            "distance_km": -1,
            "availability": 5,
            "congestion": 0.2
        }
    )

    assert response.status_code == 400


def test_predict_congestion_endpoint_returns_prediction():
    response = client.get(
        "/predict-congestion",
        params={
            "current_usage": 8,
            "charger_capacity": 10
        }
    )

    assert response.status_code == 200
    assert response.json()["congestion_level"] == "High"


def test_predict_congestion_endpoint_rejects_invalid_capacity():
    response = client.get(
        "/predict-congestion",
        params={
            "current_usage": 8,
            "charger_capacity": 0
        }
    )

    assert response.status_code == 400
