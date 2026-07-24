from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.course import Course, CourseStatus
from app.models.module import Module


class CourseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, course_id: int) -> Course | None:
        try:
            result = await self.db.execute(
                select(Course)
                .where(Course.id == course_id)
                .options(
                    selectinload(Course.tutor),
                    selectinload(Course.category),
                    selectinload(Course.modules).selectinload(Module.lessons),
                )
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching Course: {e}",
            )

    async def list_published(self, limit: int = 20, offset: int = 0) -> list[Course]:
        try:
            statement = (
                select(Course)
                .where(Course.status == CourseStatus.PUBLISHED)
                .options(
                    selectinload(Course.tutor),
                    selectinload(Course.category),
                    selectinload(Course.modules).selectinload(Module.lessons),
                )
                .offset(offset)
                .limit(limit)
            )
            result = await self.db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while fetching published Course: {e}",
            )

    async def list_by_tutor_id(
        self, tutor_id: int, limit: int = 20, offset: int = 0
    ) -> list[Course]:

        try:
            statement = (
                select(Course)
                .where(Course.tutor_id == tutor_id)
                .options(
                    selectinload(Course.tutor),
                    selectinload(Course.category),
                    selectinload(Course.modules).selectinload(Module.lessons),
                )
                .offset(offset)
                .limit(limit)
            )
            result = await self.db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while fetching course by tutor: {e}",
            )

    async def list_pending(self, limit: int = 20, offset: int = 0) -> list[Course]:
        try:
            statement = (
                select(Course)
                .where(Course.status == CourseStatus.PENDING)
                .options(
                    selectinload(Course.tutor),
                    selectinload(Course.category),
                    selectinload(Course.modules).selectinload(Module.lessons),
                )
                .offset(offset)
                .limit(limit)
            )
            result = await self.db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while fetching pending Course: {e}",
            )

    async def create(self, course: Course) -> Course:
        try:
            self.db.add(course)
            await self.db.commit()
            await self.db.refresh(course)
            return await self.get_by_id(course.id)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while updating course: {e}",
            )

    async def update(self, course: Course) -> Course:

        try:
            await self.db.commit()
            await self.db.refresh(course)
            return await self.get_by_id(course.id)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while updating course: {e}",
            )

    async def delete(self, course: Course) -> None:

        try:
            await self.db.delete(course)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while deleting course: {e}",
            )
