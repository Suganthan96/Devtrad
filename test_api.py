import requests
import json

# API endpoint
BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    print("=" * 60)
    print("Testing Root Endpoint")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    print()

def test_ema_crossover():
    """Test EMA Crossover backtest endpoint"""
    print("=" * 60)
    print("Testing EMA Crossover Backtest")
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
    
    print(f"Request Payload:\n{json.dumps(payload, indent=2)}\n")
    
    response = requests.post(
        f"{BASE_URL}/backtest/ema-crossover",
        json=payload
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    print()

def test_different_parameters():
    """Test with different EMA parameters"""
    print("=" * 60)
    print("Testing Different EMA Parameters (12/26)")
    print("=" * 60)
    
    payload = {
        "market": "INJ/USDT",
        "timeframe": "4h",
        "parameters": {
            "short_period": 12,
            "long_period": 26
        },
        "initial_capital": 5000
    }
    
    print(f"Request Payload:\n{json.dumps(payload, indent=2)}\n")
    
    response = requests.post(
        f"{BASE_URL}/backtest/ema-crossover",
        json=payload
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    print()

if __name__ == "__main__":
    try:
        print("\n🥷 NinjaQuant API Test Suite\n")
        
        # Test 1: Root endpoint
        test_root()
        
        # Test 2: EMA Crossover with default parameters
        test_ema_crossover()
        
        # Test 3: Different parameters
        test_different_parameters()
        
        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API")
        print("Make sure the server is running: python -m uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")
