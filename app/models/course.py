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
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


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
    tutor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    overview: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[CourseStatus] = mapped_column(
        Enum(CourseStatus, native_enum=False), nullable=False
    )
    rejection_reason: Mapped[str] = mapped_column(String(255), nullable=False)
    flag_reason: Mapped[str] = mapped_column(String(255), nullable=False)
    is_free: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    discount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("catogories.id"), nullable=False, unique=True
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
