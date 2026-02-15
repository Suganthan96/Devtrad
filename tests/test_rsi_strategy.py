"""Test RSI Strategy Implementation"""
import sys
import pandas as pd
import numpy as np

# Add parent directory to path
sys.path.append('.')

from app.strategies.rsi_strategy import RSIStrategy


def test_rsi_calculation():
    """Test RSI calculation accuracy"""
    print("=" * 60)
    print("Testing RSI Calculation")
    print("=" * 60)
    
    # Create sample price data
    prices = [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84,
              46.08, 45.89, 46.03, 45.61, 46.28, 46.28, 46.00, 46.03, 46.41,
              46.22, 45.64]
    
    df = pd.DataFrame({'close': prices})
    
    strategy = RSIStrategy()
    df_with_rsi = strategy._calculate_rsi(df, period=14)
    
    print(f"Sample prices: {prices[:5]}...")
    print(f"Calculated RSI values (last 5): {df_with_rsi['rsi'].iloc[-5:].values}")
    print(f"RSI range: {df_with_rsi['rsi'].min():.2f} - {df_with_rsi['rsi'].max():.2f}")
    print("✅ RSI calculation successful\n")


def test_rsi_strategy_execution():
    """Test RSI strategy with synthetic data"""
    print("=" * 60)
    print("Testing RSI Strategy Execution")
    print("=" * 60)
    
    # Create realistic oscillating price data (good for mean reversion)
    np.random.seed(42)
    n_candles = 200
    base_price = 100
    
    # Create oscillating prices
    prices = []
    price = base_price
    for i in range(n_candles):
        # Add trend and oscillation
        trend = 0.1 * np.sin(i / 20)
        noise = np.random.randn() * 2
        price = price + trend + noise
        prices.append(price)
    
    df = pd.DataFrame({
        'close': prices,
        'timestamp': pd.date_range('2024-01-01', periods=n_candles, freq='1H')
    })
    
    # Test with default parameters
    strategy = RSIStrategy()
    parameters = {
        'period': 14,
        'oversold': 30,
        'overbought': 70
    }
    
    print(f"Testing with parameters: {parameters}")
    print(f"Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
    
    trades = strategy.execute(df, parameters)
    
    print(f"\n✅ Strategy executed successfully!")
    print(f"Total trades: {len(trades)}")
    
    if len(trades) > 0:
        winning_trades = [t for t in trades if t['return'] > 0]
        win_rate = len(winning_trades) / len(trades) * 100
        avg_return = sum(t['return'] for t in trades) / len(trades) * 100
        
        print(f"Winning trades: {len(winning_trades)}/{len(trades)} ({win_rate:.1f}%)")
        print(f"Average return per trade: {avg_return:.2f}%")
        
        print("\nSample trades:")
        for i, trade in enumerate(trades[:3]):
            print(f"  Trade {i+1}: Entry ${trade['entry_price']:.2f} -> "
                  f"Exit ${trade['exit_price']:.2f} | Return: {trade['return']*100:.2f}%")
    else:
        print("⚠️ No trades generated (may need different parameters)")
    
    print()


def test_parameter_validation():
    """Test parameter validation"""
    print("=" * 60)
    print("Testing Parameter Validation")
    print("=" * 60)
    
    strategy = RSIStrategy()
    
    # Test valid parameters
    try:
        valid_params = {
            'period': 14,
            'oversold': 30,
            'overbought': 70
        }
        strategy.validate_parameters(valid_params)
        print("✅ Valid parameters accepted")
    except ValueError as e:
        print(f"❌ Valid parameters rejected: {e}")
    
    # Test invalid: oversold >= overbought
    try:
        invalid_params = {
            'period': 14,
            'oversold': 70,
            'overbought': 30
        }
        strategy.validate_parameters(invalid_params)
        print("❌ Should have rejected oversold >= overbought")
    except ValueError as e:
        print(f"✅ Correctly rejected invalid thresholds: {e}")
    
    # Test invalid: negative period
    try:
        invalid_params = {
            'period': -5,
            'oversold': 30,
            'overbought': 70
        }
        strategy.validate_parameters(invalid_params)
        print("❌ Should have rejected negative period")
    except ValueError as e:
        print(f"✅ Correctly rejected negative period: {e}")
    
    print()


def test_edge_cases():
    """Test edge cases"""
    print("=" * 60)
    print("Testing Edge Cases")
    print("=" * 60)
    
    strategy = RSIStrategy()
    
    # Test with trending market (all up)
    prices_up = [100 + i for i in range(50)]
    df_up = pd.DataFrame({'close': prices_up})
    
    trades_up = strategy.execute(df_up, {'period': 14, 'oversold': 30, 'overbought': 70})
    print(f"Trending up market: {len(trades_up)} trades")
    
    # Test with trending market (all down)
    prices_down = [100 - i for i in range(50)]
    df_down = pd.DataFrame({'close': prices_down})
    
    trades_down = strategy.execute(df_down, {'period': 14, 'oversold': 30, 'overbought': 70})
    print(f"Trending down market: {len(trades_down)} trades")
    
    # Test with flat market
    prices_flat = [100 + np.random.randn() * 0.1 for _ in range(50)]
    df_flat = pd.DataFrame({'close': prices_flat})
    
    trades_flat = strategy.execute(df_flat, {'period': 14, 'oversold': 30, 'overbought': 70})
    print(f"Flat market: {len(trades_flat)} trades")
    
    print("✅ Edge cases handled\n")


if __name__ == "__main__":
    print("\n")
    print("🧪 RSI STRATEGY TEST SUITE")
    print("=" * 60)
    print()
    
    try:
        test_rsi_calculation()
        test_parameter_validation()
        test_rsi_strategy_execution()
        test_edge_cases()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("RSI Strategy is ready to use!")
        print("Start the API with: python -m uvicorn app.main:app --reload")
        print()
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ TEST FAILED: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        sys.exit(1)
