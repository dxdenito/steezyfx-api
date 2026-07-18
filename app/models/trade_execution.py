import enum

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, DateTime, func, Enum, Numeric, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.trade_idea import TradeIdea


class TraderMood(enum.Enum):
    CALM = "calm"
    CONFIDENT = "confident"
    DISCIPLINED = "disciplined"
    ANXIOUS = "anxious"
    FOMO = "fomo"
    GREEDY = "greedy"
    FEARFUL = "fearful"
    REVENGE = "revenge"
    BORED = "bored"
    FRUSTRATED = "frustrated"
    IMPULSIVE = "impulsive"
    HESITANT = "hesitant"


class Outcome(enum.Enum):
    OPEN = "open"
    WIN = "win"
    LOSS = "loss"
    BREAKEVEN = "breakeven"
    CANCELLED = "cancelled"
    MISSED = "missed"


class TradeSide(enum.Enum):
    BUY = "buy"
    SELL = "sell"


class TradeExecution(Base):
    __tablename__ = "trade_executions"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    trade_idea_id: Mapped[int | None] = mapped_column(
        ForeignKey("trade_ideas.id"), nullable=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    execution_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    execution_side: Mapped[TradeSide] = mapped_column(
        Enum(TradeSide, native_enum=False), nullable=False
    )
    entry_price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=5), nullable=False
    )
    exit_price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=5), nullable=False
    )
    lot_size: Mapped[float] = mapped_column(
        Float, nullable=False
    )  # lot size itself is fine as float
    risk_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    account_size: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    mood: Mapped[TraderMood] = mapped_column(
        Enum(TraderMood, native_enum=False), nullable=False
    )
    outcome: Mapped[Outcome] = mapped_column(
        Enum(Outcome, native_enum=False), nullable=False
    )
    pnl: Mapped[Decimal | None] = mapped_column(
        Numeric, nullable=True
    )  # no scale and precision because profit can be any number
    comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # in TradeExecution
    idea: Mapped["TradeIdea | None"] = relationship(back_populates="executions")
