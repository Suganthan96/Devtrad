# 🥷 NinjaQuant - Quick Start Guide

## ✅ What's Been Built

You now have a **production-ready backtesting API** with:

- ✅ **Modular architecture** (strategies, data layer, API routes separated)
- ✅ **Real Injective integration** via REST API (switchable to synthetic data)
- ✅ FastAPI backend with auto-generated Swagger documentation
- ✅ EMA Crossover strategy with extensible Strategy base class
- ✅ Performance metrics calculation (Win Rate, Total Return, Max Drawdown, Sharpe Ratio)
- ✅ Comprehensive error handling and input validation
- ✅ Configuration management with environment variables
- ✅ Structured logging
- ✅ Working test scripts

## 🚀 Running the API

### 1. Install Dependencies

First, ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### 2. Configure Data Source

The API can use **real Injective data** or **synthetic data** for testing.

#### Option A: Use Real Injective Data (Default)

```bash
set USE_REAL_DATA=true
set INJECTIVE_NETWORK=mainnet
```

#### Option B: Use Synthetic Data (For Demo/Testing)

```bash
set USE_REAL_DATA=false
```

### 3. Start the Server

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

**Note:** The new modular architecture is located in the `app/` directory.

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
├── app/                     # Application code
│   ├── main.py             # FastAPI application entry point
│   ├── api/                # API route handlers
│   ├── strategies/         # Trading strategies (base + EMA)
│   ├── data/               # Data clients (Injective + synthetic)
│   ├── core/               # Business logic (metrics + exceptions)
│   └── models/             # Pydantic schemas
├── config.py               # Configuration settings
├── test_api.py             # Comprehensive test suite
├── requirements.txt        # Python dependencies
├── README.md              # Full project documentation
├── QUICKSTART.md          # This file
└── IMPLEMENTATION.md      # Implementation summary
```

## 🔧 How It Works

### 1. Data Layer (`app/data/`)
- **InjectiveDataClient**: Fetches real historical OHLCV data from Injective network
  - Connects to Injective REST API
  - Maps market symbols to Injective market IDs
  - Handles network errors and retries
- **SyntheticDataClient**: Generates realistic synthetic data for testing
  - Configurable via `USE_REAL_DATA` environment variable

### 2. Strategy Engine (`app/strategies/`)
- **Strategy Base Class**: Abstract interface for all strategies
  - `execute()`: Run strategy on historical data
  - `validate_parameters()`: Input validation
  - `get_required_indicators()`: Declare dependencies
- **EMAStrategy**: EMA Crossover implementation
  - Calculates Short EMA (default: 9) and Long EMA (default: 21)
  - Detects crossover signals:
    - **Buy**: Short EMA crosses ABOVE Long EMA (Golden Cross)
    - **Sell**: Short EMA crosses BELOW Long EMA (Death Cross)

### 3. Trade Simulation
- Tracks position state (open/closed)
- Records entry and exit prices
- Calculates trade returns
- Returns list of completed trades

### 4. Metrics Calculation (`app/core/metrics.py`)
- **MetricsCalculator**: Computes performance indicators
  - Win Rate: Percentage of profitable trades
  - Total Return: Compounded portfolio growth
  - Max Drawdown: Peak-to-trough equity decline
  - Sharpe Ratio: Risk-adjusted return
  - Total Trades: Number of completed trades

### 5. API Layer (`app/api/routes.py`)
- FasStrategy base class allows easy addition of new strategies (RSI, MACD, etc.)
   - Modular design with clear separation of concerns
   - Dependency injection for testability
   - Configurable data sources (real Injective vs synthetic)

4. **Injective Integration**
   - Built on Injective's market data via REST API

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
## 🏗️ Architecture Benefits

### Modularity
The new architecture separates concerns into distinct modules:
- **Strategies**: Easy to add new trading strategies by extending `Strategy` base class
- **Data Layer**: Pluggable data sources (Injective, synthetic, or future: CSV, databases)
- **Metrics**: Reusable performance calculation logic
- **API**: Clean route handlers with dependency injection

### Extensibility
Adding a new strategy (e.g., RSI) is straightforward:
1. Create new class inheriting from `Strategy`
2. Implement required methods (`execute`, `validate_parameters`)
3. Add route handler in `app/api/routes.py`
4. No changes needed to existing code

### Testability
- Mock `InjectiveDataClient` for unit tests
- Use `SyntheticDataClient` for integration tests
- Strategies can be tested independently of API layer

### Production-Ready
- **Input Validation**: Pydantic models validate all inputs
- **Error Handling**: Custom exceptions with meaningful HTTP status codes
- **Logging**: Structured logging for debugging and monitoring
- **Configuration**: Environment-based configuration for different deployments
## 🚀 Next Steps

### Already Implemented ✅

1. **Real Injective Data Integration** ✅
   - Connected to Injective's REST API
   - Support for multiple markets via market discovery
   - Error handling and fallback mechanisms
   - Configurable via environment variables

2. **Modular Architecture** ✅
   - Strategy base class for extensibility
   - Separated data layer, strategy engine, and API routes
   - Comprehensive error handling
   - Input validation via Pydantic

### For Future Enhancement

1. **Add More Strategies**
   - RSI Mean Reversion
   - MACD Crossover
   - Bollinger Bands
   - Custom strategy builder

2. **Enhanced Metrics**
   - Annualized returns
   - Sortino ratio
   - Calmar ratio
   - Trade distribution analysis

3. **Optimization Features**
   - Parameter optimization endpoints
   - Walk-forward analysis
   - Monte Carlo simulation
   - Multi-market comparison

4. **Infrastructure**
   - Database persistence for backtest history
   - Rate limiting and authentication
   - Caching layer for market data
   - WebSocket support for real-time updates

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
