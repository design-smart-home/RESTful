from app.core.exceptions import EmployeeNotFoundError
from app.db.repositories.employee import EmployeeRepository
from app.db.models.employee import Employee
from app.core.security.hashing import Hasher
from uuid import UUID
from datetime import date


class EmployeeService:
    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    async def create_employee(
        self, login: str, password: str, salary: int, date_of_promotion: date
    ) -> Employee:
        hashed_password = Hasher().get_password_hash(password)
        created_employee = await self.repository.create_employee(
            login=login,
            hashed_password=hashed_password,
            salary=salary,
            date_of_promotion=date_of_promotion,
        )

        return created_employee

    async def delete_employee_by_id(self, employee_id: UUID) -> None:
        await self.repository.delete_employee_by_id(employee_id)

    async def patch_employee_by_id(
        self, employee_id: UUID, **data_to_patch
    ) -> Employee:
        if "password" in data_to_patch and data_to_patch["password"]:
            data_to_patch["hashed_password"] = Hasher().get_password_hash(
                data_to_patch["password"]
            )
            data_to_patch.pop("password")
        else:
            data_to_patch.pop("password")

        patched_employee = await self.repository.patch_employee_by_id(
            employee_id, **data_to_patch
        )

        if not patched_employee:
            raise EmployeeNotFoundError(f"Employee with id {employee_id} not found")

        return patched_employee

    async def get_employee_by_id(self, employee_id: UUID) -> Employee:
        employee = await self.repository.get_employee_by_id(employee_id)

        if not employee:
            raise EmployeeNotFoundError(f"Employee with id {employee_id} not found")

        return employee
