from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer,ForeignKey,Boolean,DateTime,func, UniqueConstraint

from app.core.database import Base

class LessonProgress(Base):
    __tablename__="lesson_progress"
    __table_args__ = (UniqueConstraint("learner_id", "lesson_id", name="uq_learner_lesson"),)
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    learner_id:Mapped[int] = mapped_column(ForeignKey("users.id"))
    lesson_id:Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    completed:Mapped[bool | None] =mapped_column(Boolean,nullable= False, default=False)
    completed_at: Mapped[datetime |None] = mapped_column(
        DateTime(timezone=True)
    )