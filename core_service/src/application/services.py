from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.repositories import AccessRepository
from src.domain.schemas import AccessRequest, AccessResponse
from src.domain.models import AccessStatus
from datetime import datetime

class AccessControlService:
    def __init__(self, db: AsyncSession):
        self.repo = AccessRepository(db)

    async def validate_entry(self, request: AccessRequest) -> AccessResponse:
        if request.liveness_score < 0.8:
            await self.repo.log_attempt(
                terminal_id=request.terminal_id,
                status=AccessStatus.SPOOFING,
                liveness=request.liveness_score
            )
            return AccessResponse(
                access_granted=False,
                message="SPOOFING DETECTED: Fake face",
                timestamp=datetime.utcnow()
            )

        employee = await self.repo.get_employee_by_face_id(request.face_id)
        
        if not employee:
            await self.repo.log_attempt(
                terminal_id=request.terminal_id,
                status=AccessStatus.DENIED,
                liveness=request.liveness_score
            )
            return AccessResponse(
                access_granted=False,
                message="Access Denied: Unknown person",
                timestamp=datetime.utcnow()
            )

        await self.repo.log_attempt(
            terminal_id=request.terminal_id,
            status=AccessStatus.SUCCESS,
            liveness=request.liveness_score,
            employee_id=employee.id
        )
        
        return AccessResponse(
            access_granted=True,
            employee_name=employee.full_name,
            message=f"Welcome, {employee.full_name}",
            timestamp=datetime.utcnow()
        )

    async def register_employee(self, name: str, face_id: str, pos: str):
        return await self.repo.create_employee(name, face_id, pos)