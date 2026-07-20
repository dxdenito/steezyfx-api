from datetime import datetime

from sqlalchemy import Integer, ForeignKey, DateTime, func,UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Enrollment(Base):
    __tablename__ = "enrollments"
    __table_args__ = (UniqueConstraint("learner_id", "course_id", name="uq_learner_course"),)
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    learner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    enrolled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
