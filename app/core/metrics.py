"""Performance metrics calculation module"""
from typing import List, Dict
import numpy as np
from ..models.schemas import Trade


class MetricsCalculator:
    """Calculate trading performance metrics"""
    
    @staticmethod
    def calculate(trades: List[Dict], initial_capital: float) -> Dict[str, float]:
        """
        Calculate comprehensive performance metrics from trade history
        
        Args:
            trades: List of trade dictionaries with 'return' key
            initial_capital: Starting portfolio value
            
        Returns:
            Dictionary containing:
            - win_rate: Percentage of profitable trades
            - total_return: Overall portfolio growth
            - max_drawdown: Largest peak-to-trough decline
            - sharpe_ratio: Risk-adjusted return
            - total_trades: Number of completed trades
        """
        if len(trades) == 0:
            return {
                'win_rate': 0.0,
                'total_return': 0.0,
                'max_drawdown': 0.0,
                'sharpe_ratio': 0.0,
                'total_trades': 0
            }
        
        # 1. Win Rate
        winning_trades = sum(1 for trade in trades if trade['return'] > 0)
        win_rate = winning_trades / len(trades) if len(trades) > 0 else 0
        
        # 2. Total Return (compounded)
        capital = initial_capital
        equity_curve = [capital]
        
        for trade in trades:
            capital *= (1 + trade['return'])
            equity_curve.append(capital)
        
        total_return = (capital - initial_capital) / initial_capital
        
        # 3. Max Drawdown
        peak = equity_curve[0]
        max_drawdown = 0
        
        for value in equity_curve:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak if peak > 0 else 0
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        # 4. Sharpe Ratio
        returns = [trade['return'] for trade in trades]
        if len(returns) > 1 and np.std(returns) > 0:
            sharpe_ratio = np.mean(returns) / np.std(returns)
        else:
            sharpe_ratio = 0.0
        
        return {
            'win_rate': round(win_rate, 4),
            'total_return': round(total_return, 4),
            'max_drawdown': round(max_drawdown, 4),
            'sharpe_ratio': round(sharpe_ratio, 4),
            'total_trades': len(trades)
        }
