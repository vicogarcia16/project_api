from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Task title",
                "description": "Task description"
            }
        }
    }
    
class TaskDisplay(BaseModel):
    id: str
    title: str
    description: Optional[str]
    user_id: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TaskResponse(BaseModel):
    message: str
    data: TaskDisplay
    
class TaskListResponse(BaseModel):
    message: str
    data: List[TaskDisplay]