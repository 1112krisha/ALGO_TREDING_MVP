# Single Dockerfile for full-stack deploy (one URL)
# Build: docker build -t algo-trading .
# Run: docker run -p 8080:80 algo-trading

# Stage 1: Frontend build
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Backend + Nginx
FROM python:3.11-slim
WORKDIR /app

# Install nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Backend
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./

# Frontend static + nginx config
COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html
COPY deploy/nginx.conf /etc/nginx/sites-available/default

# Create data dir for SQLite
RUN mkdir -p /app/data

ENV DATABASE_URL=sqlite+aiosqlite:///./data/algo_trading.db
ENV SECRET_KEY=prod-secret-change-in-env

EXPOSE 80

# Start script: nginx + uvicorn
COPY deploy/start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]
