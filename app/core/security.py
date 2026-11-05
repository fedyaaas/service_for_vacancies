from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

ALGORITHM = "HS256"
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Хеширует пароль"""
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Проверяет пароль по хешу"""
    return password_hash.verify(password, hashed)


def create_access_token(user_id: int) -> str:
    """Создаёт JWT-токен для пользователя"""
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def decode_access_token(token: str) -> int | None:
    """Достаёт id пользователя из токена или возвращает None"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None
    return int(payload["sub"])
