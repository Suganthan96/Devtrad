from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import pandas as pd
import numpy as np
from datetime import datetime

app = FastAPI(
    title="NinjaQuant API",
    description="Developer-first backtesting API built on Injective's historical market data",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Models
class EMAParameters(BaseModel):
    short_period: int = 9
    long_period: int = 21


class EMABacktestRequest(BaseModel):
    market: str
    timeframe: str
    parameters: EMAParameters
    initial_capital: float = 1000.0


# Response Models
class BacktestResults(BaseModel):
    win_rate: float
    total_return: float
    max_drawdown: float
    sharpe_ratio: float
    total_trades: int


class EMABacktestResponse(BaseModel):
    strategy: str
    market: str
    timeframe: str
    results: BacktestResults


@app.get("/")
def root():
    return {
        "message": "Welcome to NinjaQuant API",
        "docs": "/docs",
        "endpoints": [
            "/backtest/ema-crossover"
        ]
    }


@app.post("/backtest/ema-crossover", response_model=EMABacktestResponse)
def backtest_ema_crossover(request: EMABacktestRequest):
    """
    Backtest EMA Crossover Strategy
    
    The EMA Crossover strategy uses two exponential moving averages:
    - Short EMA (default: 9) - reacts quickly to price changes
    - Long EMA (default: 21) - reacts slowly
    
    Trading Logic:
    - BUY when Short EMA crosses ABOVE Long EMA (Golden Cross)
    - SELL when Short EMA crosses BELOW Long EMA (Death Cross)
    """
    try:
        # Step 1: Fetch historical data
        df = fetch_market_data(request.market, request.timeframe)
        
        # Step 2: Calculate EMAs
        df = calculate_ema(df, request.parameters.short_period, request.parameters.long_period)
        
        # Step 3: Detect crossovers and simulate trades
        trades = simulate_ema_trades(df, request.initial_capital)
        
        # Step 4: Calculate performance metrics
        metrics = calculate_metrics(trades, request.initial_capital)
        
        return EMABacktestResponse(
            strategy="ema_crossover",
            market=request.market,
            timeframe=request.timeframe,
            results=BacktestResults(**metrics)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def fetch_market_data(market: str, timeframe: str) -> pd.DataFrame:
    """
    Fetch historical OHLCV data from Injective
    
    For MVP/demo purposes, this generates synthetic data.
    In production, this would call Injective's historical data API.
    """
    # Generate synthetic data for demo
    # In production: integrate with Injective API
    np.random.seed(42)
    
    num_candles = 500
    base_price = 10.0
    
    # Generate realistic price movement
    returns = np.random.randn(num_candles) * 0.02  # 2% volatility
    prices = base_price * np.exp(np.cumsum(returns))
    
    df = pd.DataFrame({
        'timestamp': pd.date_range(start='2024-01-01', periods=num_candles, freq='1h'),
        'close': prices
    })
    
    return df


def calculate_ema(df: pd.DataFrame, short_period: int, long_period: int) -> pd.DataFrame:
    """
    Calculate Exponential Moving Averages
    
    EMA formula: EMA = (CurrentPrice × k) + (PreviousEMA × (1-k))
    where k = 2/(period+1)
    
    Using pandas ewm() for efficient calculation.
    """
    df['ema_short'] = df['close'].ewm(span=short_period, adjust=False).mean()
    df['ema_long'] = df['close'].ewm(span=long_period, adjust=False).mean()
    
    return df


def simulate_ema_trades(df: pd.DataFrame, initial_capital: float) -> list:
    """
    Simulate trades based on EMA crossover signals
    
    Buy Signal (Golden Cross):
    - Short EMA crosses ABOVE Long EMA
    
    Sell Signal (Death Cross):
    - Short EMA crosses BELOW Long EMA
    """
    trades = []
    position_open = False
    entry_price = 0
    entry_index = 0
    
    for i in range(1, len(df)):
        current_short = df['ema_short'].iloc[i]
        current_long = df['ema_long'].iloc[i]
        prev_short = df['ema_short'].iloc[i-1]
        prev_long = df['ema_long'].iloc[i-1]
        current_price = df['close'].iloc[i]
        
        # Buy Signal: Golden Cross
        if not position_open and current_short > current_long and prev_short <= prev_long:
            position_open = True
            entry_price = current_price
            entry_index = i
        
        # Sell Signal: Death Cross
        elif position_open and current_short < current_long and prev_short >= prev_long:
            exit_price = current_price
            trade_return = (exit_price - entry_price) / entry_price
            
            trades.append({
                'entry_price': entry_price,
                'exit_price': exit_price,
                'return': trade_return,
                'entry_index': entry_index,
                'exit_index': i
            })
            
            position_open = False
    
    return trades


def calculate_metrics(trades: list, initial_capital: float) -> Dict:
    """
    Calculate performance metrics from trade results
    
    Metrics:
    1. Win Rate: percentage of profitable trades
    2. Total Return: overall portfolio growth
    3. Max Drawdown: largest peak-to-trough decline
    4. Sharpe Ratio: risk-adjusted return
    5. Total Trades: number of completed trades
    """
    if len(trades) == 0:
        return {
            'win_rate': 0.0,
            'total_return': 0.0,
            'max_drawdown': 0.0,
            'sharpe_ratio': 0.0,
            'total_trades': 0
        }
    
    # 1. Win Rate
    winning_trades = sum(1 for trade in trades if trade['return'] > 0)
    win_rate = winning_trades / len(trades) if len(trades) > 0 else 0
    
    # 2. Total Return (compounded)
    capital = initial_capital
    equity_curve = [capital]
    
    for trade in trades:
        capital *= (1 + trade['return'])
        equity_curve.append(capital)
    
    total_return = (capital - initial_capital) / initial_capital
    
    # 3. Max Drawdown
    peak = equity_curve[0]
    max_drawdown = 0
    
    for value in equity_curve:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    # 4. Sharpe Ratio
    returns = [trade['return'] for trade in trades]
    if len(returns) > 1 and np.std(returns) > 0:
        sharpe_ratio = np.mean(returns) / np.std(returns)
    else:
        sharpe_ratio = 0.0
    
    return {
        'win_rate': round(win_rate, 4),
        'total_return': round(total_return, 4),
        'max_drawdown': round(max_drawdown, 4),
        'sharpe_ratio': round(sharpe_ratio, 4),
        'total_trades': len(trades)
    }
