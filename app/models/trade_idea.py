import enum
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Integer, ForeignKey, String, Enum, Numeric, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.trade_execution import TradeExecution


class BiasDirection(enum.Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"


class ConfidenceLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class IdeaStatus(enum.Enum):
    PENDING = "pending"
    EXECUTED = "executed"
    MISSED = "missed"
    CANCELLED = "cancelled"


class TradeIdea(Base):
    __tablename__ = "trade_ideas"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    pair: Mapped[str] = mapped_column(String(50), nullable=False)
    long_term_bias: Mapped[BiasDirection] = mapped_column(
        Enum(BiasDirection, native_enum=False), nullable=False
    )
    trade_direction: Mapped[BiasDirection] = mapped_column(
        Enum(BiasDirection, native_enum=False), nullable=False
    )

    entry_price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=5), nullable=False
    )
    stop_loss: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=5), nullable=False
    )
    take_profit: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=5), nullable=False
    )

    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    screenshot_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    confidence_level: Mapped[ConfidenceLevel] = mapped_column(
        Enum(ConfidenceLevel, native_enum=False), nullable=False
    )

    idea_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[IdeaStatus] = mapped_column(
        Enum(IdeaStatus, native_enum=False), nullable=False, default=IdeaStatus.PENDING
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    executions: Mapped[list["TradeExecution"]] = relationship(back_populates="idea")
