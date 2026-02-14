"""FastAPI route handlers"""
from fastapi import APIRouter, HTTPException
import logging
from ..models.schemas import EMABacktestRequest, EMABacktestResponse, BacktestResults
from ..strategies import EMAStrategy
from ..data import InjectiveDataClient, SyntheticDataClient
from ..core import MetricsCalculator
from ..core.exceptions import (
    InjectiveConnectionError,
    InvalidMarketError,
    InsufficientDataError,
    StrategyExecutionError
)
from config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


# Initialize data client based on configuration
def get_data_client():
    """Factory function to get appropriate data client"""
    if settings.USE_REAL_DATA:
        logger.info("Using InjectiveDataClient for real market data")
        return InjectiveDataClient(network=settings.INJECTIVE_NETWORK)
    else:
        logger.info("Using SyntheticDataClient for demo data")
        return SyntheticDataClient()


@router.get("/")
def root():
    """API root endpoint with information"""
    return {
        "message": "Welcome to NinjaQuant API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "endpoints": [
            "/backtest/ema-crossover"
        ],
        "data_mode": "real" if settings.USE_REAL_DATA else "synthetic"
    }


@router.post("/backtest/ema-crossover", response_model=EMABacktestResponse)
def backtest_ema_crossover(request: EMABacktestRequest):
    """
    Backtest EMA Crossover Strategy
    
    The EMA Crossover strategy uses two exponential moving averages:
    - Short EMA (default: 9) - reacts quickly to price changes
    - Long EMA (default: 21) - reacts slowly
    
    Trading Logic:
    - BUY when Short EMA crosses ABOVE Long EMA (Golden Cross)
    - SELL when Short EMA crosses BELOW Long EMA (Death Cross)
    
    Returns:
        Backtest results with performance metrics:
        - Win Rate: Percentage of profitable trades
        - Total Return: Overall portfolio growth
        - Max Drawdown: Largest peak-to-trough decline
        - Sharpe Ratio: Risk-adjusted return measure
        - Total Trades: Number of completed trades
    
    Raises:
        400: Invalid request parameters
        404: Market not found
        500: Internal server error
        503: Injective connection error
    """
    try:
        logger.info(f"Backtest request: {request.market} {request.timeframe} with params {request.parameters}")
        
        # Step 1: Fetch historical data (NO FALLBACK - Real data only)
        data_client = get_data_client()
        
        df = data_client.fetch_historical_candles(
            market=request.market,
            timeframe=request.timeframe,
            limit=settings.DEFAULT_CANDLE_LIMIT
        )
        logger.info(f"Fetched {len(df)} candles for {request.market}")
        
        # Step 2: Execute strategy
        strategy = EMAStrategy()
        trades = strategy.execute(
            data=df,
            parameters={
                'short_period': request.parameters.short_period,
                'long_period': request.parameters.long_period
            }
        )
        
        logger.info(f"Strategy executed: {len(trades)} trades generated")
        
        # Step 3: Calculate performance metrics
        metrics = MetricsCalculator.calculate(trades, request.initial_capital)
        
        logger.info(f"Metrics calculated: {metrics}")
        
        # Step 4: Return results
        return EMABacktestResponse(
            strategy="ema_crossover",
            market=request.market,
            timeframe=request.timeframe,
            results=BacktestResults(**metrics)
        )
    
    except InvalidMarketError as e:
        logger.error(f"Invalid market: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    
    except InsufficientDataError as e:
        logger.error(f"Insufficient data: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except StrategyExecutionError as e:
        logger.error(f"Strategy execution error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except InjectiveConnectionError as e:
        logger.error(f"Injective connection error: {e}")
        raise HTTPException(status_code=503, detail=f"Failed to connect to Injective network: {str(e)}")
    
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.exception(f"Unexpected error during backtest: {e}")
        raise HTTPException(status_code=500, detail="Internal server error occurred")
