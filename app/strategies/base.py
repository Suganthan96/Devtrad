"""Abstract base class for trading strategies"""
from abc import ABC, abstractmethod
from typing import Dict, List
import pandas as pd


class Strategy(ABC):
    """
    Base class for all trading strategies
    
    All strategies must implement the execute() method which takes
    price data and parameters, then returns a list of trades.
    """
    
    @abstractmethod
    def execute(self, data: pd.DataFrame, parameters: Dict) -> List[Dict]:
        """
        Execute strategy on historical data
        
        Args:
            data: DataFrame with OHLCV data (must have 'close' column minimum)
            parameters: Strategy-specific parameters
            
        Returns:
            List of trade dictionaries with keys:
            - entry_price: Entry price
            - exit_price: Exit price
            - return: Trade return percentage
            - entry_index: DataFrame index at entry
            - exit_index: DataFrame index at exit
        """
        pass
    
    @abstractmethod
    def validate_parameters(self, parameters: Dict) -> bool:
        """
        Validate strategy parameters
        
        Args:
            parameters: Strategy parameters to validate
            
        Returns:
            True if parameters are valid
            
        Raises:
            ValueError: If parameters are invalid
        """
        pass
    
    @abstractmethod
    def get_required_indicators(self) -> List[str]:
        """
        Get list of required technical indicators
        
        Returns:
            List of indicator names needed by this strategy
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Strategy name"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Strategy description"""
        pass
