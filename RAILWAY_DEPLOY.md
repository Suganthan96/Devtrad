# 🚂 Railway Deployment Guide - Quick Fix

## ✅ Problem Fixed!

The build error was due to **Python 3.13 compatibility issues with pandas 2.1.4**.

## 🔧 What Was Changed:

1. **Updated `requirements.txt`**:
   - Changed `pandas==2.1.4` → `pandas>=2.2.0` (Python 3.13 compatible)
   - Changed `numpy==1.26.3` → `numpy>=1.26.0`

2. **Updated `runtime.txt`**:
   - Changed to `python-3.11` (more stable)

3. **Added `railway.json`**:
   - Proper start command configuration

4. **Added `nixpacks.toml`**:
   - Ensures Python 3.11 is used

## 🚀 Deploy to Railway

### Step 1: Commit Changes

```bash
git add .
git commit -m "Fix: Update dependencies for Railway deployment"
git push origin main
```

### Step 2: Railway Auto-Deploy

Railway will automatically detect changes and redeploy. The build should now succeed!

### Step 3: Set Environment Variables

In Railway dashboard, add these environment variables:

```
USE_REAL_DATA=true
INJECTIVE_NETWORK=mainnet
```

### Step 4: Verify Deployment

Once deployed, visit your Railway URL:
```
https://your-app.railway.app/
```

You should see:
```json
{
  "message": "Welcome to NinjaQuant API",
  "version": "1.0.0",
  "docs": "/docs",
  "endpoints": ["/backtest/ema-crossover"],
  "data_mode": "real"
}
```

## 📚 Test Your API

Visit the docs page:
```
https://your-app.railway.app/docs
```

Test the backtest endpoint:
```bash
curl -X POST https://your-app.railway.app/backtest/ema-crossover \
  -H "Content-Type: application/json" \
  -d '{
    "market": "INJ/USDT PERP",
    "timeframe": "1h",
    "parameters": {
      "short_period": 12,
      "long_period": 26
    }
  }'
```

## 🎉 You're Live!

Your Injective backtesting API is now deployed on Railway!

---

## Alternative: Deploy with Render

If Railway still has issues, use Render.com:

1. Go to [render.com](https://render.com)
2. New → Web Service
3. Connect GitHub repo
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment:**
     - `USE_REAL_DATA=true`
     - `INJECTIVE_NETWORK=mainnet`

## 🐛 Troubleshooting

### Issue: Still getting pandas build error

**Solution:** Railway might be caching. Try:
1. In Railway dashboard → Settings → "Clear Build Cache"
2. Trigger a new deployment

### Issue: Port binding error

**Solution:** Make sure your start command uses `$PORT`:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Issue: Module not found

**Solution:** Check that all files are committed:
```bash
git add app/
git commit -m "Add app directory"
git push
```

---

**Need help?** Check the full [DEPLOYMENT.md](DEPLOYMENT.md) guide.
