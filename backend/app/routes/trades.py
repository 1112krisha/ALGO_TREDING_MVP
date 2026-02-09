"""
Trade routes: fetch trade logs and PnL summary.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.trade import Trade
from app.models.user import User
from app.schemas.trade import PnLSummary, TradeResponse
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("", response_model=list[TradeResponse])
async def list_trades(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    strategy_id: int | None = None,
    limit: int = Query(100, le=500),
):
    """Fetch trade logs for current user."""
    query = select(Trade).where(Trade.user_id == user.id)
    if strategy_id:
        query = query.where(Trade.strategy_id == strategy_id)
    query = query.order_by(Trade.created_at.desc()).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/pnl", response_model=PnLSummary)
async def get_pnl_summary(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    strategy_id: int | None = None,
):
    """Get simulated PnL summary (closed trades only)."""
    query = (
        select(
            func.coalesce(func.sum(Trade.pnl), 0).label("total_pnl"),
            func.count(Trade.id).label("total_trades"),
            func.sum(case((Trade.pnl > 0, 1), else_=0)).label("winning"),
            func.sum(case((Trade.pnl < 0, 1), else_=0)).label("losing"),
        )
        .where(Trade.user_id == user.id, Trade.status == "CLOSED", Trade.pnl.isnot(None))
    )
    if strategy_id:
        query = query.where(Trade.strategy_id == strategy_id)
    result = await db.execute(query)
    row = result.one()
    return PnLSummary(
        total_pnl=float(row.total_pnl or 0),
        total_trades=row.total_trades or 0,
        winning_trades=int(row.winning or 0),
        losing_trades=int(row.losing or 0),
    )
