from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import SessionDep
from app.core.deps import CurrentUser
from app.core.security import create_access_token
from app.schemas.user import Token, UserCreate, UserRead
from app.services import department as department_service
from app.services import user as user_service

router = APIRouter(prefix="/auth", tags=["Авторизация"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, session: SessionDep):
    """Регистрация нового сотрудника"""
    if await user_service.get_user_by_email(session, data.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email уже зарегистрирован")
    if data.department_id is not None:
        department = await department_service.get_department(
            session, data.department_id
        )
        if department is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Отдел не найден")
    return await user_service.create_user(session, data)


@router.post("/login", response_model=Token)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
):
    """Вход: в поле username укажите email"""
    user = await user_service.authenticate(session, form.username, form.password)
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_access_token(user.id))


@router.get("/me", response_model=UserRead)
async def read_me(user: CurrentUser):
    """Данные текущего пользователя"""
    return user
