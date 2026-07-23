from pydantic import BaseModel, Field

from app.schemas.lesson_schema import LessonSummary


class ModuleCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    order: int | None = Field(None, gt=0)


class ModuleUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    order: int | None = Field(None, gt=0)


class ModuleSummary(BaseModel):
    id: int
    title: str
    order: int | None
    lesson_count: int
    model_config = {"from_attributes": True}


class ModuleOut(BaseModel):
    id: int
    title: str
    description: str
    order: int
    is_active: bool
    course_id: int
    lessons: list[LessonSummary]
    model_config = {"from_attributes": True}
