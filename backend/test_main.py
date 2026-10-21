import pytest
from fastapi.testclient import TestClient
from main import app, employees

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_employee_data():
    employees.clear()

    employees.extend([
        {
            "id": 1,
            "name": "Amit Sharma",
            "department": "IT",
            "salary": 45000
        },
        {
            "id": 2,
            "name": "Priya Singh",
            "department": "HR",
            "salary": 40000
        },
        {
            "id": 3,
            "name": "Rahul Verma",
            "department": "Finance",
            "salary": 50000
        }
    ])

    yield





def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_employees():
    response = client.get("/api/employees")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 3

    assert data[0]["id"] == 1
    assert data[0]["name"] == "Amit Sharma"
    assert data[0]["department"] == "IT"
    assert data[0]["salary"] == 45000


def test_create_employee():
    new_employee = {
        "name": "Ravi Kumar",
        "department": "DevOps",
        "salary": 70000
    }

    response = client.post(
        "/api/employees",
        json=new_employee
    )

    assert response.status_code == 201

    data = response.json()

    assert isinstance(data["id"], int)
    assert data["name"] == "Ravi Kumar"
    assert data["department"] == "DevOps"
    assert data["salary"] == 70000

    # Verify the employee can be retrieved
    employee_id = data["id"]

    get_response = client.get(
        f"/api/employees/{employee_id}"
    )

    assert get_response.status_code == 200
    assert get_response.json() == data


def test_create_employee_invalid_salary():
    invalid_employee = {
        "name": "Test Employee",
        "department": "IT",
        "salary": -500
    }

    response = client.post(
        "/api/employees",
        json=invalid_employee
    )

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data

    assert any(
        "salary" in str(error["loc"])
        for error in data["detail"]
    )


def test_update_employee():
    updated_employee = {
        "name": "Amit Sharma",
        "department": "Cloud Engineering",
        "salary": 90000
    }

    response = client.put(
        "/api/employees/1",
        json=updated_employee
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Amit Sharma"
    assert data["department"] == "Cloud Engineering"
    assert data["salary"] == 90000

    # Verify the updated data using GET
    get_response = client.get("/api/employees/1")

    assert get_response.status_code == 200
    assert get_response.json() == data


def test_delete_employee():
    # Step 1: Delete employee ID 3
    response = client.delete("/api/employees/3")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Employee deleted successfully"
    assert data["employee_id"] == 3

    # Step 2: Verify employee no longer exists
    get_response = client.get("/api/employees/3")

    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": "Employee not found"
    }

    # Step 3: Try deleting the same employee again
    delete_again = client.delete("/api/employees/3")

    assert delete_again.status_code == 404
