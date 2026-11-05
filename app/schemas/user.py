from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import UserRole


class UserCreate(BaseModel):
    """Данные для регистрации"""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=200)
    department_id: int | None = None


class UserRead(BaseModel):
    """Пользователь в ответе API, без пароля"""

    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    full_name: str
    role: UserRole
    department_id: int | None
    created_at: datetime


class RoleUpdate(BaseModel):
    """Новая роль пользователя"""

    role: UserRole


class Token(BaseModel):
    """Токен доступа"""

    access_token: str
    token_type: str = "bearer"
