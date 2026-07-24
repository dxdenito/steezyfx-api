from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.module import Module


class ModuleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, module_id: int) -> Module | None:
        try:
            result = self.db.execute(
                select(Module)
                .where(Module.id == module_id)
                .options(selectinload(Module.lessons))
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching Module: {e}",
            )

    async def list_by_course(self, course_id: int) -> list[Module]:
        try:
            result = self.db.execute(
                select(Module)
                .where(Module.course_id == course_id)
                .options(selectinload(Module.lessons))
                .order_by(Module.order.asc)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching modules:{e}",
            )

    
    async def create(self, module: Module) -> Module:
        try:
            self.db.add(module)
            await self.db.commit()
            await self.db.refresh(module)
            return await self.get_by_id(module.id)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while creating module: {e}",
            )

    async def update(self, module: Module) -> Module:

        try:
            await self.db.commit()
            await self.db.refresh(module)
            return await self.get_by_id(module.id)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while updating module: {e}",
            )

    async def delete(self, module: Module) -> None:

        try:
            await self.db.delete(module)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while deleting module: {e}",
            )

