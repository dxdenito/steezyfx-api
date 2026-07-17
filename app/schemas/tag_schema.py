import re
from pydantic import BaseModel, Field, field_validator


class TagCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(None, max_length=255)


class TagUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = Field(None, max_length=255)
    is_active: bool | None = None


class TagOut(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None
    is_active: bool
    model_config = {"from_attributes": True}