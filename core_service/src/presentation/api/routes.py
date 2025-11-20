from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.domain.schemas import AccessRequest, AccessResponse, EmployeeCreate
from src.application.services import AccessControlService

router = APIRouter()

def get_service(db: AsyncSession = Depends(get_db)):
    return AccessControlService(db)

@router.post("/check-access", response_model=AccessResponse)
async def check_access(
    request: AccessRequest, 
    service: AccessControlService = Depends(get_service)
):
    """
    Основной метод: принимает ID лица и терминала, возвращает решение о доступе.
    """
    return await service.validate_entry(request)

@router.post("/employees")
async def create_employee(
    data: EmployeeCreate,
    service: AccessControlService = Depends(get_service)
):
    """
    Технический метод для наполнения базы
    """
    await service.register_employee(data.full_name, data.face_id, data.position)
    return {"status": "created"}