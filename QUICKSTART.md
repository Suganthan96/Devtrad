# 🥷 NinjaQuant - Quick Start Guide

## ✅ What's Been Built

You now have a **fully functional EMA Crossover backtesting API** with:

- ✅ FastAPI backend with auto-generated Swagger documentation
- ✅ EMA Crossover strategy implementation
- ✅ Performance metrics calculation (Win Rate, Total Return, Max Drawdown, Sharpe Ratio)
- ✅ Clean REST API interface
- ✅ Working test scripts

## 🚀 Running the API

### 1. Start the Server

```bash
python -m uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

### 2. View API Documentation

Open your browser and go to:

```
http://localhost:8000/docs
```

You'll see the **interactive Swagger UI** where you can:
- View all endpoints
- See request/response schemas
- Test the API directly from the browser

## 📡 API Usage Examples

### Using curl

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

### Using Python

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

### Using the Demo Script

```bash
python demo.py
```

## 📊 Example Response

```json
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
```

## 🧠 Understanding the Results

### Win Rate (0.3333 = 33.33%)
- Percentage of profitable trades
- 33.33% means 5 out of 15 trades were profitable

### Total Return (-0.0392 = -3.92%)
- Overall portfolio performance
- Started with $1000, ended with $960.80
- Negative return means the strategy lost money on this data

### Max Drawdown (0.1662 = 16.62%)
- Largest peak-to-trough decline
- At worst, portfolio was down 16.62% from its peak

### Sharpe Ratio (-0.0123)
- Risk-adjusted return measure
- Negative value indicates poor risk-adjusted performance
- Higher is better (typically > 1.0 is good)

### Total Trades (15)
- Number of completed buy-sell cycles
- More trades = more data points for statistical significance

## 🎯 Testing Different Parameters

### Faster EMA (More Trades)

```json
{
  "market": "INJ/USDT",
  "timeframe": "1h",
  "parameters": {
    "short_period": 5,
    "long_period": 13
  },
  "initial_capital": 1000
}
```

### Slower EMA (Fewer Trades, Longer Trends)

```json
{
  "market": "INJ/USDT",
  "timeframe": "4h",
  "parameters": {
    "short_period": 12,
    "long_period": 26
  },
  "initial_capital": 1000
}
```

### Higher Capital

```json
{
  "market": "INJ/USDT",
  "timeframe": "1h",
  "parameters": {
    "short_period": 9,
    "long_period": 21
  },
  "initial_capital": 10000
}
```

## 📁 Project Structure

```
Devtrad/
├── main.py              # FastAPI application with all logic
├── requirements.txt     # Python dependencies
├── README.md           # Full project documentation
├── QUICKSTART.md       # This file
├── demo.py             # Simple demo script
└── test_api.py         # Comprehensive test suite
```

## 🔧 How It Works

### 1. Data Layer
- Fetches historical OHLCV data (currently synthetic for demo)
- In production: integrate with Injective's historical data API

### 2. Strategy Engine
- Calculates Short EMA (9-period) and Long EMA (21-period)
- Detects crossover signals:
  - **Buy**: Short EMA crosses ABOVE Long EMA (Golden Cross)
  - **Sell**: Short EMA crosses BELOW Long EMA (Death Cross)

### 3. Trade Simulation
- Tracks position state (open/closed)
- Records entry and exit prices
- Calculates trade returns

### 4. Metrics Calculation
- Computes performance indicators
- Returns structured JSON response

## 🎨 For Hackathon Judges

### Key Highlights

1. **Developer-First Design**
   - Clean REST API
   - Auto-generated documentation
   - Standardized response format

2. **Quantitative Layer**
   - Not just raw data exposure
   - Computational intelligence layer
   - Industry-standard metrics

3. **Extensible Architecture**
   - Easy to add new strategies (RSI, MACD, Bollinger Bands)
   - Modular design
   - Separation of concerns

4. **Injective Integration**
   - Built on Injective's market data
   - Adds value to Injective ecosystem
   - Enables developer tooling

## 🚀 Next Steps

### For Production

1. **Integrate Real Injective Data**
   - Connect to Injective's historical data API
   - Support multiple markets
   - Real-time data updates

2. **Add More Strategies**
   - RSI Mean Reversion
   - MACD Crossover
   - Bollinger Bands
   - Custom strategy builder

3. **Enhanced Metrics**
   - Annualized returns
   - Sortino ratio
   - Calmar ratio
   - Trade distribution analysis

4. **Optimization Features**
   - Parameter optimization
   - Walk-forward analysis
   - Monte Carlo simulation

### For Demo

1. **Show Swagger UI** (`/docs`)
   - Interactive documentation
   - Try it out feature
   - Schema visualization

2. **Run Different Parameters**
   - Show how results change
   - Demonstrate flexibility
   - Compare strategies

3. **Explain the Value**
   - Saves development time
   - Standardized metrics
   - Reusable infrastructure

## 💡 Demo Script

```bash
# Terminal 1: Start the API
python -m uvicorn main:app --reload

# Terminal 2: Run the demo
python demo.py

# Browser: View documentation
# Open http://localhost:8000/docs
```

## 🏆 Why This Matters

**Most APIs expose raw data.**

**NinjaQuant exposes evaluated trading intelligence.**

It transforms Injective's market data into actionable insights through:
- Strategy simulation
- Performance evaluation
- Risk analysis
- Standardized metrics

This is a **computational abstraction layer** that enables:
- Faster bot development
- Quantitative research
- Strategy comparison
- Analytics platforms

---

**Built with ❤️ for the Injective ecosystem**
