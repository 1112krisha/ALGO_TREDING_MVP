# Deploy & Share Link

## Option 1: Render (Free, One Link)

1. **Push to GitHub** (see below)
2. Go to [render.com](https://render.com) → Sign up
3. **New** → **Blueprint** → Connect your GitHub repo
4. Select this repo → **Apply**
5. Wait 5–10 min for build
6. Get your link: `https://algo-trading-mvp.onrender.com`

**Demo login:** `demo@test.com` / `demo123`

---

## Option 2: Railway (Simple)

1. Push to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select repo → Add Dockerfile (auto-detected)
4. Deploy → Get public URL

---

## Option 3: Run Locally (Docker)

```bash
docker build -t algo-trading .
docker run -p 8080:80 algo-trading
```

Open: http://localhost:8080

---

## Push to GitHub

```bash
cd algo-trading-mvp
git init
git add .
git commit -m "Algo Trading MVP - ready for demo"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/algo-trading-mvp.git
git push -u origin main
```

Create repo first: github.com → New repository → `algo-trading-mvp`
