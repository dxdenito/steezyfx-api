
from pydantic import BaseModel, Field
from app.models.profile import ExperienceLevel

class ProfileUpdate(BaseModel):
    bio: str | None = Field(None, max_length=255)
    avatar_url: str | None = Field(None, max_length=255)
    experience_level: ExperienceLevel | None = None

class ProfileOut(BaseModel):
    bio: str | None
    avatar_url: str | None
    experience_level: ExperienceLevel | None
    model_config = {"from_attributes": True}