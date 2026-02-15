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
    market: str = Field(..., pattern=r'^[A-Z]+/[A-Z]+(\s+[A-Z]+)?$', description="Market pair (e.g., INJ/USDT, INJ/USDT PERP)")
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


class RSIParameters(BaseModel):
    """Parameters for RSI Mean Reversion Strategy"""
    period: int = Field(default=14, gt=0, description="RSI calculation period (must be positive)")
    oversold: float = Field(default=30, gt=0, lt=100, description="RSI oversold threshold (0-100)")
    overbought: float = Field(default=70, gt=0, lt=100, description="RSI overbought threshold (0-100)")
    
    @field_validator('overbought')
    @classmethod
    def validate_thresholds(cls, v, info):
        """Ensure overbought is greater than oversold"""
        if 'oversold' in info.data and v <= info.data['oversold']:
            raise ValueError('overbought must be greater than oversold')
        return v


class RSIBacktestRequest(BaseModel):
    """Request body for RSI Mean Reversion backtest"""
    market: str = Field(..., pattern=r'^[A-Z]+/[A-Z]+(\s+[A-Z]+)?$', description="Market pair (e.g., INJ/USDT, INJ/USDT PERP)")
    timeframe: str = Field(..., pattern=r'^(1m|5m|15m|1h|4h|1d)$', description="Candle timeframe")
    parameters: RSIParameters
    initial_capital: float = Field(default=1000.0, gt=0, description="Starting capital (must be positive)")


class RSIBacktestResponse(BaseModel):
    """Response from RSI Mean Reversion backtest"""
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


# ============================================================
# Strategy Comparison API Schemas
# ============================================================

class StrategyConfig(BaseModel):
    """Individual strategy configuration for comparison"""
    strategy: str = Field(..., pattern=r'^(ema_crossover|rsi_mean_reversion)$', description="Strategy type")
    parameters: Dict = Field(..., description="Strategy parameters")


class ComparisonRequest(BaseModel):
    """Request body for strategy comparison"""
    market: str = Field(..., pattern=r'^[A-Z]+/[A-Z]+(\s+[A-Z]+)?$', description="Market pair")
    timeframe: str = Field(..., pattern=r'^(1m|5m|15m|1h|4h|1d)$', description="Candle timeframe")
    strategies: list[StrategyConfig] = Field(..., min_length=2, max_length=10, description="List of strategies to compare (2-10)")
    initial_capital: float = Field(default=1000.0, gt=0, description="Starting capital")


class StrategyComparisonResult(BaseModel):
    """Result for a single strategy in comparison"""
    strategy_name: str
    win_rate: float
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    total_trades: int


class ComparisonResponse(BaseModel):
    """Response from strategy comparison"""
    market: str
    timeframe: str
    comparison: list[StrategyComparisonResult]
    best_strategy: str = Field(..., description="Name of best performing strategy by total return")


# ============================================================
# Market Regime Analysis API Schemas
# ============================================================

class MarketRegimeResponse(BaseModel):
    """Response from market regime analysis"""
    market: str
    timeframe: str
    regime: str = Field(..., pattern=r'^(Trending|Ranging|Volatile)$', description="Market regime classification")
    trend_strength: float = Field(..., ge=0, le=1, description="Trend strength (0-1)")
    volatility_level: str = Field(..., pattern=r'^(Low|Medium|High)$', description="Volatility classification")
    volatility_value: float = Field(..., ge=0, description="Actual volatility percentage")
    price_change_pct: float = Field(..., description="Price change over period")


# ============================================================
# Risk Analysis API Schemas
# ============================================================

class RiskAnalysisRequest(BaseModel):
    """Request body for risk analysis"""
    market: str = Field(..., pattern=r'^[A-Z]+/[A-Z]+(\s+[A-Z]+)?$', description="Market pair")
    timeframe: str = Field(..., pattern=r'^(1m|5m|15m|1h|4h|1d)$', description="Candle timeframe")
    strategy: str = Field(..., pattern=r'^(ema_crossover|rsi_mean_reversion)$', description="Strategy type")
    parameters: Dict = Field(..., description="Strategy parameters")
    initial_capital: float = Field(default=1000.0, gt=0, description="Starting capital")


class RiskMetrics(BaseModel):
    """Risk metrics from strategy analysis"""
    return_volatility: float = Field(..., ge=0, description="Volatility of returns")
    max_consecutive_losses: int = Field(..., ge=0, description="Maximum consecutive losing trades")
    largest_loss: float = Field(..., le=0, description="Largest single trade loss")
    avg_loss: float = Field(..., le=0, description="Average losing trade")
    risk_level: str = Field(..., pattern=r'^(Low|Medium|High)$', description="Overall risk classification")
    value_at_risk_95: float = Field(..., description="95% Value at Risk")


class RiskAnalysisResponse(BaseModel):
    """Response from risk analysis"""
    strategy: str
    market: str
    timeframe: str
    risk_metrics: RiskMetrics
    performance_summary: BacktestResults
