from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Skill(Base):
    """Навык (справочник), например Python или SQL."""

    __tablename__ = "skills"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)


vacancy_skills = Table(
    "vacancy_skills",
    Base.metadata,
    Column(
        "vacancy_id",
        ForeignKey("vacancies.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("skill_id", ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
)
