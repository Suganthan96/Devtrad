# 🚀 Deployment Guide - NinjaQuant FastAPI

This guide covers deploying your Injective backtesting API to production.

## 📋 Table of Contents

1. [Local Production Setup](#local-production)
2. [Docker Deployment](#docker)
3. [Cloud Platforms](#cloud-platforms)
4. [Environment Configuration](#environment)

---

## 🏠 Local Production Setup

### Option 1: Uvicorn (Simple)

```bash
# Development mode (with auto-reload)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode (no reload)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Option 2: Gunicorn + Uvicorn Workers (Recommended for Production)

**Install Gunicorn:**
```bash
pip install gunicorn
```

**Run with multiple workers:**
```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
```

**Windows Note:** Gunicorn doesn't support Windows. Use Uvicorn directly:
```powershell
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🐳 Docker Deployment

### Step 1: Create Dockerfile

Create a file named `Dockerfile` in your project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run with Uvicorn
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 2: Create .dockerignore

```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.env
.venv
env/
venv/
.git/
.gitignore
*.md
Dockerfile
.dockerignore
```

### Step 3: Build and Run

```bash
# Build image
docker build -t ninjaquant-api .

# Run container
docker run -d \
  -p 8000:8000 \
  -e USE_REAL_DATA=true \
  -e INJECTIVE_NETWORK=mainnet \
  --name ninjaquant \
  ninjaquant-api

# Check logs
docker logs -f ninjaquant

# Stop container
docker stop ninjaquant
```

### Docker Compose (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - USE_REAL_DATA=true
      - INJECTIVE_NETWORK=mainnet
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Run with Docker Compose:**
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

## ☁️ Cloud Platforms

### 1. Railway.app (Easiest - Free Tier)

**Deploy in 2 minutes:**

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub"
4. Select your repository
5. Railway auto-detects FastAPI and deploys!

**Environment Variables:**
Set in Railway dashboard:
- `USE_REAL_DATA=true`
- `INJECTIVE_NETWORK=mainnet`

**Custom Start Command (if needed):**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

### 2. Render.com (Free Tier)

1. Go to [render.com](https://render.com)
2. New → Web Service
3. Connect your GitHub repo
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:**
     - `USE_REAL_DATA=true`
     - `INJECTIVE_NETWORK=mainnet`

---

### 3. Fly.io

**Install Fly CLI:**
```bash
# macOS/Linux
curl -L https://fly.io/install.sh | sh

# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

**Deploy:**
```bash
# Login
fly auth login

# Launch app (creates fly.toml)
fly launch

# Deploy
fly deploy

# Open app
fly open
```

**fly.toml configuration:**
```toml
app = "ninjaquant-api"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  USE_REAL_DATA = "true"
  INJECTIVE_NETWORK = "mainnet"

[[services]]
  http_checks = []
  internal_port = 8000
  processes = ["app"]
  protocol = "tcp"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

---

### 4. Google Cloud Run

**Create Dockerfile** (see Docker section above)

**Deploy:**
```bash
# Login
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and push
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ninjaquant

# Deploy
gcloud run deploy ninjaquant \
  --image gcr.io/YOUR_PROJECT_ID/ninjaquant \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars USE_REAL_DATA=true,INJECTIVE_NETWORK=mainnet
```

---

### 5. AWS Elastic Beanstalk

**Create `Procfile`:**
```
web: uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Deploy:**
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 ninjaquant-api

# Create environment
eb create ninjaquant-env

# Set environment variables
eb setenv USE_REAL_DATA=true INJECTIVE_NETWORK=mainnet

# Deploy updates
eb deploy

# Open app
eb open
```

---

### 6. Heroku

**Create `Procfile`:**
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Create `runtime.txt`:**
```
python-3.11.7
```

**Deploy:**
```bash
# Login
heroku login

# Create app
heroku create ninjaquant-api

# Set environment variables
heroku config:set USE_REAL_DATA=true
heroku config:set INJECTIVE_NETWORK=mainnet

# Deploy
git push heroku main

# Open app
heroku open
```

---

## 🔧 Environment Configuration

### Production Environment Variables

Create a `.env` file (never commit this):

```env
# Data Source
USE_REAL_DATA=true
INJECTIVE_NETWORK=mainnet

# Server
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Logging
LOG_LEVEL=INFO

# API Settings
API_TITLE=NinjaQuant API
API_VERSION=1.0.0
```

### Update config.py for .env support

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    use_real_data: bool = True
    injective_network: str = "mainnet"
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

---

## 🔒 Production Best Practices

### 1. Add Health Check Endpoint

Already implemented at `/` but you can add a dedicated endpoint:

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "NinjaQuant API",
        "version": "1.0.0",
        "injective_connected": True  # Add actual check
    }
```

### 2. Enable CORS (if needed for web clients)

```bash
pip install fastapi-cors
```

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Add Rate Limiting

```bash
pip install slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/backtest/ema-crossover")
@limiter.limit("10/minute")
async def backtest_ema_crossover(request: Request, ...):
    ...
```

### 4. Add Monitoring

Consider integrating:
- **Sentry** for error tracking
- **Prometheus** for metrics
- **DataDog** for APM

---

## 🎯 Recommended Deployment Path

**For Hackathon/Demo:**
1. **Railway.app** or **Render.com** (free, instant)

**For Production:**
1. **Docker** + **DigitalOcean/AWS/GCP** (most control)
2. **Google Cloud Run** (serverless, auto-scaling)
3. **Fly.io** (global edge deployment)

---

## 📊 Performance Tuning

### Number of Workers

```bash
# Formula: (2 × CPU cores) + 1
# For 2 CPU cores:
--workers 5

# For 4 CPU cores:
--workers 9
```

### Adjust Timeouts

```bash
# For long-running backtests
--timeout 300  # 5 minutes
```

---

## 🐛 Troubleshooting

### Issue: Port already in use
```bash
# Find process
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Issue: Import errors in Docker
```dockerfile
# Add Python path to Dockerfile
ENV PYTHONPATH=/app
```

### Issue: Slow startup
```python
# Add startup event in app/main.py
@app.on_event("startup")
async def startup_event():
    # Pre-load market cache
    from app.data.injective_client import InjectiveDataClient
    client = InjectiveDataClient()
    # Cache markets on startup
```

---

## 📚 Additional Resources

- [FastAPI Deployment Docs](https://fastapi.tiangolo.com/deployment/)
- [Uvicorn Deployment](https://www.uvicorn.org/deployment/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Your API is now ready for production deployment!** 🚀

Choose the platform that best fits your needs and deploy your Injective backtesting API to the world.
