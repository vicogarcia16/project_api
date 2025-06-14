from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime

class TaskCreate(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Comprar comida",
                "description": "Descripción opcional, si no se provee se genera con IA"
            }
        }
    }
    
class TaskDisplay(BaseModel):
    id: str
    title: str
    description: Optional[str]
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TaskResponse(BaseModel):
    message: str
    data: TaskDisplay
    
class TaskListResponse(BaseModel):
    message: str
    data: List[TaskDisplay]