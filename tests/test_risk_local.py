"""Test risk analysis locally"""
import sys
sys.path.insert(0, 'D:\\Projects\\Devtrad')

from app.strategies import RSIStrategy
from app.data import InjectiveDataClient
from app.analysis import RiskAnalyzer
from app.core import MetricsCalculator

# Fetch data
client = InjectiveDataClient()
df = client.fetch_historical_candles("ETH/USDT PERP", "1h", 500)

# Execute strategy
strategy = RSIStrategy()
trades = strategy.execute(df, {'period': 14, 'oversold': 30, 'overbought': 70})

print(f"\nTrades generated: {len(trades)}")
if trades:
    print(f"First trade type: {type(trades[0])}")
    print(f"First trade: {trades[0]}")

# Test risk analyzer
try:
    risk_analyzer = RiskAnalyzer(trades, 10000)
    risk_data = risk_analyzer.analyze()
    print(f"\n✅ Risk analysis successful!")
    print(f"Risk Level: {risk_data['risk_level']}")
    print(f"Return Volatility: {risk_data['return_volatility']}")
    print(f"Max Consecutive Losses: {risk_data['max_consecutive_losses']}")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
