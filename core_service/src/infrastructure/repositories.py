from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.models import Employee, AccessLog, AccessStatus
import uuid

class AccessRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_employee_by_face_id(self, face_id: str) -> Employee | None:
        query = select(Employee).where(Employee.face_id == face_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def log_attempt(self, 
                          terminal_id: int, 
                          status: AccessStatus, 
                          liveness: float,
                          employee_id: uuid.UUID | None = None):
        
        log_entry = AccessLog(
            terminal_id=terminal_id,
            employee_id=employee_id,
            status=status,
            liveness_score=liveness
        )
        self.db.add(log_entry)
        await self.db.commit()
        return log_entry

    async def create_employee(self, name: str, face_id: str, position: str):
        emp = Employee(full_name=name, face_id=face_id, position=position)
        self.db.add(emp)
        await self.db.commit()
        return emp