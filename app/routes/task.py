from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from app.db.database import get_db
from app.models.models import Task
from app.middleware.jwt_bearer import verify_token
from app.schemas.task import TaskCreate, TaskResponse, TaskListResponse
from app.core.exceptions import TaskNotFoundException
from app.services.openrouter_service import generate_task_description
from app.helpers.task_helper import get_all_tasks_by_user, get_user_task_or_none

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=TaskListResponse)
async def get_tasks(db: AsyncSession = Depends(get_db), user: dict = Depends(verify_token)):
    tasks = await get_all_tasks_by_user(db, user["user_id"])
    return TaskListResponse(message="Get tasks successfully", data=tasks)

@router.get("/{task_id}/", response_model=TaskResponse)
async def get_task(task_id: str, db: AsyncSession = Depends(get_db), 
                   user: dict = Depends(verify_token)):
    task = await get_user_task_or_none(db, user["user_id"], task_id)
    if not task:
        raise TaskNotFoundException()

    return TaskResponse(message="Get task successfully", data=task)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(verify_token),
):
    description = await generate_task_description(task_create.title)
    new_task = Task(
        id=str(uuid4()),
        title=task_create.title,
        description=description,
        user_id=user["user_id"],
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    return TaskResponse(message="Create task successfully", data=new_task)

@router.patch("/{task_id}/", response_model=TaskResponse)
async def regenerate_description(task_id: str, db: AsyncSession = Depends(get_db), 
                                 user: dict = Depends(verify_token)):
    task = await get_user_task_or_none(db, user["user_id"], task_id)
    if not task:
        raise TaskNotFoundException()
    description = await generate_task_description(task.title)
    task.description = description
    await db.commit()
    await db.refresh(task)

    return TaskResponse(message="Regenerate description successfully", data=task)

@router.delete("/{task_id}/")
async def delete_task(task_id: str, db: AsyncSession = Depends(get_db), 
                      user: dict = Depends(verify_token)):
    task = await get_user_task_or_none(db, user["user_id"], task_id)
    if not task:
        raise TaskNotFoundException()
    await db.delete(task)
    await db.commit()
    
    return {"message": "Delete task successfully"}