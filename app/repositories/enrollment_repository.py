from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.enrollment import Enrollment


class EnrollmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_learner_and_course(
        self, learner_id: int, course_id: int
    ) -> Enrollment | None:
        try:
            result = await self.db.execute(
                select(Enrollment)
                .where(
                    Enrollment.learner_id == learner_id,
                    Enrollment.course_id == course_id,
                )
                .options(
                    selectinload(Enrollment.learner), selectinload(Enrollment.course)
                )
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while fetching enrollment: {e}",
            )

    async def list_by_learner(self, learner_id: int) -> list[Enrollment] | None:
        try:
            result = await self.db.execute(
                select(Enrollment)
                .where(
                    Enrollment.learner_id == learner_id,
                )
                .options(
                    selectinload(Enrollment.learner), selectinload(Enrollment.course)
                )
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while fetching enrollment: {e}",
            )

    async def create(self, enrollment: Enrollment) -> Enrollment:
        try:
            self.db.add(enrollment)
            await self.db.commit()
            await self.db.refresh(enrollment)
            return enrollment
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while creating enrollment: {e}",
            )

    async def delete(self, enrollment: Enrollment) -> None:

        try:
            await self.db.delete(enrollment)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while deleting enrollment: {e}",
            )
