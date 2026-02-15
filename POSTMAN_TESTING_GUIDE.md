# 📮 Postman API Testing Guide - NinjaQuant

Complete testing guide for the NinjaQuant Injective Strategy Backtesting API.

---

## 🚀 Quick Start

### Import Collection

1. Open Postman
2. Click **Import** → **Upload Files**
3. Select `Postman_Complete_Collection.json`
4. Collection will appear in left sidebar

### Configure Environment

**Set Base URL Variable:**
- Local: `http://localhost:8000`
- Railway: `https://your-app.up.railway.app`
- Render: `https://your-app.onrender.com`

**Steps:**
1. Click collection name → **Variables** tab
2. Update `BASE_URL` value
3. Save

---

## 📋 Test Categories

### 1️⃣ Health & Info (3 tests)

**Purpose:** Verify API is running and check configuration

| Test | Endpoint | Expected |
|------|----------|----------|
| Root - API Info | `GET /` | API version, endpoints list |
| Health Check | `GET /health` | Health status |
| API Documentation | `GET /docs` | Swagger UI |

**Example Response:**
```json
{
  "message": "Welcome to NinjaQuant API",
  "version": "1.0.0",
  "endpoints": [
    "/backtest/ema-crossover",
    "/backtest/rsi-mean-reversion"
  ],
  "data_mode": "real"
}
```

---

### 2️⃣ EMA Strategy Tests (8 tests)

**Standard Tests:**

| Market | Timeframe | Short | Long | Capital | Purpose |
|--------|-----------|-------|------|---------|---------|
| INJ/USDT PERP | 1h | 9 | 21 | $1,000 | Baseline test |
| BTC/USDT PERP | 1h | 9 | 21 | $10,000 | Bitcoin test |
| ETH/USDT PERP | 1h | 9 | 21 | $5,000 | Ethereum test |

**Parameter Variations:**

| Type | Short | Long | Timeframe | Description |
|------|-------|------|-----------|-------------|
| Fast | 5 | 13 | 1h | More frequent signals |
| Medium | 12 | 26 | 1h | MACD-style periods |
| Slow | 20 | 50 | 4h | Fewer, stronger signals |

**Timeframe Tests:**
- **15min:** Scalping strategy
- **1h:** Standard intraday
- **4h:** Swing trading
- **1d:** Position trading

---

### 3️⃣ RSI Strategy Tests (9 tests)

**Standard Tests:**

| Market | Timeframe | Period | Oversold | Overbought | Capital |
|--------|-----------|--------|----------|------------|---------|
| INJ/USDT PERP | 1h | 14 | 30 | 70 | $1,000 |
| BTC/USDT PERP | 1h | 14 | 30 | 70 | $10,000 |
| ETH/USDT PERP | 1h | 14 | 30 | 70 | $5,000 |

**Period Variations:**

| Type | Period | Description |
|------|--------|-------------|
| Fast | 7 | More sensitive to price changes |
| Standard | 14 | Default RSI setting |
| Slow | 21 | Smoother signals |

**Threshold Variations:**

| Type | Oversold | Overbought | Description |
|------|----------|------------|-------------|
| Wide Bands | 20 | 80 | Extreme conditions only |
| Standard | 30 | 70 | Default settings |
| Tight Bands | 40 | 60 | More frequent trades |
| Conservative | 25 | 75 | Balanced approach |

---

### 4️⃣ Error & Edge Cases (6 tests)

**Test invalid inputs to ensure proper error handling:**

| Test | Input | Expected Status | Expected Response |
|------|-------|----------------|-------------------|
| Invalid Market | "INVALID/MARKET" | 404 | Market not found error |
| Invalid Timeframe | "2h" | 422 | Validation error |
| EMA: short >= long | short=21, long=9 | 422 | Period validation error |
| RSI: oversold >= overbought | oversold=70, overbought=30 | 422 | Threshold validation error |
| Negative Capital | -1000 | 422 | Positive value required |
| Missing Fields | No timeframe | 422 | Required field error |

**Built-in Postman Tests:**
Each error test includes automatic validation:
```javascript
pm.test("Status code is 404", function () {
    pm.response.to.have.status(404);
});

pm.test("Error message present", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.detail).to.include('Market');
});
```

