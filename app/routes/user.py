from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, AuthResponse, UserDisplay
from app.middleware.jwt_bearer import verify_token
import uuid
from datetime import datetime
from app.core.exceptions import (
    InternalServerErrorException,
    CredentialsException,
    EmailExistsException,
    DatabaseErrorException,
)
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/register/")
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalars().first()

    if existing_user:
        raise EmailExistsException()
    try:
        user_id = str(uuid.uuid4())
        token = create_access_token({"user_id": user_id})
        refresh_token, refresh_token_expires_at = create_refresh_token()

        new_user = User(
            id=user_id,
            email=user_data.email,
            password=hash_password(user_data.password),
            refresh_token=refresh_token,
            refresh_token_expires_at=refresh_token_expires_at,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return {
            "message": "User registered successfully",
            "data": AuthResponse(
                token=token,
                refresh_token=refresh_token,
                user=UserDisplay(id=new_user.id, email=new_user.email),
            ).model_dump(),
        }
    except SQLAlchemyError:
        raise DatabaseErrorException()
    except Exception as e:
        raise InternalServerErrorException(str(e))


@router.post("/login/")
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalars().first()
    if not user or not verify_password(user_data.password, user.password):
        raise CredentialsException()
    try:
        token = create_access_token({"user_id": user.id})
        refresh_token, refresh_token_expires_at = create_refresh_token()

        user.refresh_token = refresh_token
        user.refresh_token_expires_at = refresh_token_expires_at
        await db.commit()
        await db.refresh(user)
        return {
            "message": "Login successful",
            "data": AuthResponse(
                token=token,
                refresh_token=refresh_token,
                user=UserDisplay(id=user.id, email=user.email),
            ).model_dump(),
        }
    except SQLAlchemyError:
        raise DatabaseErrorException()
    except Exception as e:
        raise InternalServerErrorException(str(e))


@router.post("/refresh-token/")
async def refresh_token(
    refresh_token: str = Query(...), db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(User).where(User.refresh_token == refresh_token)
        )
        user = result.scalars().first()

        if not user:
            raise CredentialsException("Invalid refresh token")

        if (
            user.refresh_token_expires_at
            and user.refresh_token_expires_at < datetime.now().replace(microsecond=0)
        ):
            raise CredentialsException("Refresh token expired")
        new_access_token = create_access_token({"user_id": user.id})
        return {"access_token": new_access_token}
    except SQLAlchemyError:
        raise DatabaseErrorException()
    except Exception as e:
        raise InternalServerErrorException(str(e))


@router.post("/logout/")
async def logout(
    user: dict = Depends(verify_token), db: AsyncSession = Depends(get_db)
):
    try:
        user_id = user["user_id"]
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if user:
            user.refresh_token = None
            user.refresh_token_expires_at = None
            await db.commit()
        return {"message": "Logout successful"}
    except SQLAlchemyError:
        raise DatabaseErrorException()
    except Exception as e:
        raise InternalServerErrorException(str(e))
