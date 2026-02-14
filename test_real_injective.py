"""Quick test of real Injective integration"""
import requests
import json
import time

print("🥷 Testing Real Injective Integration\n")

# Wait for server
time.sleep(3)

# Test 1: Check data mode
print("=" * 60)
print("Step 1: Checking data mode...")
print("=" * 60)
try:
    response = requests.get("http://localhost:8000/", timeout=5)
    data = response.json()
    print(f"✅ Server running")
    print(f"   Data mode: {data.get('data_mode')}")
    print(f"   Expected: real\n")
except Exception as e:
    print(f"❌ Error: {e}\n")
    exit(1)

# Test 2: Call backtest endpoint with real data
print("=" * 60)
print("Step 2: Testing EMA Backtest with Real Injective Data...")
print("=" * 60)

payload = {
    "market": "INJ/USDT",
    "timeframe": "1h",
    "parameters": {
        "short_period": 9,
        "long_period": 21
    },
    "initial_capital": 1000
}

print(f"Request: {json.dumps(payload, indent=2)}\n")

try:
    response = requests.post(
        "http://localhost:8000/backtest/ema-crossover",
        json=payload,
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ SUCCESS! Real Injective data working!")
        print(f"\nBacktest Results:")
        print(f"  Win Rate: {result['results']['win_rate']}")
        print(f"  Total Return: {result['results']['total_return']}")
        print(f"  Total Trades: {result['results']['total_trades']}")
        
    elif response.status_code == 503:
        print(f"\n⚠️  Injective API connection failed")
        print(f"   Response: {response.json()}")
        print(f"\n   Note: Fallback to synthetic data should have worked")
        
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        
except Exception as e:
    print(f"\n❌ Exception: {e}")

print("\n" + "=" * 60)
