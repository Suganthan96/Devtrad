# 📮 Postman API Testing Guide - NinjaQuant

## Overview

This guide provides **complete Postman test cases** for all NinjaQuant APIs, including:
- ✅ 2 Backtesting endpoints
- ✅ 3 Advanced endpoints (Strategy Comparison, Market Regime, Risk Analysis)

---

## 🚀 Quick Setup

### 1. Start the Server

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Server will run at: `http://localhost:8000`

### 2. Import into Postman

1. Open Postman
2. Click **Import** → **Raw Text**
3. Paste the JSON collection below (see bottom of this file)
4. Click **Import**

---

## 📋 API Endpoints Summary

| # | Method | Endpoint | Purpose |
|---|--------|----------|---------|
| 1 | GET | `/` | Health check |
| 2 | POST | `/backtest/ema-crossover` | EMA strategy backtest |
| 3 | POST | `/backtest/rsi-mean-reversion` | RSI strategy backtest |
| 4 | POST | `/compare` | **Compare multiple strategies** |
| 5 | GET | `/market-regime` | **Market regime analysis** |
| 6 | POST | `/risk-analysis` | **Risk metrics analysis** |

---

## 🧪 Test Cases

### Test #1: Health Check ✅

**Request:**
```
GET http://localhost:8000/
```

**Expected Response (200 OK):**
```json
{
  "message": "Welcome to NinjaQuant API",
  "version": "1.0.0",
  "docs": "/docs",
  "endpoints": {
    "backtest": [
      "/backtest/ema-crossover",
      "/backtest/rsi-mean-reversion"
    ],
    "advanced": [
      "/compare",
      "/market-regime",
      "/risk-analysis"
    ]
  },
  "data_mode": "real"
}
```

**✅ Success Criteria:**
- Status code: 200
- Response contains all 5 API endpoints
- `data_mode` shows "real"

---

### Test #2: EMA Crossover Backtest - Basic ✅

**Request:**
```
POST http://localhost:8000/backtest/ema-crossover
Content-Type: application/json

{
  "market": "BTC/USDT PERP",
  "timeframe": "1h",
  "parameters": {
    "short_period": 9,
    "long_period": 21
  },
  "initial_capital": 10000
}
```

**Expected Response (200 OK):**
```json
{
  "strategy": "ema_crossover",
  "market": "BTC/USDT PERP",
  "timeframe": "1h",
  "results": {
    "win_rate": 0.45,
    "total_return": 0.1082,
    "max_drawdown": 0.1665,
    "sharpe_ratio": 0.1483,
    "total_trades": 11
  }
}
```

**✅ Success Criteria:**
- Status code: 200
- Contains `results` with all 5 metrics
- `win_rate` between 0 and 1
- `total_trades` > 0

---

### Test #3: EMA Crossover - Different Markets 🌍

Test with all three supported markets:

#### BTC/USDT PERP
```json
{
  "market": "BTC/USDT PERP",
  "timeframe": "1h",
  "parameters": {"short_period": 9, "long_period": 21},
  "initial_capital": 10000
}
```

#### ETH/USDT PERP
```json
{
  "market": "ETH/USDT PERP",
  "timeframe": "1h",
  "parameters": {"short_period": 9, "long_period": 21},
  "initial_capital": 10000
}
```

#### INJ/USDT PERP
```json
{
  "market": "INJ/USDT PERP",
  "timeframe": "1h",
  "parameters": {"short_period": 9, "long_period": 21},
  "initial_capital": 10000
}
```

**✅ Success Criteria:**
- All three markets return 200 OK
- Different markets produce different results

---

### Test #4: EMA Crossover - Parameter Variations 🔧

Test different EMA periods:

#### Conservative (Slower)
```json
{
  "market": "BTC/USDT PERP",
  "timeframe": "1h",
  "parameters": {"short_period": 20, "long_period": 50},
  "initial_capital": 10000
}
```

