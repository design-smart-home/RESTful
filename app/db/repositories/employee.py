from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.employee import Employee
from uuid import UUID
from datetime import date


class EmployeeRepository:
    _db: AsyncSession

    def __init__(self, db: AsyncSession):
        self._db = db

    async def create_employee(
        self, login: str, hashed_password: str, salary: int, date_of_promotion: date
    ) -> Employee:
        employee = Employee(
            login=login,
            hashed_password=hashed_password,
            salary=salary,
            date_of_promotion=date_of_promotion,
        )

        self._db.add(employee)
        await self._db.flush()

        return employee

    async def delete_employee_by_id(self, employee_id: UUID) -> None:
        employee_to_delete = await self.get_employee_by_id(employee_id)

        await self._db.delete(employee_to_delete)

    async def patch_employee_by_id(
        self,
        employee_id: UUID,
        login: str | None = None,
        hashed_password: str | None = None,
        salary: int | None = None,
        date_of_promotion: date | None = None,
    ) -> Employee | None:
        updated_employee = await self.get_employee_by_id(employee_id)

        if not updated_employee:
            return None

        if login:
            updated_employee.login = login
        if hashed_password:
            updated_employee.hashed_password = hashed_password
        if salary:
            updated_employee.salary = salary
        if date_of_promotion:
            updated_employee.date_of_promotion = date_of_promotion

        return updated_employee

    async def get_employee_by_id(self, employee_id: UUID) -> Employee | None:
        employee = await self._db.scalar(
            select(Employee).where(Employee.id == employee_id)
        )

        return employee

    async def get_employee_by_login(self, employee_login: str) -> Employee | None:
        employee = await self._db.scalar(
            select(Employee).where(Employee.login == employee_login)
        )

        return employee
