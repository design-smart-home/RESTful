from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.api.main import main_router
import uvicorn
import asyncio

from app.core.exceptions import EmployeeNotFoundError

try:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
except Exception:
    pass

app = FastAPI()

app.include_router(main_router)


@app.exception_handler(EmployeeNotFoundError)
async def employee_not_found_exception_handler(
    request: Request, exception: EmployeeNotFoundError
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exception)}
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