#### Aggressive (Faster)
```json
{
  "market": "BTC/USDT PERP",
  "timeframe": "1h",
  "parameters": {"short_period": 5, "long_period": 15},
  "initial_capital": 10000
}
```

#### Standard
```json
{
  "market": "BTC/USDT PERP",
  "timeframe": "1h",
  "parameters": {"short_period": 12, "long_period": 26},
  "initial_capital": 10000
}
```

**✅ Success Criteria:**
- All configurations return valid results
- Faster periods = more trades
- Slower periods = fewer trades

---

### Test #5: RSI Mean Reversion - Basic ✅

**Request:**
```
POST http://localhost:8000/backtest/rsi-mean-reversion
Content-Type: application/json

{
  "market": "ETH/USDT PERP",
  "timeframe": "1h",
  "parameters": {
    "period": 14,
    "oversold": 30,
    "overbought": 70
  },
  "initial_capital": 10000
}
```

**Expected Response (200 OK):**
```json
{
  "strategy": "rsi_mean_reversion",
  "market": "ETH/USDT PERP",
  "timeframe": "1h",
  "results": {
    "win_rate": 0.5556,
    "total_return": 0.5033,
    "max_drawdown": 0.0721,
    "sharpe_ratio": 0.5884,
    "total_trades": 9
  }
}
```

**✅ Success Criteria:**
- Status code: 200
- Strategy is "rsi_mean_reversion"
- All metrics present

---

### Test #6: RSI - Parameter Variations 🎯

#### Tight Thresholds (More Trades)
```json
{
  "market": "BTC/USDT PERP",
  "timeframe": "1h",
  "parameters": {
    "period": 14,
    "oversold": 40,
    "overbought": 60
  },
  "initial_capital": 10000
}
```

#### Wide Thresholds (Fewer Trades)
```json
{
  "market": "BTC/USDT PERP",
  "timeframe": "1h",
  "parameters": {
    "period": 14,
    "oversold": 20,
    "overbought": 80
  },
  "initial_capital": 10000
}
```

**✅ Success Criteria:**
- Tight thresholds = more trades
- Wide thresholds = fewer trades

---

### Test #7: 🔬 Strategy Comparison - Basic ✅

**Request:**
```
POST http://localhost:8000/compare
Content-Type: application/json

{
  "market": "BTC/USDT PERP",
  "timeframe": "1h",
  "strategies": [
    {
      "strategy": "ema_crossover",
      "parameters": {
        "short_period": 9,
        "long_period": 21
      }
    },
    {
      "strategy": "ema_crossover",
      "parameters": {
        "short_period": 12,
        "long_period": 26
      }
    },
    {
      "strategy": "rsi_mean_reversion",
      "parameters": {
        "period": 14,
        "oversold": 30,
        "overbought": 70
      }
    }
  ],
  "initial_capital": 10000
}
```

**Expected Response (200 OK):**
```json
{
  "market": "BTC/USDT PERP",
  "timeframe": "1h",
  "comparison": [
    {
      "strategy_name": "ema_9_21",
      "win_rate": 0.3,
      "total_return": 0.8317,
      "sharpe_ratio": 0.3377,
      "max_drawdown": 0.1887,
      "total_trades": 10
    },
    {
      "strategy_name": "ema_12_26",
      "win_rate": 0.3333,
      "total_return": 0.8296,
      "sharpe_ratio": 0.36,
      "max_drawdown": 0.2097,
      "total_trades": 9
    },
    {
      "strategy_name": "rsi_14_30_70",
      "win_rate": 0.8,
      "total_return": 0.2693,
      "sharpe_ratio": 0.6222,
      "max_drawdown": 0.0761,
      "total_trades": 10
    }
  ],
  "best_strategy": "ema_9_21"
}
```

**✅ Success Criteria:**
- Status code: 200
- Returns comparison for all 3 strategies
- `best_strategy` is identified
- Each strategy has complete metrics

