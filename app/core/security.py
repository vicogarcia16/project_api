from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
import secrets
from app.core.config import get_settings

settings = get_settings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(expires_delta: timedelta = timedelta(days=7)):
    token = secrets.token_urlsafe(36)
    expires_at = datetime.now() + expires_delta
    expires_at = expires_at.replace(microsecond=0)
    return token, expires_at

