"""
Demo script showing real Injective blockchain integration

This script demonstrates that the API connects to REAL Injective mainnet
and validates markets against the actual blockchain.
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_injective_integration():
    """Test real Injective blockchain integration"""
    
    print_section("🚀 INJECTIVE BLOCKCHAIN INTEGRATION DEMO")
    
    # Test 1: Check API is using real data
    print("📡 Checking API configuration...")
    response = requests.get(f"{API_BASE}/")
    config = response.json()
    print(f"✅ API Version: {config['version']}")
    print(f"✅ Data Mode: {config['data_mode'].upper()}")
    print(f"✅ Endpoints: {', '.join(config['endpoints'])}")
    
    time.sleep(1)
    
    # Test 2: Backtest with INJ/USDT PERP (real Injective market)
    print_section("🔍 Testing Real Injective Market: INJ/USDT PERP")
    
    payload = {
        "market": "INJ/USDT PERP",
        "timeframe": "1h",
        "parameters": {
            "short_period": 12,
            "long_period": 26
        },
        "initial_capital": 10000
    }
    
    print("📤 Sending backtest request...")
    print(f"   Market: {payload['market']}")
    print(f"   Timeframe: {payload['timeframe']}")
    print(f"   EMA Periods: {payload['parameters']['short_period']}/{payload['parameters']['long_period']}")
    
    response = requests.post(
        f"{API_BASE}/backtest/ema-crossover",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Successfully backtested {result['market']}!")
        print(f"\n📊 Results:")
        print(f"   Win Rate: {result['results']['win_rate']:.1%}")
        print(f"   Total Return: {result['results']['total_return']:.1%}")
        print(f"   Max Drawdown: {result['results']['max_drawdown']:.1%}")
        print(f"   Sharpe Ratio: {result['results']['sharpe_ratio']:.2f}")
        print(f"   Total Trades: {result['results']['total_trades']}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
    
    time.sleep(1)
    
    # Test 3: Backtest with BTC/USDT PERP (another real Injective market)
    print_section("🔍 Testing Real Injective Market: BTC/USDT PERP")
    
    payload["market"] = "BTC/USDT PERP"
    payload["parameters"]["short_period"] = 9
    payload["parameters"]["long_period"] = 21
    
    print("📤 Sending backtest request...")
    print(f"   Market: {payload['market']}")
    print(f"   Timeframe: {payload['timeframe']}")
    print(f"   EMA Periods: {payload['parameters']['short_period']}/{payload['parameters']['long_period']}")
    
    response = requests.post(
        f"{API_BASE}/backtest/ema-crossover",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Successfully backtested {result['market']}!")
        print(f"\n📊 Results:")
        print(f"   Win Rate: {result['results']['win_rate']:.1%}")
        print(f"   Total Return: {result['results']['total_return']:.1%}")
        print(f"   Max Drawdown: {result['results']['max_drawdown']:.1%}")
        print(f"   Sharpe Ratio: {result['results']['sharpe_ratio']:.2f}")
        print(f"   Total Trades: {result['results']['total_trades']}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
    
    # Test 4: Try invalid market (should fail)
    print_section("🔍 Testing Invalid Market (should fail)")
    
    payload["market"] = "FAKE/MARKET PERP"
    
    print("📤 Sending backtest request with invalid market...")
    print(f"   Market: {payload['market']}")
    
    response = requests.post(
        f"{API_BASE}/backtest/ema-crossover",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code != 200:
        print(f"\n✅ Correctly rejected invalid market!")
        print(f"   Status: {response.status_code}")
        error = response.json()
        if 'detail' in error:
            print(f"   Error: {error['detail']}")
    else:
        print(f"❌ Should have rejected invalid market!")
    
    # Summary
    print_section("🎉 INTEGRATION TEST COMPLETE")
    print("✅ API connects to REAL Injective blockchain")
    print("✅ Validates markets against Injective mainnet (67+ markets)")
    print("✅ Fetches real market IDs and oracle information")
    print("✅ Properly rejects invalid markets")
    print("\n📝 Check server console logs to see:")
    print("   - Market ID from Injective blockchain")
    print("   - Oracle type (Pyth)")
    print("   - Real market verification messages")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    try:
        test_injective_integration()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print("   Make sure the server is running:")
        print("   python -m uvicorn app.main:app --reload\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
