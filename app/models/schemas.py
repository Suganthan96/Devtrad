"""Pydantic schemas for API requests and responses"""
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Optional


class EMAParameters(BaseModel):
    """Parameters for EMA Crossover Strategy"""
    short_period: int = Field(default=9, gt=0, description="Short EMA period (must be positive)")
    long_period: int = Field(default=21, gt=0, description="Long EMA period (must be positive)")
    
    @field_validator('long_period')
    @classmethod
    def validate_periods(cls, v, info):
        """Ensure long period is greater than short period"""
        if 'short_period' in info.data and v <= info.data['short_period']:
            raise ValueError('long_period must be greater than short_period')
        return v


class EMABacktestRequest(BaseModel):
    """Request body for EMA Crossover backtest"""
    market: str = Field(..., pattern=r'^[A-Z]+/[A-Z]+$', description="Market pair (e.g., INJ/USDT)")
    timeframe: str = Field(..., pattern=r'^(1m|5m|15m|1h|4h|1d)$', description="Candle timeframe")
    parameters: EMAParameters
    initial_capital: float = Field(default=1000.0, gt=0, description="Starting capital (must be positive)")


class BacktestResults(BaseModel):
    """Performance metrics from backtest"""
    win_rate: float = Field(..., ge=0, le=1, description="Percentage of winning trades")
    total_return: float = Field(..., description="Total portfolio return")
    max_drawdown: float = Field(..., ge=0, le=1, description="Maximum drawdown percentage")
    sharpe_ratio: float = Field(..., description="Risk-adjusted return metric")
    total_trades: int = Field(..., ge=0, description="Number of completed trades")


class EMABacktestResponse(BaseModel):
    """Response from EMA Crossover backtest"""
    strategy: str
    market: str
    timeframe: str
    results: BacktestResults


class Trade(BaseModel):
    """Individual trade record"""
    entry_price: float
    exit_price: float
    return_pct: float
    entry_index: int
    exit_index: int
