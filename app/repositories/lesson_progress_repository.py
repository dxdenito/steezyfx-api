from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.lesson_progress import LessonProgress
from app.models.lesson import Lesson
from app.models.module import Module


class LessonProgressRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_learner_and_lesson(
        self, learner_id: int, lesson_id: int
    ) -> LessonProgress | None:
        try:
            result = await self.db.execute(
                select(LessonProgress)
                .where(
                    LessonProgress.learner_id == learner_id,
                    LessonProgress.lesson_id == lesson_id,
                )
                .options(
                    selectinload(LessonProgress.learner),
                    selectinload(LessonProgress.lesson),
                )
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while fetching lesson progress: {e}",
            )

    async def list_by_learner_and_course(
        self, learner_id: int, course_id: int
    ) -> list[LessonProgress]:
        try:
            statement = (
                select(LessonProgress)
                .join(Lesson, LessonProgress.lesson_id == Lesson.id)
                .join(Module, Lesson.module_id == Module.id)
                .where(
                    LessonProgress.learner_id == learner_id,
                    Module.course_id == course_id,
                )
                .options(selectinload(LessonProgress.lesson))
            )
            result = await self.db.execute(statement)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while fetching lesson progress: {e}",
            )

    async def create(self, lessonprogress: LessonProgress) -> LessonProgress:
        try:
            self.db.add(lessonprogress)
            await self.db.commit()
            await self.db.refresh(lessonprogress)
            return lessonprogress
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while creating lesson progress: {e}",
            )

    async def update(self, lessonprogress: LessonProgress) -> LessonProgress:

        try:
            await self.db.commit()
            await self.db.refresh(lessonprogress)
            return lessonprogress
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while updating lesson progress: {e}",
            )
