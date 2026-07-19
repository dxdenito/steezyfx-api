from app.models.trade_execution import TradeExecution
from app.models.trade_idea import IdeaStatus
from app.repositories.trade_execution_repository import TradeExecutionRepository
from app.repositories.trade_idea_repository import TradeIdeaRepository
from app.schemas.trade_schema import TradeExecutionCreate, TradeExecutionUpdate


class TradeExecutionService:
    def __init__(
        self,
        execution_repo: TradeExecutionRepository,
        idea_repo: TradeIdeaRepository,
    ):
        self.execution_repo = execution_repo
        self.idea_repo = idea_repo

    async def create_execution(self, data: TradeExecutionCreate, user_id: int) -> TradeExecution:
        if data.trade_idea_id is not None:
            idea = await self.idea_repo.get_by_id(data.trade_idea_id)
            if idea is None:
                raise ValueError("Linked trade idea not found")
            if idea.user_id != user_id:
                raise PermissionError("You can only link executions to your own trade ideas")

            # first execution against this idea flips it to EXECUTED;
            # later scale-in executions leave it as EXECUTED, no-op either way
            if idea.status != IdeaStatus.EXECUTED:
                idea.status = IdeaStatus.EXECUTED
                await self.idea_repo.update(idea)

        execution = TradeExecution(
            user_id=user_id,
            trade_idea_id=data.trade_idea_id,
            execution_date=data.execution_date,
            execution_side=data.execution_side,
            entry_price=data.entry_price,
            exit_price=data.exit_price,
            lot_size=data.lot_size,
            risk_amount=data.risk_amount,
            account_size=data.account_size,
            mood=data.mood,
            outcome=data.outcome,
            comments=data.comments,
        )
        return await self.execution_repo.create(execution)

    async def update_execution(
        self, execution_id: int, data: TradeExecutionUpdate, user_id: int
    ) -> TradeExecution:
        execution = await self.execution_repo.get_by_id(execution_id)
        if execution is None:
            raise ValueError("Trade execution not found")
        if execution.user_id != user_id:
            raise PermissionError("You can only edit your own trade executions")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(execution, field, value)

        return await self.execution_repo.update(execution)

    async def delete_execution(self, execution_id: int, user_id: int) -> None:
        execution = await self.execution_repo.get_by_id(execution_id)
        if execution is None:
            raise ValueError("Trade execution not found")
        if execution.user_id != user_id:
            raise PermissionError("You can only delete your own trade executions")
        await self.execution_repo.delete(execution)