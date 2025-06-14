from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Task
from sqlalchemy.future import select    
from typing import List

async def get_all_tasks_by_user(db: AsyncSession, user_id: str) -> List[Task]:
    query = select(Task).where(Task.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()

async def get_user_task_or_none(db: AsyncSession, user_id: str, task_id: str) -> Task:
    query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()
