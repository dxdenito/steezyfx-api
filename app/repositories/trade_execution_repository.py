import calendar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from datetime import date

from app.models.trade_execution import TradeExecution


class TradeExecutionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, execution_id: int) -> TradeExecution | None:
        try:
            result = await self.db.execute(
                select(TradeExecution).where(TradeExecution.id == execution_id)
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching trade execution: {e}",
            )

    async def list_by_idea(self, idea_id: int) -> list[TradeExecution]:
        try:
            result = await self.db.execute(
                select(TradeExecution).where(TradeExecution.trade_idea_id == idea_id)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching list by idea: {e}",
            )

    async def list_by_user(
        self, user_id: int, limit: int = 20, offset: int = 0
    ) -> list[TradeExecution]:
        try:
            statement = (
                select(TradeExecution)
                .where(TradeExecution.user_id == user_id)
                .offset(offset)
                .limit(limit)
            )
            result = await self.db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while fetching trade execution by user: {e}",
            )

    async def create(self, execution: TradeExecution) -> TradeExecution:
        try:
            self.db.add(execution)
            await self.db.commit()
            await self.db.refresh(execution)
            return execution
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating trade execution: {e}",
            )

    async def update(self, execution: TradeExecution) -> TradeExecution:
        try:
            await self.db.commit()
            await self.db.refresh(execution)
            return execution
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating trade execution: {e}",
            )

    async def delete(self, execution: TradeExecution) -> None:
        try:
            await self.db.delete(execution)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting trade execution: {e}",
            )
