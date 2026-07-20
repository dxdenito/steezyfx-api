from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer,ForeignKey,Boolean,DateTime,func

from app.core.database import Base

class LessonProgress(Base):
    __tablename__="lesson_progress"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    learner_id:Mapped[int] = mapped_column(ForeignKey("users.id"),unique=True)
    lesson_id:Mapped[int] = mapped_column(ForeignKey("lessons.id"),unique=True)
    completed:Mapped[bool | None] =mapped_column(Boolean,nullable= True)
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )