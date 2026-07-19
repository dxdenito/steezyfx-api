import re
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator
from app.models.trade_idea import BiasDirection, ConfidenceLevel, IdeaStatus
from app.models.trade_execution import TraderMood, TradeSide, Outcome


class TradeIdeaCreate(BaseModel):
    pair: str = Field(..., min_length=2, max_length=50)
    long_term_bias: BiasDirection
    trade_direction: BiasDirection
    entry_price: Decimal =Field(..., gt = 0)
    stop_loss: Decimal =Field(..., gt = 0)
    take_profit: Decimal =Field(..., gt = 0)
    reason: str = Field(..., min_length=1, max_length=255)
    screenshot_url: str | None = None
    confidence_level: ConfidenceLevel
    idea_date: date

    @field_validator("pair")
    @classmethod
    def convert_pair(cls, value):
        value = value.upper()
        return value


class TradeExecutionCreate(BaseModel):
    trade_idea_id: int | None = None
    execution_date: datetime | None = None
    execution_side: TradeSide
    entry_price: Decimal =Field(..., gt = 0)
    exit_price: Decimal =Field(..., gt = 0)
    lot_size: float =Field(..., gt = 0)
    risk_amount: Decimal =Field(..., gt = 0)
    account_size: Decimal =Field(..., gt = 0)
    mood: TraderMood
    outcome: Outcome = Outcome.OPEN
    comments: str | None = None

class TradeExecutionUpdate(BaseModel):
    exit_price: Decimal | None = Field(None, gt = 0)
    outcome: Outcome | None = None
    pnl: Decimal | None = None
    comments: str | None = None

class TradeExecutionSummary(BaseModel):
    id: int
    execution_side: TradeSide
    outcome: Outcome
    pnl: Decimal | None
    model_config = {"from_attributes": True}

class TradeIdeaOut(BaseModel):
    id: int
    pair: str
    long_term_bias: BiasDirection
    trade_direction: BiasDirection
    entry_price: Decimal 
    stop_loss: Decimal 
    take_profit: Decimal 
    reason: str
    screenshot_url: str | None
    confidence_level: ConfidenceLevel
    idea_date: date
    status: IdeaStatus
    executions: list[TradeExecutionSummary]
    created_at: datetime
    model_config = {"from_attributes": True}


class TradeExecutionOut(BaseModel):
    id: int
    trade_idea_id: int | None
    execution_date: datetime | None
    execution_side: TradeSide
    entry_price: Decimal 
    exit_price: Decimal 
    lot_size: float 
    risk_amount: Decimal
    account_size: Decimal 
    mood: TraderMood
    outcome: Outcome
    pnl: Decimal | None
    comments: str | None
    created_at: datetime
    model_config = {"from_attributes": True}

class TradeIdeaUpdate(BaseModel):
    pair: str | None = Field(None, min_length=2, max_length=50)
    long_term_bias: BiasDirection | None = None
    trade_direction: BiasDirection | None = None
    entry_price: Decimal | None = Field(None, gt=0)
    stop_loss: Decimal | None = Field(None, gt=0)
    take_profit: Decimal | None = Field(None, gt=0)
    reason: str | None = Field(None, min_length=1, max_length=255)
    screenshot_url: str | None = None
    confidence_level: ConfidenceLevel | None = None
    idea_date: date | None = None

    @field_validator("pair")
    @classmethod
    def convert_pair(cls, value):
        if value is not None:
            value = value.upper()
        return value