from pydantic import BaseModel, Field


class LessonCreate(BaseModel):
    module_id: int
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    video_url: str | None
    order: int | None


class LessonUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    content: str | None = Field(None, min_length=1)
    video_url: str | None = None
    order: int | None = None


class LessonSummary(BaseModel):
    id: int
    title: str
    order: int | None
    model_config = {"from_attributes": True}


class LessonOut(BaseModel):
    id: int
    module_id: int
    title: str 
    content: str 
    video_url: str | None
    order: int | None
    model_config = {"from_attributes": True}
