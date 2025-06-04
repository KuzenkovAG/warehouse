from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


class BaseHTTPError(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    msg: str = "Internal Server Error"


class AbsentMovementError(BaseHTTPError):
    status_code: int = status.HTTP_404_NOT_FOUND
    msg: str = "Absent movement"


class AbsentProductError(BaseHTTPError):
    status_code: int = status.HTTP_404_NOT_FOUND
    msg: str = "Absent product information"


def set_exceptions_handler(app: FastAPI) -> None:
    @app.exception_handler(BaseHTTPError)
    async def invalid_exception_handler(request: Request, exc: BaseHTTPError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.msg,
        )

    @app.exception_handler(Exception)
    async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error",
        )
