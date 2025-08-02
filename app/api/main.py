from fastapi import APIRouter

from app.api.routers.employee import employee_router
from app.api.routers.authorization import login_router


main_router = APIRouter()

main_router.include_router(employee_router, prefix="/employee", tags=["employee"])
main_router.include_router(
    login_router, prefix="/authorization", tags=["authorization"]
)
