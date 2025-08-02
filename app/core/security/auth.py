from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security.hashing import Hasher
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from jose import jwt, JWTError
from app.db.models.employee import Employee
from app.db.session import get_db
from app.db.repositories.employee import EmployeeRepository
from app.core.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")
SECRET_KEY: str = settings.SECRET_KEY
ALGORITHM: str = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES


async def _get_employee_by_login_for_auth(
    employee_login: str, db: AsyncSession
) -> Employee | None:
    async with db.begin():
        employee_repo = EmployeeRepository(db)
        return await employee_repo.get_employee_by_login(employee_login=employee_login)


async def authenticate_employee(
    login: str, password: str, db: AsyncSession
) -> Employee | None:
    employee = await _get_employee_by_login_for_auth(login, db)

    if (
        employee is not None
        and Hasher.verify_password(password, employee.hashed_password)
        and login == employee.login
    ):
        return employee

    return None


async def get_current_employee_from_token(
    token: str, db: AsyncSession = Depends(get_db)
) -> Employee:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("login")
    except JWTError:
        raise credentials_exception

    employee = await _get_employee_by_login_for_auth(login, db)
    if employee is None:
        raise credentials_exception

    return employee
