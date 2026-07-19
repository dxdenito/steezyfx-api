from app.models.trade_idea import TradeIdea, IdeaStatus
from app.repositories.trade_idea_repository import TradeIdeaRepository
from app.schemas.trade_schema import TradeIdeaCreate, TradeIdeaUpdate


class TradeIdeaService:
    def __init__(self, repo: TradeIdeaRepository):
        self.repo = repo

    async def create_idea(self, data: TradeIdeaCreate, user_id: int) -> TradeIdea:
        idea = TradeIdea(
            user_id=user_id,
            pair=data.pair,
            long_term_bias=data.long_term_bias,
            trade_direction=data.trade_direction,
            entry_price=data.entry_price,
            stop_loss=data.stop_loss,
            take_profit=data.take_profit,
            reason=data.reason,
            screenshot_url=data.screenshot_url,
            confidence_level=data.confidence_level,
            idea_date=data.idea_date,
            status=IdeaStatus.PENDING,
        )
        return await self.repo.create(idea)

    async def update_idea(self, idea_id: int, data: TradeIdeaUpdate, user_id: int) -> TradeIdea:
        idea = await self.repo.get_by_id(idea_id)
        if idea is None:
            raise ValueError("Trade idea not found")
        if idea.user_id != user_id:
            raise PermissionError("You can only edit your own trade ideas")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(idea, field, value)

        return await self.repo.update(idea)

    async def delete_idea(self, idea_id: int, user_id: int) -> None:
        idea = await self.repo.get_by_id(idea_id)
        if idea is None:
            raise ValueError("Trade idea not found")
        if idea.user_id != user_id:
            raise PermissionError("You can only delete your own trade ideas")
        await self.repo.delete(idea)

    async def mark_missed(self, idea_id: int, user_id: int) -> TradeIdea:
        idea = await self.repo.get_by_id(idea_id)
        if idea is None:
            raise ValueError("Trade idea not found")
        if idea.user_id != user_id:
            raise PermissionError("You can only update your own trade ideas")
        if idea.status != IdeaStatus.PENDING:
            raise ValueError("Only pending ideas can be marked as missed")
        idea.status = IdeaStatus.MISSED
        return await self.repo.update(idea)