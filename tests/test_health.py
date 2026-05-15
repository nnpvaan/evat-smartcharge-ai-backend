from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint_returns_welcome_message():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to EVAT SmartCharge AI Backend API"  # noqa: E501


def test_health_endpoint_returns_healthy_status():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_metrics_endpoint_returns_prometheus_metrics():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "evat_request_total" in response.text
