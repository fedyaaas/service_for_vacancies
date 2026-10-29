from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

engine = create_async_engine(settings.database_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Базовый класс, от которого будут наследоваться все модели (таблицы)."""


async def get_session():
    """Выдаёт сессию для одного запроса и закрывает её после."""
    async with async_session() as session:
        yield session
