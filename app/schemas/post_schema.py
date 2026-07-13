import re
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ValidationInfo


class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    excerpt: str | None = Field(None, max_length=255)
    category_id: int | None = Field(None, description="The ID of the category")
    tag_ids: list[int] | None = Field(
        None, description="A list of tag IDs associated with the post"
    )
    # NOTE: no `slug` field -- slug is generated server-side from the title,
    # never supplied by the client. Same reasoning as why `role` never comes
    # from the client on UserCreate -- some fields are the system's to decide,
    # not the caller's.


class PostUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    content: str | None = Field(None, min_length=1)
    excerpt: str | None = Field(None, max_length=255)
    category_id: int | None = Field(None, description="The ID of the category")
    tag_ids: list[int] | None = Field(
        None, description="A list of tag IDs associated with the post"
    )
    # Same reasoning -- no slug here either. If the title changes, the
    # service layer can decide whether to regenerate the slug, not the client.


class PostReviewAction(BaseModel):
    action: str = Field(..., description="The action to be taken on the post")
    rejection_reason: str | None = Field(
        None, description="Required if action is 'reject'"
    )

    @field_validator("action")
    @classmethod
    def validate_action(cls, value):
        if value not in ["approve", "reject"]:
            raise ValueError("Action must be either 'approve' or 'reject'")
        return value

    @field_validator("rejection_reason")
    @classmethod
    def require_reason_if_rejecting(cls, value, info: ValidationInfo):
        # info.data contains every field validated so far, in declaration
        # order. Since `action` is declared ABOVE `rejection_reason` in this
        # class, `info.data["action"]` is already available here.
        # If the order were flipped, this .get("action") would return None
        # every time, and this whole check would silently never fire.
        if info.data.get("action") == "reject" and not value:
            raise ValueError("rejection_reason is required when rejecting a post")
        return value


class AuthorOut(BaseModel):
    id: int
    username: str
    model_config = {"from_attributes": True}


class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str
    model_config = {"from_attributes": True}


class TagOut(BaseModel):
    id: int
    name: str
    slug: str
    model_config = {"from_attributes": True}


class PostPublicOut(BaseModel):
    """What a regular site visitor / learner sees on a published post."""
    id: int
    title: str
    slug: str
    content: str
    excerpt: str | None
    author: AuthorOut
    category: CategoryOut | None
    tags: list[TagOut]
    published_at: datetime | None
    model_config = {"from_attributes": True}


class PostAdminOut(PostPublicOut):
    """What the author (their own post) or an admin (review queue) sees.
    Inherits everything from PostPublicOut, adds the internal-only fields."""
    status: str
    rejection_reason: str | None
    created_at: datetime
    updated_at: datetime
