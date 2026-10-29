from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения, читаются из файла .env."""

    database_url: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
