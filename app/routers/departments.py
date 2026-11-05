from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.core.database import SessionDep
from app.schemas.department import DepartmentCreate, DepartmentRead
from app.services import department as service

router = APIRouter(prefix="/departments", tags=["Отделы"])


@router.get("/", response_model=list[DepartmentRead])
async def list_departments(session: SessionDep):
    """Список всех отделов"""
    return await service.get_departments(session)


@router.get("/{department_id}", response_model=DepartmentRead)
async def read_department(department_id: int, session: SessionDep):
    """Отдел по id"""
    department = await service.get_department(session, department_id)
    if department is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Отдел не найден")
    return department


@router.post("/", response_model=DepartmentRead, status_code=status.HTTP_201_CREATED)
async def create_department(data: DepartmentCreate, session: SessionDep):
    """Создание отдела"""
    if await service.get_department_by_name(session, data.name):
        raise HTTPException(status.HTTP_409_CONFLICT, "Такой отдел уже есть")
    return await service.create_department(session, data)


@router.put("/{department_id}", response_model=DepartmentRead)
async def update_department(
    department_id: int, data: DepartmentCreate, session: SessionDep
):
    """Изменение названия отдела"""
    department = await service.get_department(session, department_id)
    if department is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Отдел не найден")
    existing = await service.get_department_by_name(session, data.name)
    if existing and existing.id != department_id:
        raise HTTPException(status.HTTP_409_CONFLICT, "Такой отдел уже есть")
    return await service.update_department(session, department, data)


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(department_id: int, session: SessionDep) -> None:
    """Удаление отдела"""
    department = await service.get_department(session, department_id)
    if department is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Отдел не найден")
    try:
        await service.delete_department(session, department)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, "В отделе есть сотрудники или вакансии"
        )
