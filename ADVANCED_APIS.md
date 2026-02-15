# 🚀 Advanced APIs Documentation

## Overview

NinjaQuant includes three **professional-grade** advanced APIs that demonstrate quantitative analysis capabilities beyond basic backtesting.

These APIs showcase:
- ✅ Multi-strategy parameter optimization
- ✅ Market intelligence and regime classification
- ✅ Professional risk management metrics

---

## 🥇 API #1: Strategy Comparison

**Endpoint:** `POST /compare`

### Purpose

Compare multiple strategy configurations in a single request to optimize parameters and find the best performing setup.

### Use Cases

- **Parameter Optimization**: Test EMA(9,21) vs EMA(12,26) vs EMA(20,50)
- **Strategy Selection**: Compare EMA vs RSI vs other strategies
- **Performance Benchmarking**: Find which configuration works best for a given market

### Request Body

```json
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

### Response

```json
{
  "market": "BTC/USDT PERP",
  "timeframe": "1h",
  "comparison": [
    {
      "strategy_name": "ema_9_21",
      "win_rate": 0.62,
      "total_return": 0.18,
      "sharpe_ratio": 1.24,
      "max_drawdown": 0.08,
      "total_trades": 15
    },
    {
      "strategy_name": "ema_12_26",
      "win_rate": 0.55,
      "total_return": 0.12,
      "sharpe_ratio": 1.05,
      "max_drawdown": 0.06,
      "total_trades": 12
    },
    {
      "strategy_name": "rsi_14_30_70",
      "win_rate": 0.70,
      "total_return": 0.15,
      "sharpe_ratio": 1.15,
      "max_drawdown": 0.05,
      "total_trades": 10
    }
  ],
  "best_strategy": "ema_9_21"
}
```

### cURL Example

```bash
curl -X POST http://localhost:8000/compare \
  -H "Content-Type: application/json" \
  -d '{
    "market": "BTC/USDT PERP",
    "timeframe": "1h",
    "strategies": [
      {
        "strategy": "ema_crossover",
        "parameters": {"short_period": 9, "long_period": 21}
      }
    ],
    "initial_capital": 10000
  }'
```

---

## 🌡️ API #2: Market Regime Analysis

**Endpoint:** `GET /market-regime`

### Purpose

Analyze and classify current market conditions to help select appropriate trading strategies.

**This is market intelligence, not strategy testing.**

### Market Regimes

| Regime | Description | Recommended Strategy |
|--------|-------------|---------------------|
| **Trending** | Strong directional movement (high trend strength) | EMA Crossover (trend-following) |
| **Ranging** | Price oscillates within bounds (low trend strength) | RSI Mean Reversion |
| **Volatile** | High volatility regardless of trend | Reduce position sizes, use stops |

### Request Parameters

```
market: str - Trading pair (e.g., "BTC/USDT PERP")
timeframe: str - Analysis timeframe (default: "1h")
```

### Response

```json
{
  "market": "BTC/USDT PERP",
  "timeframe": "1h",
  "regime": "Trending",
  "trend_strength": 0.68,
  "volatility_level": "High",
  "volatility_value": 1.25,
  "price_change_pct": 0.15
}
```

### Response Fields

- **regime**: Market classification (Trending/Ranging/Volatile)
- **trend_strength**: 0-1 scale (higher = stronger trend)
- **volatility_level**: Low/Medium/High classification
- **volatility_value**: Actual volatility (annualized)
- **price_change_pct**: Price change over analysis period

### cURL Example

```bash
curl -X GET "http://localhost:8000/market-regime?market=BTC/USDT PERP&timeframe=1h"
```

### Usage Strategy

```python
# Example: Select strategy based on market regime
response = requests.get('http://localhost:8000/market-regime', 
                       params={'market': 'BTC/USDT PERP', 'timeframe': '1h'})
regime_data = response.json()

if regime_data['regime'] == 'Trending':
    # Use EMA Crossover
    strategy = 'ema_crossover'
elif regime_data['regime'] == 'Ranging':
    # Use RSI Mean Reversion
    strategy = 'rsi_mean_reversion'
else:
    # High volatility - reduce position size
    position_size = 0.05  # 5% instead of 10%
```

---

## 📊 API #3: Risk Analysis

**Endpoint:** `POST /risk-analysis`

### Purpose

Analyze risk characteristics of a trading strategy with professional-grade risk metrics.

**Unlike `/backtest` (which focuses on profit), this focuses on RISK.**

### Risk Metrics Explained

| Metric | Description | Good Value |
|--------|-------------|-----------|
| **Return Volatility** | How consistent are returns? | < 0.08 |
| **Max Consecutive Losses** | Longest losing streak | < 3 |
| **Largest Loss** | Worst single trade | > -0.08 |
| **Average Loss** | Typical losing trade | > -0.05 |
| **Value at Risk (95%)** | Max expected loss at 95% confidence | > -0.10 |
| **Risk Level** | Overall classification | Low preferred |

### Request Body

```json
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

