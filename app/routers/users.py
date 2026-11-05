from fastapi import APIRouter, HTTPException, status

from app.core.database import SessionDep
from app.core.deps import AdminUser
from app.schemas.user import RoleUpdate, UserRead
from app.services import user as user_service

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("/", response_model=list[UserRead])
async def list_users(session: SessionDep, _: AdminUser):
    """Список пользователей для админа"""
    return await user_service.get_users(session)


@router.patch("/{user_id}/role", response_model=UserRead)
async def change_role(
    user_id: int, data: RoleUpdate, session: SessionDep, _: AdminUser
):
    """Смена роли пользователя для админа"""
    user = await user_service.get_user(session, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Пользователь не найден")
    return await user_service.set_role(session, user, data.role)
