import enum
from datetime import datetime
from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class VacancyStatus(enum.StrEnum):
    """Статусы вакансии: черновик, открыта, закрыта."""

    DRAFT = "draft"
    OPEN = "open"
    CLOSED = "closed"


class Vacancy(Base):
    """Вакансия внутри компании."""

    __tablename__ = "vacancies"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[VacancyStatus] = mapped_column(
        Enum(VacancyStatus), default=VacancyStatus.DRAFT
    )
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
