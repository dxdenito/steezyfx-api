import enum

from decimal import Decimal
from datetime import datetime

from sqlalchemy import (
    Integer,
    ForeignKey,
    String,
    Text,
    Enum,
    Boolean,
    Numeric,
    DateTime,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.category import Category
    from app.models.module import Module


class CourseStatus(enum.Enum):
    DRAFT = "draft"  # tutor is building it, not submitted
    PENDING = "pending"  # submitted, awaiting admin review
    PUBLISHED = "published"  # approved, live, editable freely from here
    REJECTED = "rejected"  # admin declined the initial submission
    FLAGGED = "flagged"  # was published, admin has since hidden it for review


class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    tutor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    overview: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[CourseStatus] = mapped_column(
        Enum(CourseStatus, native_enum=False),
        nullable=False,
        default=CourseStatus.DRAFT,
    )
    rejection_reason: Mapped[str] = mapped_column(String(255), nullable=True)
    flag_reason: Mapped[str] = mapped_column(String(255), nullable=True)
    is_free: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    discount_percentage: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2), nullable=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False, unique=True
    )
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    tutor: Mapped["User"] = relationship(back_populates="courses")


    category: Mapped["Category | None"] = relationship(back_populates="courses")

    # in Course
    modules: Mapped[list["Module"]] = relationship(back_populates="course")
