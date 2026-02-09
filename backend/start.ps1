# Start backend on port 8001 (avoids conflict if 8000 is in use)
cd $PSScriptRoot
.\venv\Scripts\activate
uvicorn app.main:app --host 127.0.0.1 --port 8001
