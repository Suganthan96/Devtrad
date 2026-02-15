"""FastAPI route handlers"""
from fastapi import APIRouter, HTTPException
import logging
from ..models.schemas import (
    EMABacktestRequest, EMABacktestResponse,
    RSIBacktestRequest, RSIBacktestResponse,
    BacktestResults,
    ComparisonRequest, ComparisonResponse, StrategyComparisonResult,
    MarketRegimeResponse,
    RiskAnalysisRequest, RiskAnalysisResponse, RiskMetrics
)
from ..strategies import EMAStrategy, RSIStrategy
from ..data import InjectiveDataClient, SyntheticDataClient
from ..core import MetricsCalculator
from ..analysis import MarketRegimeAnalyzer, RiskAnalyzer
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
        "endpoints": {
            "backtest": [
                "/backtest/ema-crossover",
                "/backtest/rsi-mean-reversion"
            ],
            "advanced": [
                "/compare",
                "/market-regime",
                "/risk-analysis"
            ]
        },
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


@router.post("/backtest/rsi-mean-reversion", response_model=RSIBacktestResponse)
def backtest_rsi_mean_reversion(request: RSIBacktestRequest):
    """
    Backtest RSI Mean Reversion Strategy
    
    The RSI Mean Reversion strategy uses the Relative Strength Index:
    - RSI calculates the magnitude of recent price changes
    - RSI ranges from 0 to 100
    
    Trading Logic:
    - BUY when RSI crosses BELOW oversold level (default: 30) - expecting bounce
    - SELL when RSI crosses ABOVE overbought level (default: 70) - take profit
    
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
        logger.info(f"RSI Backtest request: {request.market} {request.timeframe} with params {request.parameters}")
        
        # Step 1: Fetch historical data
        data_client = get_data_client()
        
        df = data_client.fetch_historical_candles(
            market=request.market,
            timeframe=request.timeframe,
            limit=settings.DEFAULT_CANDLE_LIMIT
        )
        logger.info(f"Fetched {len(df)} candles for {request.market}")
        
        # Step 2: Execute RSI strategy
        strategy = RSIStrategy()
        trades = strategy.execute(
            data=df,
            parameters={
                'period': request.parameters.period,
                'oversold': request.parameters.oversold,
                'overbought': request.parameters.overbought
            }
        )
        
        logger.info(f"RSI Strategy executed: {len(trades)} trades generated")
        
        # Step 3: Calculate performance metrics
        metrics = MetricsCalculator.calculate(trades, request.initial_capital)
        
        logger.info(f"Metrics calculated: {metrics}")
        
        # Step 4: Return results
        return RSIBacktestResponse(
            strategy="rsi_mean_reversion",
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
        logger.exception(f"Unexpected error during RSI backtest: {e}")
        raise HTTPException(status_code=500, detail="Internal server error occurred")


# ============================================================
# ADVANCED APIS
# ============================================================

@router.post("/compare", response_model=ComparisonResponse)
def compare_strategies(request: ComparisonRequest):
    """
    Compare Multiple Strategy Configurations
    
    This endpoint allows you to test multiple strategy configurations
    in a single request and compare their performance side-by-side.
    
    Perfect for:
    - Parameter optimization
    - Strategy selection
    - Performance benchmarking
    
    Example:
        Compare EMA(9,21) vs EMA(12,26) vs RSI(14,30,70)
    
    Returns:
        Comparison results with best performing strategy highlighted
    
    Raises:
        400: Invalid request parameters
        404: Market not found
        500: Internal server error
    """
    try:
        logger.info(f"Strategy comparison request: {request.market} with {len(request.strategies)} strategies")
        
        # Fetch market data once (shared by all strategies)
        data_client = get_data_client()
        df = data_client.fetch_historical_candles(
            market=request.market,
            timeframe=request.timeframe,
            limit=settings.DEFAULT_CANDLE_LIMIT
        )
        
        logger.info(f"Fetched {len(df)} candles for comparison")
        
        # Run each strategy
        comparison_results = []
        
        for i, strategy_config in enumerate(request.strategies):
            try:
                # Select strategy
                if strategy_config.strategy == "ema_crossover":
                    strategy = EMAStrategy()
                    strategy_name = f"ema_{strategy_config.parameters.get('short_period')}_{strategy_config.parameters.get('long_period')}"
                elif strategy_config.strategy == "rsi_mean_reversion":
                    strategy = RSIStrategy()
                    strategy_name = f"rsi_{strategy_config.parameters.get('period')}_{strategy_config.parameters.get('oversold')}_{strategy_config.parameters.get('overbought')}"
                else:
                    logger.warning(f"Unknown strategy: {strategy_config.strategy}")
                    continue
                
                # Execute strategy
                trades = strategy.execute(data=df, parameters=strategy_config.parameters)
                
                # Calculate metrics
                metrics = MetricsCalculator.calculate(trades, request.initial_capital)
                
                # Add to comparison
                comparison_results.append(
                    StrategyComparisonResult(
                        strategy_name=strategy_name,
                        win_rate=metrics['win_rate'],
                        total_return=metrics['total_return'],
                        sharpe_ratio=metrics['sharpe_ratio'],
                        max_drawdown=metrics['max_drawdown'],
                        total_trades=metrics['total_trades']
                    )
                )
                
                logger.info(f"Strategy {i+1}/{len(request.strategies)}: {strategy_name} - Return: {metrics['total_return']:.2%}")
                
            except Exception as e:
                logger.error(f"Error executing strategy {i+1}: {e}")
                continue
        
        if not comparison_results:
            raise HTTPException(status_code=400, detail="No strategies could be executed successfully")
        
        # Find best strategy (by total return)
        best_strategy = max(comparison_results, key=lambda x: x.total_return)
        
        logger.info(f"Comparison complete. Best strategy: {best_strategy.strategy_name}")
        
        return ComparisonResponse(
            market=request.market,
            timeframe=request.timeframe,
            comparison=comparison_results,
            best_strategy=best_strategy.strategy_name
        )
    
    except InvalidMarketError as e:
        logger.error(f"Invalid market: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        logger.exception(f"Unexpected error during comparison: {e}")
        raise HTTPException(status_code=500, detail="Internal server error occurred")


@router.get("/market-regime", response_model=MarketRegimeResponse)
def analyze_market_regime(market: str, timeframe: str = "1h"):
    """
    Analyze Market Regime
    
    Classifies current market conditions to help select appropriate strategies:
    
    Regimes:
    - **Trending**: Strong directional movement (use trend-following strategies)
    - **Ranging**: Price oscillates within bounds (use mean reversion)
    - **Volatile**: High volatility regardless of trend (reduce position sizes)
    
    Metrics:
    - Trend Strength: 0-1 scale (higher = stronger trend)
    - Volatility Level: Low/Medium/High classification
    - Price Change: % change over analysis period
    
    This is market intelligence, not strategy testing.
    Use this to decide which strategy to apply.
    
    Returns:
        Market regime classification and metrics
    
    Raises:
        400: Invalid parameters
        404: Market not found
        500: Internal server error
    """
    try:
        logger.info(f"Market regime analysis request: {market} {timeframe}")
        
        # Fetch market data
        data_client = get_data_client()
        df = data_client.fetch_historical_candles(
            market=market,
            timeframe=timeframe,
            limit=settings.DEFAULT_CANDLE_LIMIT
        )
        
        logger.info(f"Fetched {len(df)} candles for regime analysis")
        
        # Analyze regime
        analyzer = MarketRegimeAnalyzer(df)
        regime_data = analyzer.analyze()
        
        logger.info(f"Regime analysis complete: {regime_data['regime']}")
        
        return MarketRegimeResponse(
            market=market,
            timeframe=timeframe,
            **regime_data
        )
    
    except InvalidMarketError as e:
        logger.error(f"Invalid market: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        logger.exception(f"Unexpected error during regime analysis: {e}")
        raise HTTPException(status_code=500, detail="Internal server error occurred")


@router.post("/risk-analysis", response_model=RiskAnalysisResponse)
def analyze_risk(request: RiskAnalysisRequest):
    """
    Comprehensive Risk Analysis
    
    Analyzes risk characteristics of a trading strategy.
    
    Unlike /backtest (which focuses on profit), this focuses on RISK:
    
    Risk Metrics:
    - Return Volatility: How consistent are the returns?
    - Max Consecutive Losses: Longest losing streak
    - Largest Loss: Worst single trade
    - Average Loss: Typical losing trade size
    - Value at Risk (95%): Maximum expected loss at 95% confidence
    - Risk Level: Overall classification (Low/Medium/High)
    
    Use this to:
    - Understand strategy danger zones
    - Set appropriate position sizes
    - Decide if strategy matches risk tolerance
    
    Returns:
        Risk metrics and performance summary
    
    Raises:
        400: Invalid parameters
        404: Market not found
        500: Internal server error
    """
    try:
        logger.info(f"Risk analysis request: {request.strategy} on {request.market}")
        
        # Fetch market data
        data_client = get_data_client()
        df = data_client.fetch_historical_candles(
            market=request.market,
            timeframe=request.timeframe,
            limit=settings.DEFAULT_CANDLE_LIMIT
        )
        
        logger.info(f"Fetched {len(df)} candles for risk analysis")
        
        # Execute strategy
        if request.strategy == "ema_crossover":
            strategy = EMAStrategy()
        elif request.strategy == "rsi_mean_reversion":
            strategy = RSIStrategy()
        else:
            raise HTTPException(status_code=400, detail=f"Unknown strategy: {request.strategy}")
        
        trades = strategy.execute(data=df, parameters=request.parameters)
        
        logger.info(f"Strategy executed: {len(trades)} trades")
        
        # Calculate performance metrics (for reference)
        performance_metrics = MetricsCalculator.calculate(trades, request.initial_capital)
        
        # Analyze risk
        risk_analyzer = RiskAnalyzer(trades, request.initial_capital)
        risk_data = risk_analyzer.analyze()
        
        logger.info(f"Risk analysis complete: Risk Level = {risk_data['risk_level']}")
        
        return RiskAnalysisResponse(
            strategy=request.strategy,
            market=request.market,
            timeframe=request.timeframe,
            risk_metrics=RiskMetrics(**risk_data),
            performance_summary=BacktestResults(**performance_metrics)
        )
    
    except InvalidMarketError as e:
        logger.error(f"Invalid market: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        logger.exception(f"Unexpected error during risk analysis: {e}")
        raise HTTPException(status_code=500, detail="Internal server error occurred")
