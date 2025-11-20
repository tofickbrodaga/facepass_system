from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from src.domain.models import AccessStatus


class AccessRequest(BaseModel):
    face_id: str
    terminal_id: int
    liveness_score: float
    snapshot_url: Optional[str] = None


class AccessResponse(BaseModel):
    access_granted: bool
    employee_name: Optional[str] = None
    message: str
    timestamp: datetime


class EmployeeCreate(BaseModel):
    full_name: str
    face_id: str
    position: str