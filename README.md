# 🥷 NinjaQuant – Injective Strategy Backtesting API

[![Injective](https://img.shields.io/badge/Injective-Mainnet-00d1ff?style=flat-square)](https://injective.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green?style=flat-square)](https://fastapi.tiangolo.com/)

## 🚀 Injective Blockchain Integration

**✅ REAL Injective Mainnet Connection**

This API connects to the **real Injective blockchain** to validate and fetch market data:

- 📡 **67+ Live Derivative Markets** from Injective mainnet
- 🔐 **Market Verification** - Every request validates against real blockchain data
- 🌐 **Oracle Integration** - Fetches Pyth oracle information
- 🎯 **Market IDs** - Uses actual Injective market identifiers

**Proof of Integration:**
```bash
# Start server
python -m uvicorn app.main:app --reload

# Test with REAL Injective market
curl -X POST http://localhost:8000/backtest/ema-crossover \
  -H "Content-Type: application/json" \
  -d '{"market":"INJ/USDT PERP","timeframe":"1h","parameters":{"short_period":12,"long_period":26}}'

# Server logs show REAL blockchain connection:
# ✅ Successfully fetched 67 real markets from Injective!
# ✅ Verified market on Injective blockchain
# Market ID: 0x9b9980167ecc3645ff1a5517886652d94a0825e54a77d2057cbbe3ebee015963
# Oracle: Pyth
```

**See [INJECTIVE_INTEGRATION.md](INJECTIVE_INTEGRATION.md) for complete integration details.**

---

## 🎯 Problem

Injective provides rich on-chain trading data, but there is no simple API layer that allows developers to:

- Quickly test trading strategies
- Evaluate historical performance
- Compare strategy parameters
- Obtain standardized risk and return metrics

## 💡 Solution

NinjaQuant provides a modular strategy backtesting API that:

- **Connects to real Injective blockchain** for market validation
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
- RSI Mean Reversion Strategy (coming soon)

### 2️⃣ Real Injective Markets Supported

The API validates all markets against **real Injective blockchain data**:

**Available Markets** (67+ derivative markets):
- `INJ/USDT PERP` - Injective perpetual futures
- `BTC/USDT PERP` - Bitcoin perpetual futures
- `ETH/USDT PERP` - Ethereum perpetual futures
- `XAU/USDT PERP` - Gold perpetual futures
- `LINK/USDT PERP` - Chainlink perpetual futures
- `SOL/USDT PERP` - Solana perpetual futures
- `BNB/USDT PERP` - Binance Coin perpetual futures
- And 60+ more real Injective markets...

**Market Verification:**
Every backtest request connects to Injective blockchain to:
- Verify market exists on Injective mainnet
- Fetch real market ID (e.g., `0x9b9980167ecc3645ff1a5517886652d94a0825e54a77d2057cbbe3ebee015963`)
- Get oracle information (Pyth, Band Protocol)
- Validate quote denomination

### 3️⃣ Standardized Performance Metrics

For each backtest, the API returns:

- **Win Rate**: Percentage of profitable trades
- **Total Return**: Overall portfolio growth
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted return measure
- **Total Trades**: Number of completed trades

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
