from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Department
from app.schemas.department import DepartmentCreate


async def get_departments(session: AsyncSession) -> list[Department]:
    """Возвращает все отделы"""
    result = await session.scalars(select(Department).order_by(Department.id))
    return list(result)


async def get_department(
    session: AsyncSession, department_id: int
) -> Department | None:
    """Возвращает отдел по id или None"""
    return await session.get(Department, department_id)


async def get_department_by_name(session: AsyncSession, name: str) -> Department | None:
    """Ищет отдел по названию"""
    return await session.scalar(select(Department).where(Department.name == name))


async def create_department(
    session: AsyncSession, data: DepartmentCreate
) -> Department:
    """Создаёт отдел"""
    department = Department(name=data.name)
    session.add(department)
    await session.commit()
    await session.refresh(department)
    return department


async def update_department(
    session: AsyncSession, department: Department, data: DepartmentCreate
) -> Department:
    """Меняет название отдела"""
    department.name = data.name
    await session.commit()
    await session.refresh(department)
    return department


async def delete_department(session: AsyncSession, department: Department) -> None:
    """Удаляет отдел"""
    await session.delete(department)
    await session.commit()
