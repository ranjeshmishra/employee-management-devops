
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import get_db
from models import Base, Employee


engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def override_get_db():
    with TestingSessionLocal() as db:
        yield db


def test_get_employees_from_database():
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as db:
        db.add(
            Employee(
                name="Test Employee",
                department="DevOps",
                salary=60000,
            )
        )
        db.commit()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            response = client.get("/api/employees")

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 1
        assert data[0]["name"] == "Test Employee"
        assert data[0]["department"] == "DevOps"
        assert data[0]["salary"] == 60000

    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)

def test_get_employee_by_id_from_database():
    Base.metadata.create_all(bind=engine)

    try:
        with TestingSessionLocal() as db:
            employee = Employee(
                name="Priya Singh",
                department="HR",
                salary=40000,
            )
            db.add(employee)
            db.commit()
            db.refresh(employee)
            employee_id = employee.id

        app.dependency_overrides[get_db] = override_get_db

        with TestClient(app) as client:
            response = client.get(
                f"/api/employees/{employee_id}"
            )
            missing_response = client.get(
                "/api/employees/99999"
            )

        assert response.status_code == 200
        assert response.json()["name"] == "Priya Singh"
        assert response.json()["department"] == "HR"
        assert response.json()["salary"] == 40000

        assert missing_response.status_code == 404
        assert missing_response.json() == {
            "detail": "Employee not found"
        }

    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(bind=engine)


def test_create_employee_in_database():
    Base.metadata.create_all(bind=engine)

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/employees",
                json={
                    "name": "Ravi Kumar",
                    "department": "DevOps",
                    "salary": 70000,
                },
            )

            assert response.status_code == 201

            data = response.json()

            assert isinstance(data["id"], int)
            assert data["name"] == "Ravi Kumar"
            assert data["department"] == "DevOps"
            assert data["salary"] == 70000

            employee_id = data["id"]

            get_response = client.get(
                f"/api/employees/{employee_id}"
            )

            assert get_response.status_code == 200
            assert get_response.json() == data

        with TestingSessionLocal() as db:
            saved_employee = db.get(Employee, employee_id)

            assert saved_employee is not None
            assert saved_employee.name == "Ravi Kumar"

    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(bind=engine)


def test_update_employee_in_database():
    Base.metadata.create_all(bind=engine)

    try:
        with TestingSessionLocal() as db:
            employee = Employee(
                name="Amit Sharma",
                department="IT",
                salary=45000,
            )
            db.add(employee)
            db.commit()
            db.refresh(employee)
            employee_id = employee.id

        app.dependency_overrides[get_db] = override_get_db

        with TestClient(app) as client:
            response = client.put(
                f"/api/employees/{employee_id}",
                json={
                    "name": "Amit Sharma",
                    "department": "Cloud Engineering",
                    "salary": 90000,
                },
            )

            assert response.status_code == 200

            data = response.json()

            assert data["id"] == employee_id
            assert data["name"] == "Amit Sharma"
            assert data["department"] == "Cloud Engineering"
            assert data["salary"] == 90000

            get_response = client.get(
                f"/api/employees/{employee_id}"
            )

            assert get_response.status_code == 200
            assert get_response.json() == data

            missing_response = client.put(
                "/api/employees/99999",
                json={
                    "name": "Missing Employee",
                    "department": "IT",
                    "salary": 50000,
                },
            )

            assert missing_response.status_code == 404
            assert missing_response.json() == {
                "detail": "Employee not found"
            }

        with TestingSessionLocal() as db:
            saved_employee = db.get(Employee, employee_id)

            assert saved_employee is not None
            assert saved_employee.department == "Cloud Engineering"
            assert saved_employee.salary == 90000

    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(bind=engine)

def test_delete_employee_in_database():
    Base.metadata.create_all(bind=engine)

    try:
        with TestingSessionLocal() as db:
            employee = Employee(
                name="Rahul Verma",
                department="Finance",
                salary=50000,
            )

            db.add(employee)
            db.commit()
            db.refresh(employee)

            employee_id = employee.id

        app.dependency_overrides[get_db] = override_get_db

        with TestClient(app) as client:
            response = client.delete(
                f"/api/employees/{employee_id}"
            )

            assert response.status_code == 200
            assert response.json() == {
                "message": "Employee deleted successfully",
                "employee_id": employee_id,
            }

            get_response = client.get(
                f"/api/employees/{employee_id}"
            )

            assert get_response.status_code == 404

            second_delete = client.delete(
                f"/api/employees/{employee_id}"
            )

            assert second_delete.status_code == 404

        with TestingSessionLocal() as db:
            deleted_employee = db.get(
                Employee,
                employee_id,
            )

            assert deleted_employee is None

    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(bind=engine)
