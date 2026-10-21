
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
def get_employees():
    return employees


@app.get("/api/employees/{employee_id}")
def get_employee(employee_id: int):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    department: str = Field(min_length=2, max_length=50)
    salary: int = Field(gt=0)


@app.post(
    "/api/employees",
    status_code=status.HTTP_201_CREATED
)
def create_employee(employee: EmployeeCreate):
    new_id = max(
        (item["id"] for item in employees),
        default=0
    ) + 1

    new_employee = {
        "id": new_id,
        "name": employee.name,
        "department": employee.department,
        "salary": employee.salary
    }

    employees.append(new_employee)

    return new_employee


@app.put("/api/employees/{employee_id}")
def update_employee(
    employee_id: int,
    updated_data: EmployeeCreate
):
    for employee in employees:
        if employee["id"] == employee_id:
            employee["name"] = updated_data.name
            employee["department"] = updated_data.department
            employee["salary"] = updated_data.salary

            return employee

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )

@app.delete("/api/employees/{employee_id}")
def delete_employee(employee_id: int):
    for employee in employees:
        if employee["id"] == employee_id:
            employees.remove(employee)

            return {
                "message": "Employee deleted successfully",
                "employee_id": employee_id
            }

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )
