from fastapi import FastAPI

app = FastAPI(
    title="Сервис вакансий",
    description="Внутренний сервис вакансий компании",
)


@app.get("/")
async def root() -> dict[str, str]:
    """Проверка, что сервис работает."""
    return {"message": "Сервис вакансий работает"}
