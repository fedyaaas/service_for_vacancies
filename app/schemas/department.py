from pydantic import BaseModel, ConfigDict, Field


class DepartmentCreate(BaseModel):
    """Данные для создания или изменения отдела"""

    name: str = Field(min_length=2, max_length=100)


class DepartmentRead(BaseModel):
    """Отдел в ответе API"""

    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
