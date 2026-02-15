"""Market Regime Analysis - Classify market conditions"""
import pandas as pd
import numpy as np
from typing import Dict, Any


class MarketRegimeAnalyzer:
    """
    Analyzes market behavior to classify regime
    
    Regimes:
    - Trending: Strong directional movement
    - Ranging: Price oscillates within bounds
    - Volatile: High volatility regardless of trend
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize analyzer with market data
        
        Args:
            df: DataFrame with OHLCV data (must have 'close' column)
        """
        self.df = df.copy()
        self.close = df['close'].values
        
    def analyze(self) -> Dict[str, Any]:
        """
        Perform comprehensive market regime analysis
        
        Returns:
            Dict with regime classification and metrics
        """
        # Calculate trend strength
        trend_strength = self._calculate_trend_strength()
        
        # Calculate volatility
        volatility = self._calculate_volatility()
        
        # Calculate price change
        price_change_pct = (self.close[-1] - self.close[0]) / self.close[0]
        
        # Classify regime
        regime = self._classify_regime(trend_strength, volatility)
        
        # Classify volatility level
        volatility_level = self._classify_volatility(volatility)
        
        return {
            "regime": regime,
            "trend_strength": round(trend_strength, 4),
            "volatility_level": volatility_level,
            "volatility_value": round(volatility, 4),
            "price_change_pct": round(price_change_pct, 4)
        }
    
    def _calculate_trend_strength(self) -> float:
        """
        Calculate trend strength using linear regression R²
        
        Returns:
            Trend strength between 0 and 1
        """
        n = len(self.close)
        x = np.arange(n)
        
        # Linear regression
        slope, intercept = np.polyfit(x, self.close, 1)
        y_pred = slope * x + intercept
        
        # Calculate R² (coefficient of determination)
        ss_res = np.sum((self.close - y_pred) ** 2)
        ss_tot = np.sum((self.close - np.mean(self.close)) ** 2)
        
        if ss_tot == 0:
            return 0.0
        
        r_squared = 1 - (ss_res / ss_tot)
        
        # Return absolute value (trend strength regardless of direction)
        return abs(r_squared)
    
    def _calculate_volatility(self) -> float:
        """
        Calculate volatility as standard deviation of returns
        
        Returns:
            Volatility (annualized)
        """
        returns = np.diff(self.close) / self.close[:-1]
        
        if len(returns) == 0:
            return 0.0
        
        # Standard deviation of returns
        volatility = np.std(returns)
        
        # Annualize (assuming hourly data, 24*365 periods per year)
        annualized_volatility = volatility * np.sqrt(24 * 365)
        
        return annualized_volatility
    
    def _classify_regime(self, trend_strength: float, volatility: float) -> str:
        """
        Classify market regime based on trend and volatility
        
        Args:
            trend_strength: Trend strength (0-1)
            volatility: Volatility value
            
        Returns:
            Regime classification: "Trending", "Ranging", or "Volatile"
        """
        # High volatility dominates classification
        if volatility > 1.5:
            return "Volatile"
        
        # Strong trend
        if trend_strength > 0.6:
            return "Trending"
        
        # Weak trend = Ranging
        return "Ranging"
    
    def _classify_volatility(self, volatility: float) -> str:
        """
        Classify volatility level
        
        Args:
            volatility: Volatility value
            
        Returns:
            "Low", "Medium", or "High"
        """
        if volatility < 0.5:
            return "Low"
        elif volatility < 1.5:
            return "Medium"
        else:
            return "High"
