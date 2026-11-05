from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Skill
from app.schemas.skill import SkillCreate


async def get_skills(session: AsyncSession) -> list[Skill]:
    """Возвращает все навыки"""
    result = await session.scalars(select(Skill).order_by(Skill.name))
    return list(result)


async def get_skill(session: AsyncSession, skill_id: int) -> Skill | None:
    """Возвращает навык по id или None"""
    return await session.get(Skill, skill_id)


async def get_skill_by_name(session: AsyncSession, name: str) -> Skill | None:
    """Ищет навык по названию"""
    return await session.scalar(select(Skill).where(Skill.name == name))


async def create_skill(session: AsyncSession, data: SkillCreate) -> Skill:
    """Создаёт навык"""
    skill = Skill(name=data.name)
    session.add(skill)
    await session.commit()
    await session.refresh(skill)
    return skill


async def update_skill(session: AsyncSession, skill: Skill, data: SkillCreate) -> Skill:
    """Меняет название навыка"""
    skill.name = data.name
    await session.commit()
    await session.refresh(skill)
    return skill


async def delete_skill(session: AsyncSession, skill: Skill) -> None:
    """Удаляет навык"""
    await session.delete(skill)
    await session.commit()
