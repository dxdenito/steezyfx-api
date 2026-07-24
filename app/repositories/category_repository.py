from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, category_id: int) -> Category | None:
        try:
            result = await self.db.execute(
                select(Category).where(Category.id == category_id)
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching category: {e}",
            )

    async def get_by_slug(self, slug: str) -> Category | None:
        try:
            result = await self.db.execute(
                select(Category).where(Category.slug == slug)
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching category: {e}",
            )

    async def list_all(self) -> list[Category]:
        try:
            result = await self.db.execute(select(Category))
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error listing categories: {e}",
            )

    async def create(self, category: Category) -> Category:
        try:
            self.db.add(category)
            await self.db.commit()
            await self.db.refresh(category)
            return category
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating category: {e}",
            )

    async def update(self, category: Category) -> Category:
        try:
            await self.db.commit()
            await self.db.refresh(category)
            return category
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating category: {e}",
            )

    async def delete(self, category: Category) -> None:
        try:
            await self.db.delete(category)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting category: {e}",
            )
