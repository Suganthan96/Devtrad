"""EMA Crossover Strategy Implementation"""
from typing import Dict, List
import pandas as pd
import logging
from .base import Strategy
from ..core.exceptions import StrategyExecutionError

logger = logging.getLogger(__name__)


class EMAStrategy(Strategy):
    """
    Exponential Moving Average Crossover Strategy
    
    Trading Logic:
    - BUY (Golden Cross): When short EMA crosses above long EMA
    - SELL (Death Cross): When short EMA crosses below long EMA
    
    Parameters:
    - short_period: Period for fast EMA (default: 9)
    - long_period: Period for slow EMA (default: 21)
    """
    
    @property
    def name(self) -> str:
        return "ema_crossover"
    
    @property
    def description(self) -> str:
        return "EMA Crossover Strategy using Golden Cross and Death Cross signals"
    
    def execute(self, data: pd.DataFrame, parameters: Dict) -> List[Dict]:
        """
        Execute EMA Crossover strategy on historical data
        
        Args:
            data: DataFrame with 'close' column
            parameters: Dict with 'short_period' and 'long_period'
            
        Returns:
            List of completed trades
        """
        # Validate inputs
        self.validate_parameters(parameters)
        
        if 'close' not in data.columns:
            raise StrategyExecutionError("Data must contain 'close' column")
        
        if len(data) < parameters['long_period']:
            raise StrategyExecutionError(
                f"Insufficient data: need at least {parameters['long_period']} candles"
            )
        
        # Calculate EMAs
        df = self._calculate_ema(data.copy(), parameters['short_period'], parameters['long_period'])
        
        # Detect crossovers and simulate trades
        trades = self._simulate_trades(df)
        
        logger.info(f"EMA Strategy executed: {len(trades)} trades generated")
        return trades
    
    def validate_parameters(self, parameters: Dict) -> bool:
        """
        Validate EMA strategy parameters
        
        Args:
            parameters: Must contain 'short_period' and 'long_period'
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If parameters are invalid
        """
        if 'short_period' not in parameters:
            raise ValueError("Missing required parameter: short_period")
        
        if 'long_period' not in parameters:
            raise ValueError("Missing required parameter: long_period")
        
        short = parameters['short_period']
        long = parameters['long_period']
        
        if not isinstance(short, int) or short <= 0:
            raise ValueError(f"short_period must be positive integer, got {short}")
        
        if not isinstance(long, int) or long <= 0:
            raise ValueError(f"long_period must be positive integer, got {long}")
        
        if short >= long:
            raise ValueError(f"short_period ({short}) must be less than long_period ({long})")
        
        return True
    
    def get_required_indicators(self) -> List[str]:
        """Required indicators for EMA strategy"""
        return ['ema_short', 'ema_long']
    
    def _calculate_ema(
        self, 
        df: pd.DataFrame, 
        short_period: int, 
        long_period: int
    ) -> pd.DataFrame:
        """
        Calculate Exponential Moving Averages
        
        EMA formula: EMA = (CurrentPrice × k) + (PreviousEMA × (1-k))
        where k = 2/(period+1)
        
        Using pandas ewm() for efficient calculation.
        """
        df['ema_short'] = df['close'].ewm(span=short_period, adjust=False).mean()
        df['ema_long'] = df['close'].ewm(span=long_period, adjust=False).mean()
        
        return df
    
    def _simulate_trades(self, df: pd.DataFrame) -> List[Dict]:
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
            
            # Skip if EMAs are NaN (initial period)
            if pd.isna(current_short) or pd.isna(current_long):
                continue
            
            # Buy Signal: Golden Cross
            if not position_open and current_short > current_long and prev_short <= prev_long:
                position_open = True
                entry_price = current_price
                entry_index = i
                logger.debug(f"Golden Cross at index {i}: Entry at {entry_price}")
            
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
                
                logger.debug(f"Death Cross at index {i}: Exit at {exit_price}, Return: {trade_return:.2%}")
                position_open = False
        
        return trades