---

### Test #8: 🔬 Strategy Comparison - Multiple EMA Configs

Test different EMA parameter combinations:

**Request:**
```json
{
  "market": "ETH/USDT PERP",
  "timeframe": "1h",
  "strategies": [
    {"strategy": "ema_crossover", "parameters": {"short_period": 5, "long_period": 15}},
    {"strategy": "ema_crossover", "parameters": {"short_period": 9, "long_period": 21}},
    {"strategy": "ema_crossover", "parameters": {"short_period": 12, "long_period": 26}},
    {"strategy": "ema_crossover", "parameters": {"short_period": 20, "long_period": 50}}
  ],
  "initial_capital": 10000
}
```

**✅ Success Criteria:**
- All 4 EMA configs compared
- Best strategy identified
- Results sorted or clearly comparable

---

### Test #9: 🌡️ Market Regime Analysis - BTC ✅

**Request:**
```
GET http://localhost:8000/market-regime?market=BTC/USDT PERP&timeframe=1h
```

**Expected Response (200 OK):**
```json
{
  "market": "BTC/USDT PERP",
  "timeframe": "1h",
  "regime": "Volatile",
  "trend_strength": 0.1041,
  "volatility_level": "High",
  "volatility_value": 2.0006,
  "price_change_pct": 0.3684
}
```

**✅ Success Criteria:**
- Status code: 200
- `regime` is one of: "Trending", "Ranging", "Volatile"
- `volatility_level` is one of: "Low", "Medium", "High"
- `trend_strength` between 0 and 1

---

### Test #10: 🌡️ Market Regime - All Markets

Test regime analysis for all markets:

#### BTC
```
GET http://localhost:8000/market-regime?market=BTC/USDT PERP&timeframe=1h
```

#### ETH
```
GET http://localhost:8000/market-regime?market=ETH/USDT PERP&timeframe=1h
```

#### INJ
```
GET http://localhost:8000/market-regime?market=INJ/USDT PERP&timeframe=1h
```

**✅ Success Criteria:**
- All three markets return different regimes
- Each has complete regime data
- Trend strength and volatility values vary

---

### Test #11: 📊 Risk Analysis - RSI Strategy ✅

**Request:**
```
POST http://localhost:8000/risk-analysis
Content-Type: application/json

{
  "market": "ETH/USDT PERP",
  "timeframe": "1h",
  "strategy": "rsi_mean_reversion",
  "parameters": {
    "period": 14,
    "oversold": 30,
    "overbought": 70
  },
  "initial_capital": 10000
}
```

**Expected Response (200 OK):**
```json
{
  "strategy": "rsi_mean_reversion",
  "market": "ETH/USDT PERP",
  "timeframe": "1h",
  "risk_metrics": {
    "return_volatility": 0.065,
    "max_consecutive_losses": 3,
    "largest_loss": -0.1458,
    "avg_loss": -0.0593,
    "risk_level": "Low",
    "value_at_risk_95": -0.0948
  },
  "performance_summary": {
    "win_rate": 0.5294,
    "total_return": -0.0738,
    "max_drawdown": 0.2135,
    "sharpe_ratio": -0.036,
    "total_trades": 17
  }
}
```

**✅ Success Criteria:**
- Status code: 200
- `risk_level` is one of: "Low", "Medium", "High"
- All risk metrics present
- Performance summary included

---

### Test #12: 📊 Risk Analysis - EMA Strategy

**Request:**
```json
{
  "market": "BTC/USDT PERP",
  "timeframe": "1h",
  "strategy": "ema_crossover",
  "parameters": {
    "short_period": 9,
    "long_period": 21
  },
  "initial_capital": 10000
}
```

**✅ Success Criteria:**
- Status code: 200
- Risk level calculated
- VaR (95%) is negative (represents loss)

---

## ❌ Error Test Cases

### Test #13: Invalid Market

