from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.models.profile import Profile


class ProfileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id(self, user_id: int) -> Profile:
        try:
            result = await self.db.execute(
                select(Profile).where(Profile.user_id == user_id)
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching Profile: {e}",
            )

    async def create_profile(self, profile: Profile) -> Profile:
        try:
            self.db.add(profile)
            await self.db.commit()
            await self.db.refresh(profile)
            return profile
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating profile: {e}",
            )

    async def update_profile(self, profile: Profile) -> Profile:
        try:
            await self.db.commit()
            await self.db.refresh(profile)
            return profile
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating profile: {e}",
            )

    async def delete_profile(self, profile: Profile) -> None:
        try:
            await self.db.delete(profile)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting profile: {e}",
            )
