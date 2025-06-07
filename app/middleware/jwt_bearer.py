from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime, timezone
from app.core.config import get_settings
from app.core.exceptions import UnauthorizedException

settings = get_settings()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

security = HTTPBearer(auto_error=False)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """ Verifica el token y devuelve los datos del usuario autenticado. """
    if not credentials:
        raise UnauthorizedException('No token provided')
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expiration_time = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)
        if datetime.now(timezone.utc) > expiration_time:
            raise UnauthorizedException("Token expired")
        return payload
    except JWTError:
        raise UnauthorizedException('Invalid token')
        
    
        