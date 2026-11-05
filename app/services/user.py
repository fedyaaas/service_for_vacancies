from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models import User, UserRole
from app.schemas.user import UserCreate


async def get_users(session: AsyncSession) -> list[User]:
    """Возвращает всех пользователей"""
    result = await session.scalars(select(User).order_by(User.id))
    return list(result)


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    """Возвращает пользователя по id или None"""
    return await session.get(User, user_id)


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    """Ищет пользователя по email"""
    return await session.scalar(select(User).where(User.email == email.lower()))


async def create_user(session: AsyncSession, data: UserCreate) -> User:
    """Регистрирует пользователя с ролью сотрудника"""
    user = User(
        email=data.email.lower(),
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
        department_id=data.department_id,
        role=UserRole.EMPLOYEE,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate(session: AsyncSession, email: str, password: str) -> User | None:
    """Проверяет email и пароль, возвращает пользователя или None"""
    user = await get_user_by_email(session, email)
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user


async def set_role(session: AsyncSession, user: User, role: UserRole) -> User:
    """Меняет роль пользователя"""
    user.role = role
    await session.commit()
    await session.refresh(user)
    return user
