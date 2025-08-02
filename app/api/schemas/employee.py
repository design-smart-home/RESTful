from pydantic import BaseModel, Field
from datetime import date

import uuid

# id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
# login: Mapped[str] = mapped_column(String(60), nullable=False)
# hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
# salary: Mapped[int] = mapped_column(Integer, nullable=False)
# date_of_promotion: Mapped[date] = mapped_column(Date)


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
