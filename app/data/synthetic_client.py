"""Synthetic data generator for testing and demo purposes"""
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class SyntheticDataClient:
    """Generate synthetic market data for testing and demos"""
    
    def __init__(self, seed: int = 42):
        """
        Initialize synthetic data generator
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        logger.info(f"Initialized SyntheticDataClient with seed={seed}")
    
    def fetch_historical_candles(
        self, 
        market: str, 
        timeframe: str, 
        limit: int = 500
    ) -> pd.DataFrame:
        """
        Generate synthetic OHLCV candles
        
        Args:
            market: Trading pair (ignored, for compatibility)
            timeframe: Candle interval (used for timestamp generation)
            limit: Number of candles to generate
            
        Returns:
            DataFrame with columns: timestamp, open, high, low, close, volume
        """
        logger.info(f"Generating {limit} synthetic candles for {market} ({timeframe})")
        
        np.random.seed(self.seed)
        
        base_price = 10.0
        volatility = 0.02  # 2% volatility
        
        # Generate price movement using random walk
        returns = np.random.randn(limit) * volatility
        close_prices = base_price * np.exp(np.cumsum(returns))
        
        # Generate OHLC from close prices
        data = []
        for i, close in enumerate(close_prices):
            high_factor = 1 + abs(np.random.randn() * 0.005)
            low_factor = 1 - abs(np.random.randn() * 0.005)
            
            open_price = close_prices[i-1] if i > 0 else base_price
            high = max(open_price, close) * high_factor
            low = min(open_price, close) * low_factor
            volume = abs(np.random.randn() * 1000000)
            
            data.append({
                'timestamp': pd.Timestamp('2024-01-01') + pd.Timedelta(hours=i),
                'open': open_price,
                'high': high,
                'low': low,
                'close': close,
                'volume': volume
            })
        
        df = pd.DataFrame(data)
        logger.info(f"Generated {len(df)} synthetic candles")
        return df
