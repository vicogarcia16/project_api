from fastapi import Request, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from .exceptions import (
    UnauthorizedException,
    CredentialsException,
    EmailExistsException,
    InternalServerErrorException,
    DatabaseErrorException,
    OpenRouterException,
    TaskNotFoundException
)

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(UnauthorizedException)
    async def handle_unauthorized(request: Request, exc: UnauthorizedException):
        return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

    @app.exception_handler(CredentialsException)
    async def handle_credentials(request: Request, exc: CredentialsException):
        return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

    @app.exception_handler(EmailExistsException)
    async def handle_email_exists(request: Request, exc: EmailExistsException):
        return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

    @app.exception_handler(InternalServerErrorException)
    async def handle_internal_error(request: Request, exc: InternalServerErrorException):
        return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

    @app.exception_handler(DatabaseErrorException)
    async def handle_database_error(request: Request, exc: DatabaseErrorException):
        return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})
    
    @app.exception_handler(OpenRouterException)
    async def handle_openrouter_exception(request: Request, exc: OpenRouterException):
        return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

    @app.exception_handler(TaskNotFoundException)
    async def handle_task_not_found(request: Request, exc: TaskNotFoundException):
        return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})
    
    # 🔥 Manejo global de HTTPException
    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail or "HTTP error"}
        )

    # 🔥 Manejo global de errores inesperados
    @app.exception_handler(Exception)
    async def handle_general_exception(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal Server Error"}
        )
