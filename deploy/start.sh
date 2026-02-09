#!/bin/sh
cd /app && python seed_demo_user.py 2>/dev/null || true
nginx &
exec python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
