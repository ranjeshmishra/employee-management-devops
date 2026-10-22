from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy import select
from database import SessionLocal
from models import Employee
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field



app = FastAPI(
    title="Employee Management API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Employee Management API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# Temporary employee data stored in memory
employees = [
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
]




@app.get("/api/employees")
def get_employees(db: Session = Depends(get_db)):
    result = db.scalars(
        select(Employee).order_by(Employee.id)
    ).all()

    return [
        {
            "id": employee.id,
            "name": employee.name,
            "department": employee.department,
            "salary": employee.salary,
        }
        for employee in result
    ]




@app.get("/api/employees/{employee_id}")
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
):
    employee = db.get(Employee, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return {
        "id": employee.id,
        "name": employee.name,
        "department": employee.department,
        "salary": employee.salary,
    }



class EmployeeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    department: str = Field(min_length=2, max_length=50)
    salary: int = Field(gt=0)



@app.post("/api/employees", status_code=status.HTTP_201_CREATED)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
):
    new_employee = Employee(
        name=employee.name,
        department=employee.department,
        salary=employee.salary,
    )

    db.add(new_employee)

    try:
        db.commit()
        db.refresh(new_employee)
    except Exception:
        db.rollback()
        raise

    return {
        "id": new_employee.id,
        "name": new_employee.name,
        "department": new_employee.department,
        "salary": new_employee.salary,
    }



@app.put("/api/employees/{employee_id}")
def update_employee(
    employee_id: int,
    updated_data: EmployeeCreate,
    db: Session = Depends(get_db),
):
    employee = db.get(Employee, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    employee.name = updated_data.name
    employee.department = updated_data.department
    employee.salary = updated_data.salary

    try:
        db.commit()
        db.refresh(employee)
    except Exception:
        db.rollback()
        raise

    return {
        "id": employee.id,
        "name": employee.name,
        "department": employee.department,
        "salary": employee.salary,
    }



@app.delete("/api/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
):
    employee = db.get(Employee, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    try:
        db.delete(employee)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return {
        "message": "Employee deleted successfully",
        "employee_id": employee_id,
    }