**Request:**
```json
{
  "market": "INVALID/USDT PERP",
  "timeframe": "1h",
  "parameters": {"short_period": 9, "long_period": 21},
  "initial_capital": 10000
}
```

**Expected Response (404):**
```json
{
  "detail": "Market 'INVALID/USDT PERP' not supported. Available markets: INJ/USDT PERP, BTC/USDT PERP, ETH/USDT PERP"
}
```

---

### Test #14: Invalid Parameters - Short > Long

**Request:**
```json
{
  "market": "BTC/USDT PERP",
  "timeframe": "1h",
  "parameters": {
    "short_period": 50,
    "long_period": 20
  },
  "initial_capital": 10000
}
```

**Expected Response (422):**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "parameters", "long_period"],
      "msg": "Value error, long_period must be greater than short_period"
    }
  ]
}
```

---

### Test #15: Invalid RSI Thresholds

**Request:**
```json
{
  "market": "BTC/USDT PERP",
  "timeframe": "1h",
  "parameters": {
    "period": 14,
    "oversold": 70,
    "overbought": 30
  },
  "initial_capital": 10000
}
```

**Expected Response (422):**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "parameters", "overbought"],
      "msg": "Value error, overbought must be greater than oversold"
    }
  ]
}
```

---

### Test #16: Missing Required Fields

**Request:**
```json
{
  "market": "BTC/USDT PERP",
  "timeframe": "1h"
}
```

**Expected Response (422):**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "parameters"],
      "msg": "Field required"
    }
  ]
}
```

---

### Test #17: Invalid Timeframe

**Request:**
```json
{
  "market": "BTC/USDT PERP",
  "timeframe": "30m",
  "parameters": {"short_period": 9, "long_period": 21},
  "initial_capital": 10000
}
```

**Expected Response (422):**
```json
{
  "detail": [
    {
      "type": "string_pattern_mismatch",
      "loc": ["body", "timeframe"],
      "msg": "String should match pattern '^(1m|5m|15m|1h|4h|1d)$'"
    }
  ]
}
```

---

## 🎯 Complete Test Workflow

### Scenario: Find Best Strategy for Current Market

```
Step 1: Check market regime
GET /market-regime?market=BTC/USDT PERP&timeframe=1h
→ Result: "Trending"

Step 2: Compare strategies suitable for trending market
POST /compare
Body: {multiple EMA configurations}
→ Result: "ema_12_26" is best

Step 3: Analyze risk of best strategy
POST /risk-analysis
Body: {ema_12_26 config}
→ Result: "Medium" risk

