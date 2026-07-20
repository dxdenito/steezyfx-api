import calendar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from datetime import date

from app.models.trade_idea import TradeIdea


class TradeIdeaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, idea_id: int) -> TradeIdea | None:
        try:
            result = await self.db.execute(
                select(TradeIdea)
                .options(selectinload(TradeIdea.executions))
                .where(TradeIdea.id == idea_id)
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching trade idea: {e}",
            )

    async def list_by_user(
        self, user_id: int, limit: int = 20, offset: int = 0
    ) -> list[TradeIdea]:
        try:
            statement = (
                select(TradeIdea)
                .options(selectinload(TradeIdea.executions))
                .where(TradeIdea.user_id == user_id)
                .offset(offset)
                .limit(limit)
            )
            result = await self.db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while fetching trade ideas by user: {e}",
            )

    async def list_by_user_and_date(
        self, user_id: int, target_date: date
    ) -> list[TradeIdea]:
        try:
            statement = (
                select(TradeIdea)
                .options(selectinload(TradeIdea.executions))
                .where(TradeIdea.user_id == user_id, TradeIdea.idea_date == target_date)
            )
            result = await self.db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while fetching idea by user and date : {e}",
            )

    # ^ this is the one the "click a calendar date" UI calls directly
    async def list_by_user_and_month(
        self, user_id: int, year: int, month: int
    ) -> list[TradeIdea]:
        try:
            start_date = date(year, month, 1)
            last_day = calendar.monthrange(year, month)[1]
            end_date = date(year, month, last_day)

            statement = (
                select(TradeIdea)
                .options(selectinload(TradeIdea.executions))
                .where(
                    TradeIdea.user_id == user_id,
                    TradeIdea.idea_date >= start_date,
                    TradeIdea.idea_date <= end_date,
                )
            )
            result = await self.db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while fetching idea by user and date : {e}",
            )

    # ^ this is what feeds the calendar's day-cell markers + monthly PnL sidebar
    async def create(self, idea: TradeIdea) -> TradeIdea:
        try:
            self.db.add(idea)
            await self.db.commit()
            await self.db.refresh(idea)
            return await self.get_by_id(idea.id)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating trade idea: {e}",
            )

    async def update(self, idea: TradeIdea) -> TradeIdea:
        try:
            await self.db.commit()
            await self.db.refresh(idea)
            return await self.get_by_id(idea.id)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating trade idea: {e}",
            )

    async def delete(self, idea: TradeIdea) -> None:
        try:
            await self.db.delete(idea)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting trade idea: {e}",
            )
