from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from datetime import datetime
from typing import List

class User(Base):
    __tablename__ = "users_practice"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    refresh_token: Mapped[str] = mapped_column(nullable=True)
    refresh_token_expires_at: Mapped[datetime] = mapped_column(nullable=True)
    
    tasks: Mapped[List["Task"]] = relationship(back_populates="user", cascade="all, delete")
    
class Task(Base):
    __tablename__ = "tasks_practice"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users_practice.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    
    user: Mapped[User] = relationship(back_populates="tasks")