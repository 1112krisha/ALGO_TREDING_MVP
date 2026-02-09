"""
Trading Engine - Core paper trading logic.

Polls mock market prices, executes BUY/SELL based on strategy rules.
Tracks trade state (OPEN/CLOSED) and calculates PnL.
Async-safe with proper locking.
"""

import asyncio
import logging
import random
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import AsyncSessionLocal
from app.models.strategy import Strategy
from app.models.trade import Trade

logger = logging.getLogger(__name__)


class TradingEngine:
    """
    Paper trading engine that:
    1. Polls mock market prices every N seconds
    2. For each active strategy: checks buy/sell/stop-loss conditions
    3. Executes simulated trades and stores in DB
    4. Tracks OPEN positions and calculates PnL on SELL
    """

    def __init__(self):
        self._running = False
        self._task: asyncio.Task | None = None
        self._lock = asyncio.Lock()
        # Mock price cache: symbol -> current price (random walk)
        self._mock_prices: dict[str, float] = {}

    async def start(self):
        """Start the background polling loop."""
        if self._running:
            logger.warning("Trading engine already running")
            return
        self._running = True
        self._task = asyncio.create_task(self._poll_loop())
        logger.info("Trading engine started")

    async def stop(self):
        """Stop the background polling loop."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Trading engine stopped")

    def _get_mock_price(self, symbol: str) -> float:
        """
        Simulate market price using random walk.
        Start from a base if new; otherwise step ±small random change.
        """
        if symbol not in self._mock_prices:
            # Initialize with random base (50-200)
            self._mock_prices[symbol] = 50 + random.random() * 150
        else:
            # Random walk: ±2% per step
            change = (random.random() - 0.5) * 0.04 * self._mock_prices[symbol]
            self._mock_prices[symbol] = max(1, self._mock_prices[symbol] + change)
        return round(self._mock_prices[symbol], 2)

    async def _poll_loop(self):
        """Main loop: poll prices and evaluate strategies."""
        interval = settings.PRICE_POLL_INTERVAL_SECONDS
        while self._running:
            try:
                await self._evaluate_all_strategies()
            except Exception as e:
                logger.exception("Error in trading engine: %s", e)
            await asyncio.sleep(interval)

    async def _evaluate_all_strategies(self):
        """Load active strategies and evaluate each against current price."""
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Strategy)
                .where(Strategy.is_active == True)
                .order_by(Strategy.id)
            )
            strategies = result.scalars().all()

        for strategy in strategies:
            try:
                await self._evaluate_strategy(strategy)
            except Exception as e:
                logger.exception("Error evaluating strategy %s: %s", strategy.id, e)

    async def _evaluate_strategy(self, strategy: Strategy):
        """
        Evaluate one strategy:
        - Get current mock price
        - Check if we have OPEN position for this strategy
        - BUY: if price <= buy_price and no open position
        - SELL: if price >= sell_price OR price <= stop_loss, and we have open position
        """
        price = self._get_mock_price(strategy.symbol)
        logger.debug("Strategy %s (%s): mock price=%.2f", strategy.id, strategy.symbol, price)

        async with AsyncSessionLocal() as db:
            async with self._lock:
                # Check for open BUY position
                open_trade_result = await db.execute(
                    select(Trade)
                    .where(
                        Trade.strategy_id == strategy.id,
                        Trade.trade_type == "BUY",
                        Trade.status == "OPEN",
                    )
                    .order_by(Trade.created_at.desc())
                    .limit(1)
                )
                open_trade = open_trade_result.scalar_one_or_none()

                # SELL condition: price >= sell_price OR price <= stop_loss
                should_sell = (
                    price >= strategy.sell_price or price <= strategy.stop_loss
                ) and open_trade is not None

                # BUY condition: price <= buy_price AND no open position
                should_buy = price <= strategy.buy_price and open_trade is None

                if should_buy:
                    await self._execute_buy(db, strategy, price)
                elif should_sell:
                    await self._execute_sell(db, open_trade, price)

    async def _execute_buy(self, db: AsyncSession, strategy: Strategy, price: float):
        """Execute paper BUY and store trade."""
        trade = Trade(
            user_id=strategy.user_id,
            strategy_id=strategy.id,
            trade_type="BUY",
            symbol=strategy.symbol,
            quantity=strategy.quantity,
            price=price,
            status="OPEN",
        )
        db.add(trade)
        await db.commit()
        logger.info(
            "BUY executed: strategy=%s %s qty=%.2f @ %.2f",
            strategy.id,
            strategy.symbol,
            strategy.quantity,
            price,
        )

    async def _execute_sell(self, db: AsyncSession, open_trade: Trade, price: float):
        """Execute paper SELL, close position, calculate PnL."""
        buy_price = open_trade.price
        quantity = open_trade.quantity
        pnl = (price - buy_price) * quantity
        pnl_percent = ((price - buy_price) / buy_price) * 100 if buy_price else 0

        # Close the BUY trade (PnL stored on SELL to avoid double-counting)
        open_trade.status = "CLOSED"

        # Create SELL trade record with PnL
        sell_trade = Trade(
            user_id=open_trade.user_id,
            strategy_id=open_trade.strategy_id,
            trade_type="SELL",
            symbol=open_trade.symbol,
            quantity=quantity,
            price=price,
            status="CLOSED",
            pnl=pnl,
            pnl_percent=pnl_percent,
        )
        db.add(sell_trade)
        await db.commit()
        logger.info(
            "SELL executed: strategy=%s %s qty=%.2f @ %.2f | PnL=%.2f (%.2f%%)",
            open_trade.strategy_id,
            open_trade.symbol,
            quantity,
            price,
            pnl,
            pnl_percent,
        )
