from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    BACKEND_CORS_ORIGINS: List[str]
    API_VERSION: str = "1"
    OPENROUTER_API_KEY: str
    OPENROUTER_MODEL: str

    class Config:
        env_file = ".env"
        extra = "ignore"
    
    @property
    def api_prefix(self) -> str:
        return f"/api/v{self.API_VERSION}"
    
    @property
    def user_agent(self) -> str:
        app_name = "taskgen-fastapi"
        return f"{app_name}/{self.API_VERSION}.0.0"

@lru_cache
def get_settings():
    return Settings()
