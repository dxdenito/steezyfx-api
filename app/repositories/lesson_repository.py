from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.lesson import Lesson


class LessonRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, lesson_id: int) -> Lesson | None:
        try:
            result = await self.db.execute(select(Lesson).where(Lesson.id == lesson_id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching Lesson: {e}",
            )

    async def list_by_module(self, module_id: int) -> list[Lesson]:
        try:
            result = await self.db.execute(
                select(Lesson)
                .where(Lesson.module_id == module_id)
                .order_by(Lesson.order.asc())
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching lessons:{e}",
            )

    async def create(self, lesson: Lesson) -> Lesson:
        try:
            self.db.add(lesson)
            await self.db.commit()
            await self.db.refresh(lesson)
            return await self.get_by_id(lesson.id)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while creating lesson: {e}",
            )

    async def update(self, lesson: Lesson) -> Lesson:

        try:
            await self.db.commit()
            await self.db.refresh(lesson)
            return await self.get_by_id(lesson.id)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while updating lesson: {e}",
            )

    async def delete(self, lesson: Lesson) -> None:

        try:
            await self.db.delete(lesson)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while deleting lesson: {e}",
            )
