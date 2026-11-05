from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import SessionDep
from app.routers import auth, departments, skills, users

app = FastAPI(
    title="Сервис вакансий",
    description="Внутренний сервис вакансий компании",
    version="1.0.0",
)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(departments.router)
app.include_router(skills.router)


@app.get("/", tags=["Служебное"])
async def root() -> dict[str, str]:
    """Проверка, что сервис работает"""
    return {"message": "Сервис вакансий работает"}


@app.get("/health/db", tags=["Служебное"])
async def check_db(session: SessionDep) -> dict[str, str]:
    """Проверка связи с БД"""
    await session.execute(text("SELECT 1"))
    return {"database": "ok"}