---

### 5️⃣ Performance Tests (2 tests)

**Test different capital sizes:**

| Test | Market | Capital | Purpose |
|------|--------|---------|---------|
| Large Capital | BTC/USDT PERP | $100,000 | Institutional size |
| Small Capital | INJ/USDT PERP | $100 | Retail size |

---

### 6️⃣ Strategy Comparison (2 tests)

**Compare EMA vs RSI on same market:**

Both tests use:
- Market: INJ/USDT PERP
- Timeframe: 1h
- Capital: $10,000

**Compare metrics:**
- Win Rate
- Total Return
- Sharpe Ratio
- Total Trades

---

## 🧪 Sample Test Bodies

### EMA Crossover - Standard
```json
{
  "market": "INJ/USDT PERP",
  "timeframe": "1h",
  "parameters": {
    "short_period": 9,
    "long_period": 21
  },
  "initial_capital": 1000
}
```

### RSI Mean Reversion - Standard
```json
{
  "market": "INJ/USDT PERP",
  "timeframe": "1h",
  "parameters": {
    "period": 14,
    "oversold": 30,
    "overbought": 70
  },
  "initial_capital": 1000
}
```

### EMA - Aggressive (Fast Scalping)
```json
{
  "market": "ETH/USDT PERP",
  "timeframe": "15m",
  "parameters": {
    "short_period": 5,
    "long_period": 13
  },
  "initial_capital": 5000
}
```

### RSI - Conservative (Wide Bands)
```json
{
  "market": "BTC/USDT PERP",
  "timeframe": "4h",
  "parameters": {
    "period": 21,
    "oversold": 20,
    "overbought": 80
  },
  "initial_capital": 10000
}
```

### RSI - Tight Scalping
```json
{
  "market": "INJ/USDT PERP",
  "timeframe": "15m",
  "parameters": {
    "period": 7,
    "oversold": 40,
    "overbought": 60
  },
  "initial_capital": 1000
}
```

---

## 📊 Understanding Responses

### Success Response (200)

```json
{
  "strategy": "rsi_mean_reversion",
  "market": "INJ/USDT PERP",
  "timeframe": "1h",
  "results": {
    "win_rate": 0.64,          // 64% winning trades
    "total_return": 0.32,       // 32% profit
    "max_drawdown": 0.05,       // 5% max loss from peak
    "sharpe_ratio": 2.32,       // Risk-adjusted return
    "total_trades": 9           // 9 completed trades
  }
}
```

**Metrics Explained:**

- **Win Rate**: Percentage of profitable trades (0.0 to 1.0)
  - `0.64` = 64% of trades were winners
  - Higher is better

- **Total Return**: Portfolio growth percentage (can be negative)
  - `0.32` = 32% profit ($1000 → $1320)
  - `-0.15` = 15% loss ($1000 → $850)

- **Max Drawdown**: Largest peak-to-trough decline (0.0 to 1.0)
  - `0.05` = 5% worst decline
  - Lower is better (less risk)

- **Sharpe Ratio**: Risk-adjusted return metric
  - `> 1.0` = Good risk-adjusted returns
  - `> 2.0` = Excellent
  - `< 0` = Negative returns

- **Total Trades**: Number of completed buy-sell cycles
  - More trades = more data points
  - Too few = unreliable statistics

---

## 🔍 Testing Workflows

### Basic Functionality Test
**Run in order:**
1. Root - API Info
2. EMA - INJ/USDT PERP (Standard)
3. RSI - INJ/USDT PERP (Standard)

**Expected:** All return 200 OK

---

### Parameter Optimization Test
**Test same market with different parameters:**

1. RSI - Fast (7 period)
2. RSI - Standard (14 period)
3. RSI - Slow (21 period)

**Goal:** Find optimal RSI period for the market

---

### Multi-Market Test
**Test strategy across all major markets:**

1. INJ/USDT PERP
2. BTC/USDT PERP
3. ETH/USDT PERP

**Goal:** Identify which market works best with strategy

---

### Timeframe Analysis
**Test same parameters across timeframes:**

