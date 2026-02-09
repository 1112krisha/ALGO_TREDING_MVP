"""Trade schemas."""

from datetime import datetime
from pydantic import BaseModel


class TradeResponse(BaseModel):
    """Trade API response."""
    id: int
    trade_type: str
    symbol: str
    quantity: float
    price: float
    status: str
    pnl: float | None
    pnl_percent: float | None
    created_at: datetime

    class Config:
        from_attributes = True


class PnLSummary(BaseModel):
    """Profit & Loss summary."""
    total_pnl: float
    total_trades: int
    winning_trades: int
    losing_trades: int
