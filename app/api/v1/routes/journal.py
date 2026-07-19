from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.v1.deps import get_current_user
from app.repositories.trade_idea_repository import TradeIdeaRepository
from app.repositories.trade_execution_repository import TradeExecutionRepository
from app.services.trade_idea_service import TradeIdeaService
from app.services.trade_execution_service import TradeExecutionService
from app.schemas.trade_schema import (
    TradeExecutionCreate,
    TradeIdeaCreate,
    TradeExecutionOut,
    TradeExecutionSummary,
    TradeExecutionUpdate,
    TradeIdeaOut,
    TradeIdeaUpdate,
)

router = APIRouter(prefix="/journal", tags=["journal"])


def get_idea_service(db: AsyncSession = Depends(get_db)) -> TradeIdeaService:
    return TradeIdeaService(repo=TradeIdeaRepository(db))


def get_execution_service(db: AsyncSession = Depends(get_db)) -> TradeExecutionService:
    return TradeExecutionService(
        execution_repo=TradeExecutionRepository(db),
        idea_repo=TradeIdeaRepository(db),
    )


# --- Trade Ideas ---


@router.post("/ideas", response_model=TradeIdeaOut)
async def create_idea(
    idea: TradeIdeaCreate,
    current_user=Depends(get_current_user),
    service: TradeIdeaService = Depends(get_idea_service),
):
    return await service.create_idea(data=idea, user_id=current_user.id)


@router.patch("/ideas/{idea_id}", response_model=TradeIdeaOut)
async def update_idea(
    idea_id: int,
    idea: TradeIdeaUpdate,
    current_user=Depends(get_current_user),
    service: TradeIdeaService = Depends(get_idea_service),
):
    try:
        return await service.update_idea(
            idea_id=idea_id, data=idea, user_id=current_user.id
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/ideas/{idea_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_idea(
    idea_id: int,
    current_user=Depends(get_current_user),
    service: TradeIdeaService = Depends(get_idea_service),
):
    try:
        await service.delete_idea(idea_id=idea_id, user_id=current_user.id)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/ideas/{idea_id}/missed", response_model=TradeIdeaOut)
async def mark_missed(
    idea_id: int,
    current_user=Depends(get_current_user),
    service: TradeIdeaService = Depends(get_idea_service),
):
    try:
        return await service.mark_missed(idea_id=idea_id, user_id=current_user.id)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/ideas/day", response_model=list[TradeIdeaOut])
async def get_ideas_by_date(
    target_date: date,
    current_user=Depends(get_current_user),
    service: TradeIdeaService = Depends(get_idea_service),
):
    return await service.repo.list_by_user_and_date(current_user.id, target_date)


@router.get("/ideas/month", response_model=list[TradeIdeaOut])
async def get_ideas_by_month(
    year: int,
    month: int,
    current_user=Depends(get_current_user),
    service: TradeIdeaService = Depends(get_idea_service),
):
    return await service.repo.list_by_user_and_month(current_user.id, year, month)


@router.get("/ideas/{idea_id}", response_model=TradeIdeaOut)
async def get_idea(
    idea_id: int,
    current_user=Depends(get_current_user),
    service: TradeIdeaService = Depends(get_idea_service),
):
    idea = await service.repo.get_by_id(idea_id)
    if idea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Trade idea not found"
        )
    return idea


# --- Trade Executions ---


@router.post("/executions", response_model=TradeExecutionOut)
async def create_execution(
    execution: TradeExecutionCreate,
    current_user=Depends(get_current_user),
    service: TradeExecutionService = Depends(get_execution_service),
):
    try:
        return await service.create_execution(data=execution, user_id=current_user.id)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/executions/{execution_id}", response_model=TradeExecutionOut)
async def update_execution(
    execution_id: int,
    execution: TradeExecutionUpdate,
    current_user=Depends(get_current_user),
    service: TradeExecutionService = Depends(get_execution_service),
):
    try:
        return await service.update_execution(
            execution_id=execution_id, data=execution, user_id=current_user.id
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/executions/{execution_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_execution(
    execution_id: int,
    current_user=Depends(get_current_user),
    service: TradeExecutionService = Depends(get_execution_service),
):
    try:
        await service.delete_execution(
            execution_id=execution_id, user_id=current_user.id
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/executions/idea/{idea_id}", response_model=list[TradeExecutionSummary])
async def list_by_idea(
    idea_id: int,
    current_user=Depends(get_current_user),
    service: TradeExecutionService = Depends(get_execution_service),
):
    return await service.execution_repo.list_by_idea(idea_id)
