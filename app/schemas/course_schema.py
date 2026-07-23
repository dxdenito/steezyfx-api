from decimal import Decimal

from pydantic import BaseModel, field_validator, Field, ValidationInfo

from app.schemas.module_schema import ModuleSummary
from app.models.course import CourseStatus


class CourseCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    overview: str = Field(..., min_length=1)
    category_id: int | None = None
    is_free: bool = True
    price: Decimal | None = Field(None, gt=0)
    discount_percentage: Decimal | None = Field(None, ge=0, le=100)


class CourseUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=255)
    overview: str | None = None
    category_id: int | None = None
    is_free: bool | None = None
    price: Decimal | None = Field(None, gt=0)
    discount_percentage: Decimal | None = Field(None, ge=0, le=100)


class CourseReviewAction(BaseModel):
    action: str
    rejection_reason: str | None = None

    @field_validator("action")
    @classmethod
    def validate_action(cls, value):
        if value not in ["approve", "reject"]:
            raise ValueError("Action must be either 'approve' or 'reject'")
        return value

    @field_validator("rejection_reason")
    @classmethod
    def require_reason_if_rejecting(cls, value, info: ValidationInfo):
        if info.data.get("action") == "reject" and not value:
            raise ValueError("rejection_reason is required when rejecting a course")
        return value


class CourseFlagAction(BaseModel):
    flag_reason: str = Field(..., min_length=1, max_length=255)


class CourseOut(BaseModel):
    id: int
    tutor_id: int
    title: str
    overview: str
    category_id: int | None
    is_free: bool = True
    price: Decimal | None
    discount_percentage: Decimal | None
    status: CourseStatus
    rejection_reason: str | None
    flag_reason: str | None
    modules: list[ModuleSummary]
