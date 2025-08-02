from pydantic import BaseModel, Field
from datetime import date

import uuid


class CreateEmployeeRequest(BaseModel):
    login: str
    password: str = Field(min_length=8, max_length=20)
    salary: int
    date_of_promotion: date


class CreateEmployeeResponse(BaseModel):
    employee_id: uuid.UUID


class PatchEmployeeRequest(BaseModel):
    login: str | None = None
    password: str | None = None
    salary: int | None = None
    date_of_promotion: date | None = None


class GetEmployeeResponse(BaseModel):
    employee_id: uuid.UUID
    login: str
    salary: int
    date_of_promotion: date


class GetSalaryResponse(BaseModel):
    salary: int


class GetDateOfPromotionResponse(BaseModel):
    date_of_promotion: date
