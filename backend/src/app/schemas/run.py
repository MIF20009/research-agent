from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class RunCreate(BaseModel):
    topic: str = Field(..., min_length=3, max_length=300)
    notes: Optional[str] = None

class RunOut(BaseModel):
    id: int
    topic: str
    status: str
    notes: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True