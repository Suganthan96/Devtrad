# ✅ How to Verify NinjaQuant is Working

## 🎯 Quick Verification (3 Ways)

### Method 1: Check the Server is Running ✅

Look at your terminal - you should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [XXXX]
INFO:     Application startup complete.
```

**Status: ✅ Your server IS running on port 8000**

---

### Method 2: Open the API Documentation 📚

1. Open your web browser
2. Go to: `http://localhost:8000/docs`
3. You should see **Swagger UI** with:
   - "NinjaQuant API" title
   - Green "POST /backtest/ema-crossover" endpoint
   - Interactive "Try it out" buttons

**This proves the FastAPI server is working and serving documentation**

---

### Method 3: Run a Test Request 🧪

**Option A: Run the demo script**

```bash
python demo.py
```

**Expected output:**
```
🥷 NinjaQuant - EMA Crossover Backtest
============================================================

Request:
{
  "market": "INJ/USDT",
  "timeframe": "1h",
  "parameters": {
    "short_period": 9,
    "long_period": 21
  },
  "initial_capital": 1000
}

============================================================
Response:
============================================================
{
  "strategy": "ema_crossover",
  "market": "INJ/USDT",
  "timeframe": "1h",
  "results": {
    "win_rate": 0.3333,
    "total_return": -0.0392,
    "max_drawdown": 0.1662,
    "sharpe_ratio": -0.0123,
    "total_trades": 15
  }
}

✅ Backtest completed successfully!
```

**Option B: Run the visual demo**

```bash
python visual_demo.py
```

**Expected output:** Multiple backtests with formatted performance metrics

**Option C: Use curl**

```bash
curl http://localhost:8000/
```

**Expected output:**
```json
{
  "message": "Welcome to NinjaQuant API",
  "docs": "/docs",
  "endpoints": ["/backtest/ema-crossover"]
}
```

---

## 🔍 What Each Test Proves

| Test | What It Verifies |
|------|------------------|
| Server running | FastAPI is up and listening |
| `/docs` loads | Swagger UI is working |
| `demo.py` works | API endpoint is functional |
| Response has metrics | Backtesting logic is working |
| Different parameters = different results | Strategy engine is calculating correctly |

---

## ✅ Verification Checklist

- [x] Server is running on port 8000
- [x] Can access `http://localhost:8000/docs`
- [x] `demo.py` returns JSON response
- [x] Response contains all 5 metrics (win_rate, total_return, max_drawdown, sharpe_ratio, total_trades)
- [x] Different EMA parameters produce different results

**If all checked: Your API is 100% working! 🎉**

---

## 🎬 For Hackathon Demo

### Live Demo Flow:

1. **Show the code** (`main.py`)
   - Point out the clean structure
   - Highlight the EMA calculation
   - Show the metrics computation

2. **Open Swagger UI** (`http://localhost:8000/docs`)
   - Click "Try it out"
   - Modify parameters
   - Execute the request
   - Show the response

3. **Run visual demo** (`python visual_demo.py`)
   - Shows multiple backtests
   - Different parameters
   - Performance comparison

4. **Explain the value**
   - "This is not just data exposure"
   - "It's a computational intelligence layer"
   - "Developers can integrate this into bots, analytics tools, research platforms"

---

## 🧪 Test Different Scenarios

### Scenario 1: Fast Trading (More Signals)
```bash
curl -X POST "http://localhost:8000/backtest/ema-crossover" \
  -H "Content-Type: application/json" \
  -d '{"market":"INJ/USDT","timeframe":"1h","parameters":{"short_period":5,"long_period":13},"initial_capital":1000}'
```

### Scenario 2: Conservative Trading (Fewer Signals)
```bash
curl -X POST "http://localhost:8000/backtest/ema-crossover" \
  -H "Content-Type: application/json" \
  -d '{"market":"INJ/USDT","timeframe":"4h","parameters":{"short_period":20,"long_period":50},"initial_capital":1000}'
```

### Scenario 3: Higher Capital
```bash
curl -X POST "http://localhost:8000/backtest/ema-crossover" \
  -H "Content-Type: application/json" \
  -d '{"market":"INJ/USDT","timeframe":"1h","parameters":{"short_period":9,"long_period":21},"initial_capital":10000}'
```

**Each should return different results, proving the engine is working correctly!**

---

## 🎯 What Success Looks Like

✅ **Server responds instantly**
✅ **Returns valid JSON**
✅ **All metrics are calculated**
✅ **Different parameters = different results**
✅ **Swagger UI is interactive**
✅ **No errors in terminal**

---

## 🚨 Troubleshooting

**Problem: "Connection refused"**
- Solution: Make sure server is running (`python -m uvicorn main:app`)

**Problem: "Module not found"**
- Solution: Install dependencies (`pip install -r requirements.txt`)

**Problem: "Port already in use"**
- Solution: Kill the process or use different port (`--port 8001`)

---

## 📊 Understanding the Output

When you see this response:

```json
{
  "results": {
    "win_rate": 0.3333,
    "total_return": -0.0392,
    "max_drawdown": 0.1662,
    "sharpe_ratio": -0.0123,
    "total_trades": 15
  }
}
```

**This proves:**
1. ✅ Data was fetched (500 candles of synthetic data)
2. ✅ EMAs were calculated (short & long)
3. ✅ Crossovers were detected (15 trades found)
4. ✅ Trades were simulated (entry/exit prices tracked)
5. ✅ Metrics were computed (all 5 metrics calculated)

**The entire backtesting pipeline is working!**

---

**Your API is fully functional and ready for demo! 🚀**
