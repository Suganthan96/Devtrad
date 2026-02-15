"""
Test your deployed Railway API

Replace YOUR_RAILWAY_URL with your actual Railway deployment URL
Example: https://ninjaquant-production.up.railway.app
"""

import requests
import json

# ⚠️ REPLACE THIS with your Railway URL
RAILWAY_URL = "https://your-app-name.up.railway.app"

def test_railway_api():
    """Test the deployed API on Railway"""
    
    print("🚂 Testing NinjaQuant API on Railway")
    print("=" * 60)
    print(f"API URL: {RAILWAY_URL}")
    print("=" * 60)
    print()
    
    # Test 1: Root endpoint
    print("1️⃣ Testing Root Endpoint...")
    try:
        response = requests.get(f"{RAILWAY_URL}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"✅ API Version: {data.get('version')}")
            print(f"✅ Data Mode: {data.get('data_mode').upper()}")
            print(f"✅ Endpoints: {', '.join(data.get('endpoints', []))}")
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"❌ Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure to replace YOUR_RAILWAY_URL with your actual Railway URL!")
        return
    
    print()
    
    # Test 2: API Documentation
    print("2️⃣ Testing API Docs...")
    try:
        response = requests.get(f"{RAILWAY_URL}/docs", timeout=10)
        if response.status_code == 200:
            print(f"✅ Docs available at: {RAILWAY_URL}/docs")
        else:
            print(f"⚠️ Docs returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test 3: Backtest with INJ/USDT PERP
    print("3️⃣ Testing Backtest - INJ/USDT PERP...")
    try:
        payload = {
            "market": "INJ/USDT PERP",
            "timeframe": "1h",
            "parameters": {
                "short_period": 12,
                "long_period": 26
            },
            "initial_capital": 10000
        }
        
        print(f"   Sending request to: {RAILWAY_URL}/backtest/ema-crossover")
        response = requests.post(
            f"{RAILWAY_URL}/backtest/ema-crossover",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"✅ Strategy: {result['strategy']}")
            print(f"✅ Market: {result['market']}")
            print(f"\n📊 Results:")
            print(f"   Win Rate: {result['results']['win_rate']:.1%}")
            print(f"   Total Return: {result['results']['total_return']:.1%}")
            print(f"   Max Drawdown: {result['results']['max_drawdown']:.1%}")
            print(f"   Sharpe Ratio: {result['results']['sharpe_ratio']:.2f}")
            print(f"   Total Trades: {result['results']['total_trades']}")
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"❌ Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test 4: Backtest with BTC/USDT PERP
    print("4️⃣ Testing Backtest - BTC/USDT PERP...")
    try:
        payload = {
            "market": "BTC/USDT PERP",
            "timeframe": "1h",
            "parameters": {
                "short_period": 9,
                "long_period": 21
            }
        }
        
        response = requests.post(
            f"{RAILWAY_URL}/backtest/ema-crossover",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"✅ Market: {result['market']}")
            print(f"\n📊 Results:")
            print(f"   Win Rate: {result['results']['win_rate']:.1%}")
            print(f"   Total Return: {result['results']['total_return']:.1%}")
            print(f"   Total Trades: {result['results']['total_trades']}")
        else:
            print(f"❌ Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("=" * 60)
    print("🎉 Testing Complete!")
    print("=" * 60)
    print(f"\n📝 Your API Links:")
    print(f"   Homepage: {RAILWAY_URL}/")
    print(f"   API Docs: {RAILWAY_URL}/docs")
    print(f"   Redoc: {RAILWAY_URL}/redoc")
    print()


if __name__ == "__main__":
    # Check if URL is set
    if "your-app-name" in RAILWAY_URL.lower() or "example" in RAILWAY_URL.lower():
        print("❌ ERROR: Please update RAILWAY_URL with your actual Railway deployment URL!")
        print("\n📍 To find your Railway URL:")
        print("   1. Go to railway.app dashboard")
        print("   2. Click on your project")
        print("   3. Go to Settings → Domains")
        print("   4. Copy the generated URL (e.g., https://your-project.up.railway.app)")
        print("\n   Then update line 9 in this file:")
        print(f'   RAILWAY_URL = "https://your-actual-url.up.railway.app"')
        print()
    else:
        test_railway_api()
