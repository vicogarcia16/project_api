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

    class Config:
        env_file = ".env"
        extra = "ignore"
    
    @property
    def api_prefix(self) -> str:
        return f"/api/v{self.API_VERSION}"

@lru_cache
def get_settings():
    return Settings()
