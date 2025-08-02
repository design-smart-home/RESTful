from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.session import get_db
from app.db.repositories.employee import EmployeeRepository
from app.services.employee import EmployeeService


def get_employee_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> EmployeeRepository:
    return EmployeeRepository(db)


def get_employee_service(
    repository: Annotated[EmployeeRepository, Depends(get_employee_repository)],
):
    return EmployeeService(repository)
