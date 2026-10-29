from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session

app = FastAPI(
    title="Сервис вакансий",
    description="Внутренний сервис вакансий компании",
)


@app.get("/")
async def root() -> dict[str, str]:
    """Проверка, что сервис работает."""
    return {"message": "Сервис вакансий работает"}


@app.get("/health/db")
async def check_db(session: AsyncSession = Depends(get_session)) -> dict[str, str]:
    """Проверка, что есть связь с базой данных."""
    await session.execute(text("SELECT 1"))
    return {"database": "ok"}
