from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.auth import Token
from app.core.security.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security.auth import authenticate_employee
from app.core.config import settings
from app.db.session import get_db


login_router = APIRouter()

SECRET_KEY: str = settings.SECRET_KEY
ALGORITHM: str = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES


@login_router.post("/token/{employee_id}", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> Token:
    employee = await authenticate_employee(form_data.username, form_data.password, db)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"login": employee.login, "password": employee.hashed_password},
        expires_delta=access_token_expires,
    )

    return Token(access_token=access_token, token_type="bearer")
