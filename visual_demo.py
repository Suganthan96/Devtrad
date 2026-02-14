"""
🥷 NinjaQuant API - Visual Demo
Shows multiple backtests with different parameters
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_header(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_results(response_data):
    results = response_data['results']
    
    print(f"\n📊 Strategy: {response_data['strategy'].upper()}")
    print(f"📈 Market: {response_data['market']}")
    print(f"⏰ Timeframe: {response_data['timeframe']}")
    print("\n" + "-" * 70)
    print("PERFORMANCE METRICS:")
    print("-" * 70)
    print(f"  Win Rate:        {results['win_rate']:.2%} ({results['win_rate']*100:.1f}%)")
    print(f"  Total Return:    {results['total_return']:.2%} ({results['total_return']*100:.1f}%)")
    print(f"  Max Drawdown:    {results['max_drawdown']:.2%} ({results['max_drawdown']*100:.1f}%)")
    print(f"  Sharpe Ratio:    {results['sharpe_ratio']:.4f}")
    print(f"  Total Trades:    {results['total_trades']}")
    print("-" * 70)
    
    # Performance rating
    if results['total_return'] > 0.1:
        rating = "🟢 EXCELLENT"
    elif results['total_return'] > 0:
        rating = "🟡 POSITIVE"
    else:
        rating = "🔴 NEGATIVE"
    
    print(f"\n  Performance Rating: {rating}")

def run_backtest(name, market, timeframe, short, long, capital):
    print_header(name)
    
    payload = {
        "market": market,
        "timeframe": timeframe,
        "parameters": {
            "short_period": short,
            "long_period": long
        },
        "initial_capital": capital
    }
    
    print(f"\n⚙️  Configuration:")
    print(f"   Short EMA: {short}")
    print(f"   Long EMA:  {long}")
    print(f"   Capital:   ${capital:,.2f}")
    
    try:
        response = requests.post(f"{BASE_URL}/backtest/ema-crossover", json=payload)
        response.raise_for_status()
        print_results(response.json())
        return True
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    print("\n" + "=" * 70)
    print("  🥷 NINJAQUANT - INJECTIVE STRATEGY BACKTESTING API")
    print("=" * 70)
    print(f"\n  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  API Endpoint: {BASE_URL}")
    
    # Test 1: Default parameters
    run_backtest(
        "Test 1: Standard EMA Crossover (9/21)",
        "INJ/USDT",
        "1h",
        9, 21,
        1000
    )
    
    # Test 2: Faster EMAs
    run_backtest(
        "Test 2: Fast EMA Crossover (5/13)",
        "INJ/USDT",
        "1h",
        5, 13,
        1000
    )
    
    # Test 3: Slower EMAs
    run_backtest(
        "Test 3: Slow EMA Crossover (12/26)",
        "INJ/USDT",
        "4h",
        12, 26,
        5000
    )
    
    # Test 4: Very slow EMAs
    run_backtest(
        "Test 4: Conservative EMA Crossover (20/50)",
        "INJ/USDT",
        "1d",
        20, 50,
        10000
    )
    
    print("\n" + "=" * 70)
    print("  ✅ ALL BACKTESTS COMPLETED")
    print("=" * 70)
    print("\n💡 Key Insights:")
    print("   • Different EMA periods produce different trade frequencies")
    print("   • Faster EMAs = more trades, more signals")
    print("   • Slower EMAs = fewer trades, stronger trends")
    print("   • Use Sharpe Ratio to compare risk-adjusted performance")
    print("\n📚 Next Steps:")
    print("   • View API docs: http://localhost:8000/docs")
    print("   • Try your own parameters")
    print("   • Compare different strategies")
    print("\n" + "=" * 70 + "\n")

if __name__ == "__main__":
    main()
