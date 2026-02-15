"""
🚀 ADVANCED API DEMO - Three Professional-Grade Endpoints
==========================================================

This demo showcases the three advanced APIs that make NinjaQuant 
a professional-grade quantitative trading platform.
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


def print_header(title: str):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"🎯 {title}")
    print("="*70)


def print_result(result: Dict[Any, Any]):
    """Print formatted JSON result"""
    print(json.dumps(result, indent=2))


def test_strategy_comparison():
    """
    API #1: Strategy Comparison
    Compare multiple strategy configurations in one request
    """
    print_header("API #1: STRATEGY COMPARISON")
    
    request_body = {
        "market": "BTC/USDT PERP",
        "timeframe": "1h",
        "strategies": [
            {
                "strategy": "ema_crossover",
                "parameters": {
                    "short_period": 9,
                    "long_period": 21
                }
            },
            {
                "strategy": "ema_crossover",
                "parameters": {
                    "short_period": 12,
                    "long_period": 26
                }
            },
            {
                "strategy": "rsi_mean_reversion",
                "parameters": {
                    "period": 14,
                    "oversold": 30,
                    "overbought": 70
                }
            }
        ],
        "initial_capital": 10000
    }
    
    print("\n📊 Comparing 3 strategies on BTC/USDT PERP...")
    print("   - EMA(9,21)")
    print("   - EMA(12,26)")
    print("   - RSI(14,30,70)")
    
    response = requests.post(f"{BASE_URL}/compare", json=request_body)
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ RESULTS:")
        print(f"\n🏆 Best Strategy: {result['best_strategy']}")
        print(f"\n📈 Performance Comparison:")
        
        for strategy in result['comparison']:
            print(f"\n   {strategy['strategy_name']}:")
            print(f"      Win Rate: {strategy['win_rate']:.2%}")
            print(f"      Total Return: {strategy['total_return']:.2%}")
            print(f"      Sharpe Ratio: {strategy['sharpe_ratio']:.4f}")
            print(f"      Max Drawdown: {strategy['max_drawdown']:.2%}")
            print(f"      Total Trades: {strategy['total_trades']}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")


def test_market_regime():
    """
    API #2: Market Regime Analysis
    Analyze market conditions to choose appropriate strategies
    """
    print_header("API #2: MARKET REGIME ANALYSIS")
    
    markets = ["BTC/USDT PERP", "ETH/USDT PERP", "INJ/USDT PERP"]
    
    print("\n📊 Analyzing market regimes for all markets...")
    
    for market in markets:
        response = requests.get(
            f"{BASE_URL}/market-regime",
            params={"market": market, "timeframe": "1h"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n   {market}:")
            print(f"      Regime: {result['regime']}")
            print(f"      Trend Strength: {result['trend_strength']:.4f}")
            print(f"      Volatility: {result['volatility_level']} ({result['volatility_value']:.4f})")
            print(f"      Price Change: {result['price_change_pct']:.2%}")
            
            # Strategy recommendation
            if result['regime'] == "Trending":
                print(f"      💡 Recommendation: Use EMA Crossover")
            elif result['regime'] == "Ranging":
                print(f"      💡 Recommendation: Use RSI Mean Reversion")
            else:
                print(f"      💡 Recommendation: Reduce position sizes")
        else:
            print(f"   ❌ Error for {market}: {response.status_code}")


def test_risk_analysis():
    """
    API #3: Risk Analysis
    Comprehensive risk metrics for strategy evaluation
    """
    print_header("API #3: RISK ANALYSIS")
    
    request_body = {
        "market": "ETH/USDT PERP",
        "timeframe": "1h",
        "strategy": "rsi_mean_reversion",
        "parameters": {
            "period": 14,
            "oversold": 30,
            "overbought": 70
        },
        "initial_capital": 10000
    }
    
    print("\n📊 Analyzing risk for RSI strategy on ETH/USDT PERP...")
    
    response = requests.post(f"{BASE_URL}/risk-analysis", json=request_body)
    
    if response.status_code == 200:
        result = response.json()
        risk = result['risk_metrics']
        perf = result['performance_summary']
        
        print("\n✅ RISK METRICS:")
        print(f"   Return Volatility: {risk['return_volatility']:.4f}")
        print(f"   Max Consecutive Losses: {risk['max_consecutive_losses']}")
        print(f"   Largest Loss: {risk['largest_loss']:.2%}")
        print(f"   Average Loss: {risk['avg_loss']:.2%}")
        print(f"   Value at Risk (95%): {risk['value_at_risk_95']:.2%}")
        print(f"   🎯 Risk Level: {risk['risk_level']}")
        
        print("\n📈 PERFORMANCE SUMMARY:")
        print(f"   Win Rate: {perf['win_rate']:.2%}")
        print(f"   Total Return: {perf['total_return']:.2%}")
        print(f"   Sharpe Ratio: {perf['sharpe_ratio']:.4f}")
        print(f"   Total Trades: {perf['total_trades']}")
        
        # Risk assessment
        if risk['risk_level'] == "Low":
            print(f"\n   ✅ This is a LOW risk strategy")
        elif risk['risk_level'] == "Medium":
            print(f"\n   ⚠️  This is a MEDIUM risk strategy")
        else:
            print(f"\n   🚨 This is a HIGH risk strategy - use with caution!")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")


def main():
    """Run all API demos"""
    print("\n" + "="*70)
    print("🥷 NINJAQUANT - ADVANCED API DEMO")
    print("="*70)
    print("\nThese three APIs demonstrate professional-grade quant capabilities:")
    print("1. 🔬 Strategy Comparison - Test multiple configs at once")
    print("2. 🌡️  Market Regime Analysis - Classify market conditions")
    print("3. 📊 Risk Analysis - Comprehensive risk metrics")
    
    try:
        # Test API #1
        test_strategy_comparison()
        
        # Test API #2
        test_market_regime()
        
        # Test API #3
        test_risk_analysis()
        
        print("\n" + "="*70)
        print("✅ ALL ADVANCED APIS TESTED SUCCESSFULLY!")
        print("="*70)
        print("\n🎉 NinjaQuant is ready for the hackathon! 🚀\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print("Make sure the server is running:")
        print("  python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