Step 4: Execute backtest with chosen strategy
POST /backtest/ema-crossover
Body: {ema_12_26 config}
→ Result: Detailed performance metrics
```

---

## 📊 Performance Benchmarks

Expected response times (for reference):

| Endpoint | Expected Time |
|----------|---------------|
| `/` | < 50ms |
| `/backtest/*` | 500-1000ms |
| `/compare` | 1000-3000ms (runs multiple backtests) |
| `/market-regime` | 200-500ms |
| `/risk-analysis` | 500-1000ms |

---

## 🔧 Postman Environment Variables

Create these variables for easier testing:

```
base_url: http://localhost:8000
market_btc: BTC/USDT PERP
market_eth: ETH/USDT PERP
market_inj: INJ/USDT PERP
timeframe: 1h
capital: 10000
```

Then use in requests:
```
{{base_url}}/backtest/ema-crossover
```

---

## 📦 Postman Collection JSON

Import this into Postman:

```json
{
  "info": {
    "name": "NinjaQuant API - Complete Collection",
    "description": "All endpoints including Advanced APIs",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "1. Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": [""]
        }
      }
    },
    {
      "name": "2. EMA Backtest - BTC",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"market\": \"BTC/USDT PERP\",\n  \"timeframe\": \"1h\",\n  \"parameters\": {\n    \"short_period\": 9,\n    \"long_period\": 21\n  },\n  \"initial_capital\": 10000\n}"
        },
        "url": {
          "raw": "http://localhost:8000/backtest/ema-crossover",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["backtest", "ema-crossover"]
        }
      }
    },
    {
      "name": "3. RSI Backtest - ETH",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"market\": \"ETH/USDT PERP\",\n  \"timeframe\": \"1h\",\n  \"parameters\": {\n    \"period\": 14,\n    \"oversold\": 30,\n    \"overbought\": 70\n  },\n  \"initial_capital\": 10000\n}"
        },
        "url": {
          "raw": "http://localhost:8000/backtest/rsi-mean-reversion",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["backtest", "rsi-mean-reversion"]
        }
      }
    },
    {
      "name": "4. Strategy Comparison",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"market\": \"BTC/USDT PERP\",\n  \"timeframe\": \"1h\",\n  \"strategies\": [\n    {\n      \"strategy\": \"ema_crossover\",\n      \"parameters\": {\"short_period\": 9, \"long_period\": 21}\n    },\n    {\n      \"strategy\": \"ema_crossover\",\n      \"parameters\": {\"short_period\": 12, \"long_period\": 26}\n    },\n    {\n      \"strategy\": \"rsi_mean_reversion\",\n      \"parameters\": {\"period\": 14, \"oversold\": 30, \"overbought\": 70}\n    }\n  ],\n  \"initial_capital\": 10000\n}"
        },
        "url": {
          "raw": "http://localhost:8000/compare",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["compare"]
        }
      }
    },
    {
      "name": "5. Market Regime - BTC",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/market-regime?market=BTC/USDT PERP&timeframe=1h",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["market-regime"],
          "query": [
            {"key": "market", "value": "BTC/USDT PERP"},
            {"key": "timeframe", "value": "1h"}
          ]
        }
      }
    },
    {
      "name": "6. Risk Analysis - RSI",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"market\": \"ETH/USDT PERP\",\n  \"timeframe\": \"1h\",\n  \"strategy\": \"rsi_mean_reversion\",\n  \"parameters\": {\n    \"period\": 14,\n    \"oversold\": 30,\n    \"overbought\": 70\n  },\n  \"initial_capital\": 10000\n}"
        },
        "url": {
          "raw": "http://localhost:8000/risk-analysis",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["risk-analysis"]
        }
      }
    }
  ]
}
```

---

## ✅ Testing Checklist

- [ ] **Test #1**: Health check returns all endpoints
- [ ] **Test #2**: EMA basic backtest works
- [ ] **Test #3**: All 3 markets (BTC, ETH, INJ) work
- [ ] **Test #4**: Different EMA parameters produce different results
- [ ] **Test #5**: RSI basic backtest works
- [ ] **Test #6**: RSI parameter variations work
- [ ] **Test #7**: Strategy comparison compares 3+ strategies
- [ ] **Test #8**: Strategy comparison identifies best strategy
- [ ] **Test #9**: Market regime analysis works for BTC
- [ ] **Test #10**: Market regime works for all 3 markets
- [ ] **Test #11**: Risk analysis generates risk metrics
- [ ] **Test #12**: Risk analysis works for both strategies
- [ ] **Test #13-17**: All error cases return proper error messages

---

## 🎉 Success Criteria Summary

✅ **All APIs return 200 OK** for valid requests  
✅ **Error handling works** - proper 4xx responses for invalid inputs  
✅ **Data consistency** - metrics are within expected ranges  
✅ **Performance** - responses under 3 seconds  
✅ **Complete data** - all fields present in responses  

---

## 🚀 Quick Start Command

```bash
# Start server
python -m uvicorn app.main:app --reload --port 8000

# Run automated test (Python)
python demo_advanced_apis.py

# Or test manually in Postman using this guide
```

---

**Your NinjaQuant API is ready for comprehensive testing! 🥷**
