"""
Algo Trading MVP - FastAPI Application Entry Point

Production-style backend for paper trading automation.
Supports strategy creation, execution, and PnL tracking.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routes import auth, strategies, trades
from app.services.trading_engine import TradingEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle: startup and shutdown."""
    # Startup: Initialize database and start trading engine
    await init_db()
    engine = TradingEngine()
    await engine.start()
    app.state.trading_engine = engine
    yield
    # Shutdown: Stop trading engine
    await engine.stop()


app = FastAPI(
    title="Algo Trading MVP API",
    description="Paper trading automation - create strategies, auto-execute, track PnL",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:5173",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
        "http://localhost:3003",
        "http://127.0.0.1:3003",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(strategies.router, prefix="/api/strategies", tags=["Strategies"])
app.include_router(trades.router, prefix="/api/trades", tags=["Trades"])


@app.get("/")
async def root():
    """Root - redirect to docs."""
    return {
        "message": "Algo Trading MVP API",
        "docs": "/docs",
        "health": "/health",
        "api": "/api/auth, /api/strategies, /api/trades",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return {"status": "healthy", "service": "algo-trading-mvp"}


@app.get("/api")
async def api_info():
    """API prefix info."""
    return {
        "message": "API base",
        "auth": "/api/auth/register, /api/auth/login",
        "strategies": "/api/strategies",
        "trades": "/api/trades",
    }
