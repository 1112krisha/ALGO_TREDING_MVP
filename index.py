"""
Vercel entry - FastAPI app for algo-trading-mvp.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:////tmp/algo_trading.db")
os.environ["VERCEL"] = "1"

from app.main import app
