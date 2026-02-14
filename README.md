# 🥷 NinjaQuant – Injective Strategy Backtesting API

## 🚀 Overview

NinjaQuant is a developer-first backtesting API built on top of Injective's historical market data.

It enables developers to simulate trading strategies and evaluate their historical performance through clean, structured REST endpoints — without building their own backtesting engine.

## 🎯 Problem

Injective provides rich on-chain trading data, but there is no simple API layer that allows developers to:

- Quickly test trading strategies
- Evaluate historical performance
- Compare strategy parameters
- Obtain standardized risk and return metrics

## 💡 Solution

NinjaQuant provides a modular strategy backtesting API that:

- Fetches historical Injective market data (OHLCV)
- Executes predefined trading strategies
- Simulates trade entries and exits
- Computes performance metrics
- Returns structured analytical results

## 🧠 Core Features

### 1️⃣ Strategy Simulation Engine

Currently supported strategies:

- **EMA Crossover Strategy**
- RSI Mean Reversion Strategy (coming soon)

### 2️⃣ Standardized Performance Metrics

For each backtest, the API returns:

- **Win Rate**: Percentage of profitable trades
- **Total Return**: Overall portfolio growth
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted return measure
- **Total Trades**: Number of completed trades

### 3️⃣ Clean REST API Interface

## 📡 API Endpoints

### POST /backtest/ema-crossover

Backtest the EMA Crossover strategy.

**Request Body:**

```json
{
  "market": "INJ/USDT",
  "timeframe": "1h",
  "parameters": {
    "short_period": 9,
    "long_period": 21
  },
  "initial_capital": 1000
}
```

**Response:**

```json
{
  "strategy": "ema_crossover",
  "market": "INJ/USDT",
  "timeframe": "1h",
  "results": {
    "win_rate": 0.62,
    "total_return": 0.18,
    "max_drawdown": 0.07,
    "sharpe_ratio": 1.24,
    "total_trades": 42
  }
}
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

### 2. Run the API

```bash
uvicorn main:app --reload
```

The API will start at `http://localhost:8000`

### 3. View API Documentation

Open your browser and navigate to:

```
http://localhost:8000/docs
```

You'll see the auto-generated Swagger UI with interactive API documentation.

### 4. Test the API

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
