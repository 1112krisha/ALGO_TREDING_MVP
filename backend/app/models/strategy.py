"""
Trading strategy model.

Defines buy/sell/stop-loss rules for paper trading.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class StrategyStatus:
    """Strategy lifecycle states."""
    ACTIVE = "active"
    STOPPED = "stopped"


class Strategy(Base):
    """Trading strategy with price targets and quantity."""
    
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Strategy parameters
    symbol = Column(String(20), nullable=False)  # e.g., "AAPL", "BTC"
    buy_price = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)
    stop_loss = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    
    # State
    status = Column(String(20), default=StrategyStatus.ACTIVE)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="strategies")
    trades = relationship("Trade", back_populates="strategy", order_by="Trade.created_at")
