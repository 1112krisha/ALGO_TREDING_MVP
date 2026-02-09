"""
Strategy routes: create, list, start/stop strategies.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.strategy import Strategy
from app.models.user import User
from app.schemas.strategy import StrategyCreate, StrategyResponse, StrategyUpdate
from app.utils.auth import get_current_user

router = APIRouter()


@router.post("", response_model=StrategyResponse)
async def create_strategy(
    data: StrategyCreate,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Create a new trading strategy."""
    if data.sell_price <= data.buy_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="sell_price must be greater than buy_price",
        )
    if data.stop_loss >= data.buy_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="stop_loss must be less than buy_price",
        )
    strategy = Strategy(
        user_id=user.id,
        symbol=data.symbol.upper(),
        buy_price=data.buy_price,
        sell_price=data.sell_price,
        stop_loss=data.stop_loss,
        quantity=data.quantity,
    )
    db.add(strategy)
    await db.commit()
    await db.refresh(strategy)
    return strategy


@router.get("", response_model=list[StrategyResponse])
async def list_strategies(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    active_only: bool = False,
):
    """List all strategies for current user."""
    query = select(Strategy).where(Strategy.user_id == user.id)
    if active_only:
        query = query.where(Strategy.is_active == True)
    result = await db.execute(query.order_by(Strategy.created_at.desc()))
    return result.scalars().all()


@router.get("/{strategy_id}", response_model=StrategyResponse)
async def get_strategy(
    strategy_id: int,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get single strategy."""
    result = await db.execute(
        select(Strategy).where(
            Strategy.id == strategy_id,
            Strategy.user_id == user.id,
        )
    )
    strategy = result.scalar_one_or_none()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@router.patch("/{strategy_id}/start")
async def start_strategy(
    strategy_id: int,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Activate strategy - engine will start watching for conditions."""
    result = await db.execute(
        select(Strategy).where(
            Strategy.id == strategy_id,
            Strategy.user_id == user.id,
        )
    )
    strategy = result.scalar_one_or_none()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    strategy.is_active = True
    strategy.status = "active"
    await db.commit()
    return {"message": "Strategy started"}


@router.patch("/{strategy_id}/stop")
async def stop_strategy(
    strategy_id: int,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Deactivate strategy - engine will stop watching."""
    result = await db.execute(
        select(Strategy).where(
            Strategy.id == strategy_id,
            Strategy.user_id == user.id,
        )
    )
    strategy = result.scalar_one_or_none()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    strategy.is_active = False
    strategy.status = "stopped"
    await db.commit()
    return {"message": "Strategy stopped"}
