from datetime import datetime

from sqlalchemy import Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Enrollment(Base):
    __tablename__ = "enrollments"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    learner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", unique=True))
    enrolled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
