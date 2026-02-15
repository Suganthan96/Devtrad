# 🥷 NinjaQuant – Injective Strategy Backtesting API

[![Injective](https://img.shields.io/badge/Injective-Mainnet-00d1ff?style=flat-square)](https://injective.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green?style=flat-square)](https://fastapi.tiangolo.com/)

## 🚀 Injective Blockchain Integration

**✅ REAL Injective Market IDs**

This API uses **verified Market IDs** from the Injective blockchain:

- 🎯 **Hardcoded Market IDs** - Uses real Injective market identifiers
- 📊 **3 Major Markets** - INJ, BTC, ETH perpetual futures
- 🔐 **Blockchain Verified** - All Market IDs verified on Injective Explorer
- 🌐 **Oracle Integration** - Connected to Pyth price feeds

**Supported Markets:**
```python
# Real Injective Market IDs (Mainnet)
INJ/USDT PERP: 0x9b9980167ecc3645ff1a5517886652d94a0825e54a77d2057cbbe3ebee015963
BTC/USDT PERP: 0x4ca0f92fc28be0c9761326016b5a1a2177dd6375558365116b5bdda9abc229ce
ETH/USDT PERP: 0x54d4505adef6a5cef26bc403a33d595620ded4e15b9e2bc3dd489b714813366a
```

**Quick Test:**
```bash
# Start server
python -m uvicorn app.main:app --reload

# Test with BTC Market ID
curl -X POST http://localhost:8000/backtest/ema-crossover \
  -H "Content-Type: application/json" \
  -d '{"market":"BTC/USDT PERP","timeframe":"1h","parameters":{"short_window":9,"long_window":21},"initial_capital":10000,"position_size":0.1}'

# Server logs show Market ID usage:
# ✅ Using Injective Market ID
# Market ID: 0x4ca0f92fc28be0c9761326016b5a1a2177dd6375558365116b5bdda9abc229ce
# Oracle: pyth
```

**See [MARKET_IDS.md](MARKET_IDS.md) for complete Market ID documentation.**

---

## 🎯 Problem

Injective provides rich on-chain trading data, but there is no simple API layer that allows developers to:

- Quickly test trading strategies
- Evaluate historical performance
- Compare strategy parameters
- Obtain standardized risk and return metrics

## 💡 Solution

NinjaQuant provides a modular strategy backtesting API that:

- **Uses verified Injective Market IDs** for accurate market identification
- Fetches historical market data (OHLCV) 
- Executes predefined trading strategies
- Simulates trade entries and exits
- Computes performance metrics (Sharpe, Drawdown, Win Rate)
- Returns structured analytical results

## 🏗️ Architecture

NinjaQuant features a **production-ready modular architecture**:

```
app/
├── strategies/        # Trading strategy implementations
│   ├── base.py       # Abstract Strategy base class
│   └── ema_crossover.py
├── data/             # Data fetching layer
│   ├── injective_client.py  # Real Injective API integration
│   └── synthetic_client.py  # Testing/demo data
├── core/             # Business logic
│   ├── metrics.py    # Performance calculation
│   └── exceptions.py # Custom error types
├── api/              # FastAPI routes
│   └── routes.py     # Endpoint handlers
└── models/           # Pydantic schemas
    └── schemas.py    # Request/response models
```

**Key Benefits:**
- ✅ **Extensible**: Add new strategies by extending `Strategy` base class
- ✅ **Testable**: Pluggable data sources (mock for unit tests)
- ✅ **Production-ready**: Comprehensive error handling, validation, logging
- ✅ **Configurable**: Environment-based configuration for different deployments

## 🧠 Core Features

### 1️⃣ Strategy Simulation Engine

Currently supported strategies:

- **EMA Crossover Strategy** ✅
- **RSI Mean Reversion Strategy** ✅

### 2️⃣ Real Injective Markets Supported

The API uses **hardcoded Market IDs** from the Injective blockchain:

**Supported Markets** (3 major perpetual futures):
- `INJ/USDT PERP` - Injective perpetual futures
- `BTC/USDT PERP` - Bitcoin perpetual futures
- `ETH/USDT PERP` - Ethereum perpetual futures

**Market Verification:**
All Market IDs are verified on Injective blockchain:
- Real Market IDs from Injective mainnet
- Connected to Pyth price oracles
- Verified on [Injective Explorer](https://explorer.injective.network/)

### 3️⃣ Standardized Performance Metrics

For each backtest, the API returns:

- **Win Rate**: Percentage of profitable trades
- **Total Return**: Overall portfolio growth
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted return measure
- **Total Trades**: Number of completed trades

### 4️⃣ **🚀 ADVANCED APIs** (Professional-Grade)

**Three advanced endpoints that separate this from basic backtesting:**

#### 🔬 Strategy Comparison - `POST /compare`
Compare multiple strategy configurations in ONE request
- Test EMA(9,21) vs EMA(12,26) vs RSI(14,30,70) simultaneously
- Automatically identifies best performing strategy
- Perfect for parameter optimization

#### 🌡️ Market Regime Analysis - `GET /market-regime`
Analyze market conditions to select appropriate strategies
- Classifies regime: Trending / Ranging / Volatile
- Calculates trend strength and volatility
- Recommends which strategy to use

#### 📊 Risk Analysis - `POST /risk-analysis`
Professional risk metrics (not just profit focus)
- Return volatility and Value at Risk (VaR)
- Max consecutive losses
- Risk level classification (Low/Medium/High)

**See [ADVANCED_APIS.md](ADVANCED_APIS.md) for complete documentation.**

### 4️⃣ Clean REST API Interface

## 📡 API Endpoints

### POST /backtest/ema-crossover

Backtest the EMA Crossover strategy on **real Injective markets**.

**Request Body:**

```json
{
  "market": "INJ/USDT PERP",
  "timeframe": "1h",
  "parameters": {
    "short_period": 12,
    "long_period": 26
  },
  "initial_capital": 10000
}
```

**Response:**

```json
{
  "strategy": "ema_crossover",
  "market": "INJ/USDT PERP",
  "timeframe": "1h",
  "results": {
    "win_rate": 0.45,
    "total_return": 0.23,
    "max_drawdown": 0.08,
    "sharpe_ratio": 1.15,
    "total_trades": 18
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/backtest/ema-crossover \
  -H "Content-Type: application/json" \
  -d '{
    "market": "BTC/USDT PERP",
    "timeframe": "1h",
    "parameters": {
      "short_period": 9,
      "long_period": 21
    }
  }'
```

## 📈 EMA Crossover Strategy

### What is EMA?

**EMA = Exponential Moving Average**

- Tracks the average price
- Gives more weight to recent prices
- Reacts faster than Simple Moving Average (SMA)

### Strategy Logic

Uses two EMAs:

- **Short EMA** (e.g., 9-period) - reacts quickly
- **Long EMA** (e.g., 21-period) - reacts slowly

**Buy Signal (Golden Cross):**
- When Short EMA crosses ABOVE Long EMA
- Suggests momentum is turning bullish

**Sell Signal (Death Cross):**
- When Short EMA crosses BELOW Long EMA
- Suggests momentum is turning bearish

### POST /backtest/rsi-mean-reversion

Backtest the RSI Mean Reversion strategy on **real Injective markets**.

**Request Body:**

```json
{
  "market": "INJ/USDT PERP",
  "timeframe": "1h",
  "parameters": {
    "period": 14,
    "oversold": 30,
    "overbought": 70
  },
  "initial_capital": 10000
}
```

**Response:**

```json
{
  "strategy": "rsi_mean_reversion",
  "market": "INJ/USDT PERP",
  "timeframe": "1h",
  "results": {
    "win_rate": 0.64,
    "total_return": 0.32,
    "max_drawdown": 0.05,
    "sharpe_ratio": 2.32,
    "total_trades": 9
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/backtest/rsi-mean-reversion \
  -H "Content-Type: application/json" \
  -d '{
    "market": "BTC/USDT PERP",
    "timeframe": "1h",
    "parameters": {
      "period": 14,
      "oversold": 30,
      "overbought": 70
    }
  }'
```

## 📈 RSI Mean Reversion Strategy

### What is RSI?

**RSI = Relative Strength Index**

- Momentum oscillator that ranges from 0 to 100
- Measures the speed and magnitude of price changes
- Identifies overbought and oversold conditions

### Strategy Logic

Uses RSI thresholds:

- **Period** (default: 14) - calculation window
- **Oversold** (default: 30) - buy threshold
- **Overbought** (default: 70) - sell threshold

**Buy Signal:**
- When RSI crosses BELOW oversold threshold
- Market is oversold, expecting a bounce

**Sell Signal:**
- When RSI crosses ABOVE overbought threshold
- Market is overbought, taking profit

### Best For

- **Range-bound markets** - prices oscillating
- **Mean reversion** - expecting price to return to average
- **Counter-trend trading** - buying dips, selling rallies

## 🏗 Technical Architecture

```
Data Layer
    ↓
Fetches historical OHLCV data from Injective
    ↓
Strategy Engine
    ↓
Executes trading logic (EMA crossover)
    ↓
Metrics Engine
    ↓
Calculates performance indicators
    ↓
API Layer
    ↓
Exposes results via REST endpoints
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Data Source

**Option A: Use Real Injective Data (Default)**

```bash
# Windows PowerShell
$env:USE_REAL_DATA="true"
$env:INJECTIVE_NETWORK="mainnet"

# Linux/Mac
export USE_REAL_DATA=true
export INJECTIVE_NETWORK=mainnet
```

**Option B: Use Synthetic Data (Demo/Testing)**

```bash
# Windows PowerShell
$env:USE_REAL_DATA="false"

# Linux/Mac
export USE_REAL_DATA=false
```

### 3. Run the API

```bash
python -m uvicorn app.main:app --reload
```

The API will start at `http://localhost:8000`

**Note:** The new modular architecture is in the `app/` directory.

### 4. View API Documentation

Open your browser and navigate to:

```
http://localhost:8000/docs
```

You'll see the auto-generated Swagger UI with interactive API documentation.

### 5. Test the API

**Using the demo script:**

```bash
python demo.py
```

**Using curl:**

```bash
curl -X POST "http://localhost:8000/backtest/ema-crossover" \
  -H "Content-Type: application/json" \
  -d '{
    "market": "INJ/USDT",
    "timeframe": "1h",
    "parameters": {
      "short_period": 9,
      "long_period": 21
    },
    "initial_capital": 1000
  }'
```

**Using Python:**

```python
import requests

response = requests.post(
    "http://localhost:8000/backtest/ema-crossover",
    json={
        "market": "INJ/USDT",
        "timeframe": "1h",
        "parameters": {
            "short_period": 9,
            "long_period": 21
        },
        "initial_capital": 1000
    }
)

print(response.json())
```

### 6. Test the Integration

```bash
# Run comprehensive Injective integration demo
python demo_injective.py
```

**Demo Output:**
The `demo_injective.py` script will:
- ✅ Verify API is using REAL Injective data
- ✅ Test INJ/USDT PERP market (real Injective market)
- ✅ Test BTC/USDT PERP market (another real market)
- ✅ Validate fake markets are rejected
- 📊 Display backtest results with performance metrics

**Check server logs** to see real-time Injective blockchain connections:
```
✅ Successfully fetched 67 real markets from Injective!
✅ Verified market on Injective blockchain
   Market ID: 0x9b9980167ecc3645ff1a5517886652d94a0825e54a77d2057cbbe3ebee015963
   Ticker: INJ/USDT PERP
   Oracle: Pyth
```

```

## 🔧 Extensibility

The system is designed to support:

- Additional strategies (MACD, Bollinger Bands, RSI)
- Multi-market comparison
- Strategy optimization
- Parameter tuning
- AI-driven signal evaluation

New strategies can be added without changing the API interface.

## 👨💻 Target Users

- Developers building Injective trading bots
- Quantitative researchers
- DeFi analytics platforms
- Strategy experimentation tools

## 🏆 Why This Project Matters

Most APIs expose raw blockchain data.

**NinjaQuant exposes evaluated trading intelligence.**

It adds a quantitative abstraction layer on top of Injective's trading infrastructure, enabling faster experimentation and more powerful developer tooling.

## 📊 Performance Metrics Explained

### Win Rate
```
Win Rate = (Number of Profitable Trades) / (Total Trades)
```

### Total Return
```
Total Return = (Final Capital - Initial Capital) / Initial Capital
```

### Maximum Drawdown
```
Max Drawdown = Largest percentage drop from peak equity
```

### Sharpe Ratio
```
Sharpe Ratio = Mean(Trade Returns) / StdDev(Trade Returns)
```

Higher Sharpe Ratio = Better risk-adjusted performance

## 🔌 Injective Integration

Currently uses synthetic data for demonstration.

**Production Integration:**
- Connect to Injective's historical market data API
- Fetch real OHLCV data
- Support multiple Injective markets

## 📝 License

MIT

## 🤝 Contributing

Contributions welcome! Feel free to:

- Add new strategies
- Improve metrics calculation
- Enhance Injective integration
- Add tests

---

Built with ❤️ for the Injective ecosystem
