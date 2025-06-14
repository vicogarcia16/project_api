from fastapi import HTTPException, status

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class CredentialsException(HTTPException):
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class EmailExistsException(HTTPException):
    def __init__(self, detail: str = "Email already exists"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class InternalServerErrorException(HTTPException):
    def __init__(self, error: str = "Something went wrong"):
        detail = f"Internal server error: {error}"
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class DatabaseErrorException(HTTPException):
    def __init__(self, detail: str = "Database error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class OpenRouterException(HTTPException):
    def __init__(self, detail: str = "Error writing description with OpenRouter"):
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)