### Response

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

### Risk Level Classification

```
Risk Level = Low    → Risk Score ≤ 2 (Safe to use)
Risk Level = Medium → Risk Score 3-4 (Use with caution)
Risk Level = High   → Risk Score ≥ 5 (Dangerous!)

Risk Score Components:
- High volatility (> 0.15): +2 points
- Many consecutive losses (> 5): +2 points  
- Large single loss (< -0.15): +2 points
```

### cURL Example

```bash
curl -X POST http://localhost:8000/risk-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "market": "ETH/USDT PERP",
    "timeframe": "1h",
    "strategy": "rsi_mean_reversion",
    "parameters": {
      "period": 14,
      "oversold": 30,
      "overbought": 70
    },
    "initial_capital": 10000
  }'
```

### Usage Strategy

```python
# Example: Risk-adjusted position sizing
response = requests.post('http://localhost:8000/risk-analysis', json=request_body)
risk_data = response.json()

risk_level = risk_data['risk_metrics']['risk_level']

# Adjust position size based on risk
if risk_level == 'Low':
    position_size = 0.10  # 10% of capital
elif risk_level == 'Medium':
    position_size = 0.05  # 5% of capital
else:  # High
    position_size = 0.02  # 2% of capital - or skip entirely
```

---

## 🎯 Why These APIs Matter

### For Hackathon Judges

These APIs demonstrate:

1. **Professional Quant Thinking**: Not just backtesting, but optimization, market intelligence, and risk management
2. **Production-Ready Architecture**: Modular design with separate analysis modules
3. **Advanced Metrics**: VaR, regime classification, multi-strategy comparison
4. **Real-World Applicability**: These are features actual trading firms use

### For Developers

These APIs provide:

1. **Parameter Optimization**: Test 10 configurations in one request
2. **Strategy Selection**: Automatically choose strategy based on market regime
3. **Risk Management**: Understand danger zones before deploying capital
4. **Professional Reports**: Metrics that matter to real traders

---

## 🚀 Complete Workflow Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Step 1: Analyze market regime
regime = requests.get(f"{BASE_URL}/market-regime", 
                     params={"market": "BTC/USDT PERP", "timeframe": "1h"})
regime_data = regime.json()

print(f"Market Regime: {regime_data['regime']}")

# Step 2: Compare strategies for this regime
if regime_data['regime'] == 'Trending':
    # Test different EMA configurations
    comparison = requests.post(f"{BASE_URL}/compare", json={
        "market": "BTC/USDT PERP",
        "timeframe": "1h",
        "strategies": [
            {"strategy": "ema_crossover", "parameters": {"short_period": 9, "long_period": 21}},
            {"strategy": "ema_crossover", "parameters": {"short_period": 12, "long_period": 26}},
            {"strategy": "ema_crossover", "parameters": {"short_period": 20, "long_period": 50}}
        ],
        "initial_capital": 10000
    })
    
    best = comparison.json()['best_strategy']
    print(f"Best Strategy: {best}")

# Step 3: Analyze risk of best strategy
risk = requests.post(f"{BASE_URL}/risk-analysis", json={
    "market": "BTC/USDT PERP",
    "timeframe": "1h",
    "strategy": "ema_crossover",
    "parameters": {"short_period": 9, "long_period": 21},
    "initial_capital": 10000
})

risk_data = risk.json()
print(f"Risk Level: {risk_data['risk_metrics']['risk_level']}")

# Step 4: Make trading decision
if risk_data['risk_metrics']['risk_level'] == 'Low':
    print("✅ Safe to trade with this strategy!")
else:
    print("⚠️ High risk - reduce position size or skip")
```

---

## 📝 Testing

Run the comprehensive demo:

```bash
python demo_advanced_apis.py
```

This will test all three APIs and show:
- ✅ Strategy comparison with 3 configs
- ✅ Market regime for BTC, ETH, INJ
- ✅ Risk analysis for RSI strategy

---

## 🎓 Key Takeaways

1. **Strategy Comparison** (`/compare`): Helps you find the best parameters
2. **Market Regime** (`/market-regime`): Helps you choose the right strategy
3. **Risk Analysis** (`/risk-analysis`): Helps you understand the danger zones

**Together, these APIs provide a complete quantitative trading workflow.**

This is what separates a demo project from a **production-ready platform**. 🚀
