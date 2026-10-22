
from fastapi.testclient import TestClient

from main import app


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_employee_invalid_salary():
    with TestClient(app) as client:
        response = client.post(
            "/api/employees",
            json={
                "name": "Test Employee",
                "department": "DevOps",
                "salary": -500,
            },
        )

    assert response.status_code == 422

    errors = response.json()["detail"]
    assert any("salary" in error["loc"] for error in errors)
