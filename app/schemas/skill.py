from pydantic import BaseModel, ConfigDict, Field


class SkillCreate(BaseModel):
    """Данные для создания или изменения навыка"""

    name: str = Field(min_length=1, max_length=100)


class SkillRead(BaseModel):
    """Навык в ответе API"""

    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
