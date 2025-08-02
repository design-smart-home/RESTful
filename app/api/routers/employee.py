from fastapi import APIRouter, Depends, status

from app.api.routers.dependencies import get_employee_service
from app.core.security.auth import get_current_employee_from_token
from app.services.employee import EmployeeService
from app.api.schemas.employee import (
    CreateEmployeeRequest,
    PatchEmployeeRequest,
    GetEmployeeResponse,
    GetSalaryResponse,
    GetDateOfPromotionResponse, CreateEmployeeResponse,
)
import uuid

employee_router = APIRouter()


@employee_router.get("/salary")
async def get_salary(
    employee=Depends(get_current_employee_from_token),
) -> GetSalaryResponse:
    return GetSalaryResponse(salary=employee.salary)


@employee_router.get("/date_of_promotion")
async def get_date_of_promotion(
    employee=Depends(get_current_employee_from_token),
) -> GetDateOfPromotionResponse:
    return GetDateOfPromotionResponse(date_of_promotion=employee.date_of_promotion)


@employee_router.post("/", status_code=status.HTTP_201_CREATED)
async def post_employee(
    data: CreateEmployeeRequest,
    employee_service: EmployeeService = Depends(get_employee_service),
) -> CreateEmployeeResponse:
    created_employee = await employee_service.create_employee(**data.model_dump())

    return CreateEmployeeResponse(employee_id=created_employee.id)


@employee_router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
    employee_id: uuid.UUID,
    employee_service: EmployeeService = Depends(get_employee_service),
):
    await employee_service.delete_employee_by_id(employee_id)


@employee_router.patch("/{employee_id}", status_code=status.HTTP_200_OK)
async def patch_employee(
    employee_id: uuid.UUID,
    data: PatchEmployeeRequest,
    employee_service: EmployeeService = Depends(get_employee_service),
):
    await employee_service.patch_employee_by_id(employee_id, **data.model_dump())


@employee_router.get("/{employee_id}")
async def get_employee(
    employee_id: uuid.UUID,
    employee_service: EmployeeService = Depends(get_employee_service),
) -> GetEmployeeResponse:
    employee = await employee_service.get_employee_by_id(employee_id)

    return GetEmployeeResponse(
        employee_id=employee.id,
        login=employee.login,
        salary=employee.salary,
        date_of_promotion=employee.date_of_promotion,
    )
