"""Risk Analysis - Comprehensive risk metrics for trading strategies"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Union


class RiskAnalyzer:
    """
    Analyzes risk characteristics of a trading strategy
    
    Focuses on:
    - Return volatility
    - Consecutive losses
    - Loss magnitude
    - Value at Risk (VaR)
    """
    
    def __init__(self, trades: List[Union[Dict, Any]], initial_capital: float):
        """
        Initialize risk analyzer
        
        Args:
            trades: List of trades from backtest (dicts or Trade objects)
            initial_capital: Starting capital
        """
        self.trades = trades
        self.initial_capital = initial_capital
        
    def analyze(self) -> Dict[str, Any]:
        """
        Perform comprehensive risk analysis
        
        Returns:
            Dict with risk metrics
        """
        if not self.trades:
            # No trades = no risk (but also no profit)
            return {
                "return_volatility": 0.0,
                "max_consecutive_losses": 0,
                "largest_loss": 0.0,
                "avg_loss": 0.0,
                "risk_level": "Low",
                "value_at_risk_95": 0.0
            }
        
        # Extract returns (handle both dict and object)
        returns = []
        for trade in self.trades:
            if isinstance(trade, dict):
                # Trades from strategies use 'return' key
                returns.append(trade.get('return', trade.get('return_pct', 0)))
            else:
                # Trade objects use 'return_pct' attribute
                returns.append(getattr(trade, 'return_pct', getattr(trade, 'return', 0)))
        
        # Calculate metrics
        return_volatility = self._calculate_return_volatility(returns)
        max_consecutive_losses = self._calculate_max_consecutive_losses(returns)
        largest_loss = self._calculate_largest_loss(returns)
        avg_loss = self._calculate_avg_loss(returns)
        var_95 = self._calculate_value_at_risk(returns, confidence=0.95)
        risk_level = self._classify_risk(return_volatility, max_consecutive_losses, largest_loss)
        
        return {
            "return_volatility": round(return_volatility, 4),
            "max_consecutive_losses": max_consecutive_losses,
            "largest_loss": round(largest_loss, 4),
            "avg_loss": round(avg_loss, 4),
            "risk_level": risk_level,
            "value_at_risk_95": round(var_95, 4)
        }
    
    def _calculate_return_volatility(self, returns: List[float]) -> float:
        """
        Calculate volatility of trade returns
        
        Args:
            returns: List of trade returns
            
        Returns:
            Standard deviation of returns
        """
        if len(returns) < 2:
            return 0.0
        
        return float(np.std(returns))
    
    def _calculate_max_consecutive_losses(self, returns: List[float]) -> int:
        """
        Calculate maximum consecutive losing trades
        
        Args:
            returns: List of trade returns
            
        Returns:
            Maximum consecutive losses
        """
        max_consecutive = 0
        current_consecutive = 0
        
        for ret in returns:
            if ret < 0:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 0
        
        return max_consecutive
    
    def _calculate_largest_loss(self, returns: List[float]) -> float:
        """
        Calculate largest single trade loss
        
        Args:
            returns: List of trade returns
            
        Returns:
            Largest loss (negative value)
        """
        losses = [r for r in returns if r < 0]
        
        if not losses:
            return 0.0
        
        return float(min(losses))
    
    def _calculate_avg_loss(self, returns: List[float]) -> float:
        """
        Calculate average losing trade
        
        Args:
            returns: List of trade returns
            
        Returns:
            Average loss
        """
        losses = [r for r in returns if r < 0]
        
        if not losses:
            return 0.0
        
        return float(np.mean(losses))
    
    def _calculate_value_at_risk(self, returns: List[float], confidence: float = 0.95) -> float:
        """
        Calculate Value at Risk (VaR)
        
        VaR represents the maximum expected loss at a given confidence level
        
        Args:
            returns: List of trade returns
            confidence: Confidence level (e.g., 0.95 for 95%)
            
        Returns:
            VaR value (negative = loss)
        """
        if len(returns) < 2:
            return 0.0
        
        # Calculate percentile
        percentile = (1 - confidence) * 100
        var = float(np.percentile(returns, percentile))
        
        return var
    
    def _classify_risk(self, volatility: float, max_consecutive_losses: int, largest_loss: float) -> str:
        """
        Classify overall risk level
        
        Args:
            volatility: Return volatility
            max_consecutive_losses: Max consecutive losing trades
            largest_loss: Largest single loss
            
        Returns:
            Risk classification: "Low", "Medium", or "High"
        """
        risk_score = 0
        
        # Volatility scoring
        if volatility > 0.15:
            risk_score += 2
        elif volatility > 0.08:
            risk_score += 1
        
        # Consecutive losses scoring
        if max_consecutive_losses > 5:
            risk_score += 2
        elif max_consecutive_losses > 3:
            risk_score += 1
        
        # Largest loss scoring
        if largest_loss < -0.15:  # More than 15% loss
            risk_score += 2
        elif largest_loss < -0.08:  # More than 8% loss
            risk_score += 1
        
        # Classify based on total score
        if risk_score <= 2:
            return "Low"
        elif risk_score <= 4:
            return "Medium"
        else:
            return "High"
