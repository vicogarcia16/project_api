from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "tD4b3@project.com",
                "password": "password123"
            }
        }
    }

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "tD4b3@project.com",
                "password": "password123"
            }
        }
    }
    
class UserDisplay(BaseModel):
    id: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class AuthResponse(BaseModel):
    token: str
    refresh_token: str
    user: UserDisplay
    
    
    