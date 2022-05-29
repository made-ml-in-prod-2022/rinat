import pytest
from starlette.testclient import TestClient

from app import app


FEATURE_NAMES = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
DATA = [65.0, 1.0, 0.0, 138.0, 282.0, 1.0, 2.0, 174.0, 0.0, 1.4, 1.0, 1.0, 0.0]


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_service_reply_to_root_path(client):
    response = client.get("/")
    assert 200 == response.status_code


def test_health(client):
    response = client.get("/health")
    assert 200 == response.status_code


def test_predict_request(client):
    response = client.get("predict/", json={"data": [DATA], "feature_names": FEATURE_NAMES})
    assert 200 == response.status_code
    assert len(response.json()) != 0


def test_predict_request_no_data(client):
    response = client.get("/predict/", json={"data": [], "feature_names": FEATURE_NAMES})
    assert response.status_code == 400
    assert "empty" in response.json()["detail"]