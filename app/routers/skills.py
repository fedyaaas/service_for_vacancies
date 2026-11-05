from fastapi import APIRouter, HTTPException, status

from app.core.database import SessionDep
from app.core.deps import AdminUser
from app.schemas.skill import SkillCreate, SkillRead
from app.services import skill as service

router = APIRouter(prefix="/skills", tags=["Навыки"])


@router.get("/", response_model=list[SkillRead])
async def list_skills(session: SessionDep):
    """Список всех навыков"""
    return await service.get_skills(session)


@router.get("/{skill_id}", response_model=SkillRead)
async def read_skill(skill_id: int, session: SessionDep):
    """Навык по id"""
    skill = await service.get_skill(session, skill_id)
    if skill is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Навык не найден")
    return skill


@router.post("/", response_model=SkillRead, status_code=status.HTTP_201_CREATED)
async def create_skill(data: SkillCreate, session: SessionDep, _: AdminUser):
    """Создание навыка, только для админа"""
    if await service.get_skill_by_name(session, data.name):
        raise HTTPException(status.HTTP_409_CONFLICT, "Такой навык уже есть")
    return await service.create_skill(session, data)


@router.put("/{skill_id}", response_model=SkillRead)
async def update_skill(
    skill_id: int, data: SkillCreate, session: SessionDep, _: AdminUser
):
    """Изменение названия навыка, только для админа"""
    skill = await service.get_skill(session, skill_id)
    if skill is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Навык не найден")
    existing = await service.get_skill_by_name(session, data.name)
    if existing and existing.id != skill_id:
        raise HTTPException(status.HTTP_409_CONFLICT, "Такой навык уже есть")
    return await service.update_skill(session, skill, data)


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(skill_id: int, session: SessionDep, _: AdminUser) -> None:
    """Удаление навыка, только для админа"""
    skill = await service.get_skill(session, skill_id)
    if skill is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Навык не найден")
    await service.delete_skill(session, skill)
