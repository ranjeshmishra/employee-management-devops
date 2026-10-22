
from sqlalchemy import select

from database import SessionLocal
from models import Employee


def seed_employee():
    with SessionLocal() as db:
        existing = db.scalar(
            select(Employee).where(
                Employee.name == "Amit Sharma",
                Employee.department == "IT",
            )
        )

        if existing:
            print("Employee already exists")
            print("Employee ID:", existing.id)
            return

        employee = Employee(
            name="Amit Sharma",
            department="IT",
            salary=45000,
        )

        db.add(employee)
        db.commit()
        db.refresh(employee)

        print("Employee inserted successfully")
        print("Employee ID:", employee.id)
        print("Name:", employee.name)
        print("Department:", employee.department)
        print("Salary:", employee.salary)


if __name__ == "__main__":
    seed_employee()
