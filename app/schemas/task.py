from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime

class TaskCreate(BaseModel):
    title: str = Field(..., max_length=100)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Saber cómo declarar una variable en Python"
            }
        }
    }
    
class TaskDisplay(BaseModel):
    id: str
    title: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TaskResponse(BaseModel):
    message: str
    data: TaskDisplay
    
class TaskListResponse(BaseModel):
    message: str
    data: List[TaskDisplay]