| Timeframe | Use Case | Expected Trades |
|-----------|----------|----------------|
| 15m | Scalping | Many (>20) |
| 1h | Intraday | Moderate (10-20) |
| 4h | Swing | Few (5-10) |
| 1d | Position | Very few (<5) |

---

### Strategy Battle Test
**Compare EMA vs RSI head-to-head:**

1. Run: Compare - INJ/USDT PERP - EMA
2. Run: Compare - INJ/USDT PERP - RSI
3. Compare:
   - Which has higher win rate?
   - Which has better total return?
   - Which has better Sharpe ratio?
   - Which has more/fewer trades?

---

## ⚙️ Advanced Testing

### Custom Test Scripts

**Add to Postman Tests tab:**

**1. Assert Positive Win Rate:**
```javascript
pm.test("Win rate is positive", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.results.win_rate).to.be.at.least(0);
    pm.expect(jsonData.results.win_rate).to.be.at.most(1);
});
```

**2. Assert Has Trades:**
```javascript
pm.test("Strategy generated trades", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.results.total_trades).to.be.above(0);
});
```

**3. Assert Positive Return:**
```javascript
pm.test("Strategy is profitable", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.results.total_return).to.be.above(0);
});
```

**4. Calculate Final Capital:**
```javascript
pm.test("Calculate final portfolio value", function () {
    var jsonData = pm.response.json();
    var initial = 1000; // Set to your initial_capital
    var final = initial * (1 + jsonData.results.total_return);
    console.log("Final Capital: $" + final.toFixed(2));
});
```

**5. Performance Score:**
```javascript
pm.test("Calculate performance score", function () {
    var jsonData = pm.response.json();
    var score = (
        jsonData.results.win_rate * 30 +
        jsonData.results.sharpe_ratio * 20 +
        (1 - jsonData.results.max_drawdown) * 20 +
        Math.min(jsonData.results.total_return, 1) * 30
    );
    console.log("Performance Score: " + score.toFixed(2) + "/100");
});
```

---

## 🎯 Success Criteria

### Minimum Standards

| Metric | Good | Excellent |
|--------|------|-----------|
| Win Rate | > 50% | > 65% |
| Total Return | > 0% | > 20% |
| Max Drawdown | < 20% | < 10% |
| Sharpe Ratio | > 0.5 | > 1.5 |
| Total Trades | > 5 | > 10 |

---

## 🚨 Common Issues

### Connection Refused
**Error:** `Could not get response`
**Fix:** Ensure API is running: `python -m uvicorn app.main:app --reload`

### 404 Market Not Found
**Error:** `Market not found`
**Fix:** Check market name format. Must be uppercase with space before "PERP"
- ✅ `"INJ/USDT PERP"`
- ❌ `"inj/usdt perp"`
- ❌ `"INJ/USDTPERP"`

### 422 Validation Error
**Error:** `Validation failed`
**Fix:** Check request body matches schema exactly
- Timeframe must be: `1m`, `5m`, `15m`, `1h`, `4h`, or `1d`
- EMA: `short_period < long_period`
- RSI: `oversold < overbought`

### Timeout
**Error:** Request timeout
**Fix:** Increase Postman timeout: Settings → General → Request timeout

---

## 📈 Contest/Optimization Ideas

### Find Best Parameters
**Goal:** Maximize Sharpe Ratio on INJ/USDT PERP

**Test Grid:**
- RSI Periods: 7, 14, 21
- Oversold: 20, 30, 40
- Overbought: 60, 70, 80

Track results and find optimal combination.

---

### Multi-Strategy Portfolio
**Goal:** Diversify across strategies and markets

**Allocation:**
- 40% BTC/USDT PERP - EMA (9/21)
- 30% ETH/USDT PERP - RSI (14, 30/70)
- 30% INJ/USDT PERP - RSI (7, 40/60)

Calculate blended performance.

---

## 🔗 Quick Links

- **Local API:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/docs
- **Redoc:** http://localhost:8000/redoc

---

## 💡 Tips

1. **Run Collection:** Click collection → Run → Execute all tests
2. **Save Responses:** Click request → Save Response → Name it
3. **Compare Results:** Use collection runner with CSV data file
4. **Monitor:** Use Postman Monitor for scheduled testing
5. **Collaborate:** Export collection and share with team

---

**Happy Testing! 🚀**
