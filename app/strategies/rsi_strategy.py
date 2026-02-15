"""RSI Mean Reversion Strategy Implementation"""
from typing import Dict, List
import pandas as pd
import logging
from .base import Strategy
from ..core.exceptions import StrategyExecutionError

logger = logging.getLogger(__name__)


class RSIStrategy(Strategy):
    """
    RSI (Relative Strength Index) Mean Reversion Strategy
    
    Trading Logic:
    - BUY: When RSI crosses below oversold threshold (e.g., 30) - expecting bounce
    - SELL: When RSI crosses above overbought threshold (e.g., 70) - expecting pullback
    
    Parameters:
    - period: RSI calculation period (default: 14)
    - oversold: RSI level considered oversold (default: 30)
    - overbought: RSI level considered overbought (default: 70)
    """
    
    @property
    def name(self) -> str:
        return "rsi_mean_reversion"
    
    @property
    def description(self) -> str:
        return "RSI Mean Reversion Strategy using oversold/overbought levels"
    
    def execute(self, data: pd.DataFrame, parameters: Dict) -> List[Dict]:
        """
        Execute RSI Mean Reversion strategy on historical data
        
        Args:
            data: DataFrame with 'close' column
            parameters: Dict with 'period', 'oversold', and 'overbought'
            
        Returns:
            List of completed trades
        """
        # Validate inputs
        self.validate_parameters(parameters)
        
        if 'close' not in data.columns:
            raise StrategyExecutionError("Data must contain 'close' column")
        
        if len(data) < parameters['period'] + 1:
            raise StrategyExecutionError(
                f"Insufficient data: need at least {parameters['period'] + 1} candles"
            )
        
        # Calculate RSI
        df = self._calculate_rsi(data.copy(), parameters['period'])
        
        # Detect signals and simulate trades
        trades = self._simulate_trades(
            df, 
            parameters['oversold'], 
            parameters['overbought']
        )
        
        logger.info(f"RSI Strategy executed: {len(trades)} trades generated")
        return trades
    
    def validate_parameters(self, parameters: Dict) -> bool:
        """
        Validate RSI strategy parameters
        
        Args:
            parameters: Must contain 'period', 'oversold', and 'overbought'
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If parameters are invalid
        """
        if 'period' not in parameters:
            raise ValueError("Missing required parameter: period")
        
        if 'oversold' not in parameters:
            raise ValueError("Missing required parameter: oversold")
        
        if 'overbought' not in parameters:
            raise ValueError("Missing required parameter: overbought")
        
        period = parameters['period']
        oversold = parameters['oversold']
        overbought = parameters['overbought']
        
        if not isinstance(period, int) or period <= 0:
            raise ValueError(f"period must be positive integer, got {period}")
        
        if not isinstance(oversold, (int, float)) or oversold <= 0 or oversold >= 100:
            raise ValueError(f"oversold must be between 0 and 100, got {oversold}")
        
        if not isinstance(overbought, (int, float)) or overbought <= 0 or overbought >= 100:
            raise ValueError(f"overbought must be between 0 and 100, got {overbought}")
        
        if oversold >= overbought:
            raise ValueError(
                f"oversold ({oversold}) must be less than overbought ({overbought})"
            )
        
        return True
    
    def get_required_indicators(self) -> List[str]:
        """Required indicators for RSI strategy"""
        return ['rsi']
    
    def _calculate_rsi(self, df: pd.DataFrame, period: int) -> pd.DataFrame:
        """
        Calculate Relative Strength Index (RSI)
        
        RSI Formula:
        1. Calculate price changes: delta = close - previous_close
        2. Separate gains and losses
        3. Calculate average gain and average loss over period
        4. RS = average_gain / average_loss
        5. RSI = 100 - (100 / (1 + RS))
        
        RSI ranges from 0 to 100:
        - RSI > 70: Overbought (potential sell)
        - RSI < 30: Oversold (potential buy)
        """
        # Calculate price changes
        delta = df['close'].diff()
        
        # Separate gains and losses
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)
        
        # Calculate exponential moving average of gains and losses
        avg_gain = gains.ewm(span=period, adjust=False).mean()
        avg_loss = losses.ewm(span=period, adjust=False).mean()
        
        # Calculate RS and RSI
        rs = avg_gain / avg_loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        return df
    
    def _simulate_trades(
        self, 
        df: pd.DataFrame, 
        oversold: float, 
        overbought: float
    ) -> List[Dict]:
        """
        Simulate trades based on RSI mean reversion signals
        
        Buy Signal:
        - RSI crosses BELOW oversold threshold (expecting bounce)
        
        Sell Signal:
        - RSI crosses ABOVE overbought threshold (profit taking)
        OR
        - RSI crosses below a mid-level if holding (stop loss)
        """
        trades = []
        position_open = False
        entry_price = 0
        entry_index = 0
        
        for i in range(1, len(df)):
            current_rsi = df['rsi'].iloc[i]
            prev_rsi = df['rsi'].iloc[i-1]
            current_price = df['close'].iloc[i]
            
            # Skip if RSI is NaN (initial period)
            if pd.isna(current_rsi) or pd.isna(prev_rsi):
                continue
            
            # Buy Signal: RSI crosses below oversold level
            if not position_open and current_rsi < oversold and prev_rsi >= oversold:
                position_open = True
                entry_price = current_price
                entry_index = i
                logger.debug(
                    f"RSI Oversold at index {i}: RSI={current_rsi:.2f}, Entry at {entry_price}"
                )
            
            # Sell Signal: RSI crosses above overbought level (take profit)
            elif position_open and current_rsi > overbought and prev_rsi <= overbought:
                exit_price = current_price
                trade_return = (exit_price - entry_price) / entry_price
                
                trades.append({
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'return': trade_return,
                    'entry_index': entry_index,
                    'exit_index': i,
                    'exit_reason': 'overbought'
                })
                
                logger.debug(
                    f"RSI Overbought at index {i}: RSI={current_rsi:.2f}, "
                    f"Exit at {exit_price}, Return: {trade_return:.2%}"
                )
                position_open = False
            
            # Alternative exit: RSI crosses back below 50 (mid-level stop)
            elif position_open and current_rsi < 50 and prev_rsi >= 50 and i > entry_index + 5:
                exit_price = current_price
                trade_return = (exit_price - entry_price) / entry_price
                
                trades.append({
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'return': trade_return,
                    'entry_index': entry_index,
                    'exit_index': i,
                    'exit_reason': 'mid_level_exit'
                })
                
                logger.debug(
                    f"RSI Mid-level exit at index {i}: RSI={current_rsi:.2f}, "
                    f"Exit at {exit_price}, Return: {trade_return:.2%}"
                )
                position_open = False
        
        return trades
