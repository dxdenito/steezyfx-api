from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.models.tag import Tag


class TagRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, tag_id: int) -> Tag | None:
        try:
            result = await self.db.execute(select(Tag).where(Tag.id == tag_id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching tag: {e}",
            )

    async def get_by_slug(self, slug: str) -> Tag | None:
        try:
            result = await self.db.execute(select(Tag).where(Tag.slug == slug))
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching tag: {e}",
            )

    async def list_all(self) -> list[Tag]:
        try:
            result = await self.db.execute(select(Tag))
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error listing tags: {e}",
            )

    async def create(self, tag: Tag) -> Tag:
        try:
            self.db.add(tag)
            await self.db.commit()
            await self.db.refresh(tag)
            return tag
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating tag: {e}",
            )

    async def update(self, tag: Tag) -> Tag:
        try:
            await self.db.commit()
            await self.db.refresh(tag)
            return tag
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating tag: {e}",
            )

    async def delete(self, tag: Tag) -> None:
        try:
            await self.db.delete(tag)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting tag: {e}",
            )
