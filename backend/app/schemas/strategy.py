"""Strategy schemas."""

from datetime import datetime
from pydantic import BaseModel, Field


class StrategyCreate(BaseModel):
    """Create a new trading strategy."""
    symbol: str = Field(..., min_length=1, max_length=20)
    buy_price: float = Field(..., gt=0)
    sell_price: float = Field(..., gt=0)
    stop_loss: float = Field(..., gt=0)
    quantity: float = Field(..., gt=0)


class StrategyUpdate(BaseModel):
    """Update strategy (e.g., start/stop)."""
    is_active: bool | None = None


class StrategyResponse(BaseModel):
    """Strategy API response."""
    id: int
    symbol: str
    buy_price: float
    sell_price: float
    stop_loss: float
    quantity: float
    status: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
