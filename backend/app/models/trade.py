"""
Trade model for executed paper trades.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class TradeType:
    """Trade direction."""
    BUY = "BUY"
    SELL = "SELL"


class TradeStatus:
    """Trade lifecycle."""
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class Trade(Base):
    """Executed paper trade record."""
    
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    
    # Trade details
    trade_type = Column(String(10), nullable=False)  # BUY or SELL
    symbol = Column(String(20), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String(10), default=TradeStatus.OPEN)
    
    # PnL (for SELL trades)
    pnl = Column(Float)  # Profit/Loss when trade closed
    pnl_percent = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="trades")
    strategy = relationship("Strategy", back_populates="trades")
