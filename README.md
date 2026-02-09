# Algo Trading Automation MVP

**Paper trading automation system** — Define strategies, automate execution, track PnL. Production-grade architecture, zero real money at risk.

---

## Overview

A full-stack algorithmic trading MVP that lets users create trading strategies with buy/sell/stop-loss rules. The system simulates market prices and automatically executes paper trades when conditions are met. Built for demos, learning, and as a foundation for connecting to real brokers.

---

## Features

- **Strategy Creation** — Define buy price, sell price, stop-loss, and quantity per symbol
- **Auto Execution** — Backend polls mock prices every few seconds; executes BUY/SELL when rules match
- **Active Strategies** — Start/stop strategies; view all active and stopped strategies
- **Trade Logs** — Full history of executed paper trades with timestamps
- **PnL Dashboard** — Simulated profit/loss, win/loss counts
- **JWT Auth** — Secure registration and login
- **Docker Ready** — One-command deployment with Docker Compose

---

## Tech Stack

| Layer      | Technology        |
|-----------|-------------------|
| Backend   | Python, FastAPI    |
| Database  | SQLite (dev) / PostgreSQL (prod) |
| Frontend  | React, Vite, Tailwind CSS |
| Auth      | JWT, bcrypt       |
| Deployment | Docker, Docker Compose |

---

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌──────────────────┐
│   React     │────▶│   FastAPI   │────▶│  Trading Engine  │
│  Frontend   │     │   Backend   │     │  (mock prices)   │
└─────────────┘     └──────┬──────┘     └────────┬─────────┘
                          │                      │
                          ▼                      ▼
                   ┌─────────────┐         ┌─────────────┐
                   │  SQLite /   │◀────────│  Executes   │
                   │  PostgreSQL │         │  BUY/SELL   │
                   └─────────────┘         └─────────────┘
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- (Optional) Docker & Docker Compose

### Run Locally

**1. Backend**

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**2. Frontend**

```bash
cd frontend
npm install
npm run dev
```

- Frontend: http://localhost:3000  
- API: http://localhost:8000  
- Docs: http://localhost:8000/docs  

**3. First Use**

1. Register an account
2. Create a strategy (e.g. AAPL, buy 100, sell 110, stop 95, qty 10)
3. Start the strategy
4. Watch trades execute as mock prices hit your levels

---

## Docker Deployment

```bash
docker-compose up --build
```

- Frontend: http://localhost  
- API: http://localhost:8000  

Set environment variables for production:

```bash
export SECRET_KEY=your-strong-secret-key
export DEBUG=false
docker-compose up -d
```

---

## AWS Deployment Notes

1. **EC2** — Launch an Ubuntu instance, install Docker, clone repo, run `docker-compose up -d`
2. **Security Group** — Open ports 80 (HTTP) and 443 (HTTPS)
3. **Domain** — Point DNS to EC2 IP; add nginx/certbot for SSL
4. **Database** — For production, use RDS PostgreSQL and set `DATABASE_URL`
5. **Secrets** — Store `SECRET_KEY` in AWS Secrets Manager or Parameter Store

---

## Project Structure

```
algo-trading-mvp/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app
│   │   ├── models/           # SQLAlchemy models
│   │   ├── routes/           # API endpoints
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/
│   │   │   └── trading_engine.py
│   │   └── utils/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── services/
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register user |
| POST | `/api/auth/login` | Login, get JWT |
| POST | `/api/strategies` | Create strategy |
| GET | `/api/strategies` | List strategies |
| PATCH | `/api/strategies/{id}/start` | Start strategy |
| PATCH | `/api/strategies/{id}/stop` | Stop strategy |
| GET | `/api/trades` | List trades |
| GET | `/api/trades/pnl` | PnL summary |

---

## Disclaimer

**This is paper trading only.** No real money is involved. Mock prices are simulated with a random walk. This system is for demonstration, education, and as a foundation for real trading integration. Always conduct due diligence before connecting to live brokers or handling real funds.

---

---

## Deploy & Share with Client (One Link)

**Quick deploy:** Push to GitHub → [Render.com](https://render.com) → New Blueprint → Connect repo → Deploy.

**Demo login:** `demo@test.com` / `demo123`

See [DEPLOY.md](DEPLOY.md) for full steps.

---

## License

MIT
