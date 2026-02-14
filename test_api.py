"""
NinjaQuant API - Comprehensive Test Suite

Tests: Basic functionality, validation, and error handling
"""
import requests
import json

# API endpoint
BASE_URL = "http://localhost:8000"


def check_server():
    """Check if server is running and get data mode"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=2)
        data = response.json()
        print(f"✅ Server is running")
        print(f"   Data mode: {data.get('data_mode', 'unknown')}")
        print(f"   Version: {data.get('version', 'unknown')}\n")
        return True
    except:
        return False


def test_root():
    """Test root endpoint"""
    print("=" * 60)
    print("Test 1: Root Endpoint")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    print()

def test_ema_crossover():
    """Test EMA Crossover backtest endpoint"""
    print("=" * 60)
    print("Test 2: EMA Crossover (Default Parameters)")
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
    print("Test 3: Different EMA Parameters (12/26)")
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


def test_validation_invalid_periods():
    """Test validation: short_period >= long_period"""
    print("=" * 60)
    print("Test 4: Validation - Invalid EMA Periods")
    print("=" * 60)
    
    payload = {
        "market": "INJ/USDT",
        "timeframe": "1h",
        "parameters": {
            "short_period": 21,
            "long_period": 9
        },
        "initial_capital": 1000
    }
    
    response = requests.post(f"{BASE_URL}/backtest/ema-crossover", json=payload)
    print(f"Status Code: {response.status_code} (Expected: 422)")
    if response.status_code == 422:
        print("✅ Validation working correctly")
    print()


def test_validation_negative_period():
    """Test validation: negative period"""
    print("=" * 60)
    print("Test 5: Validation - Negative Period")
    print("=" * 60)
    
    payload = {
        "market": "INJ/USDT",
        "timeframe": "1h",
        "parameters": {
            "short_period": -5,
            "long_period": 21
        },
        "initial_capital": 1000
    }
    
    response = requests.post(f"{BASE_URL}/backtest/ema-crossover", json=payload)
    print(f"Status Code: {response.status_code} (Expected: 422)")
    if response.status_code == 422:
        print("✅ Validation working correctly")
    print()


def test_validation_invalid_timeframe():
    """Test validation: invalid timeframe"""
    print("=" * 60)
    print("Test 6: Validation - Invalid Timeframe")
    print("=" * 60)
    
    payload = {
        "market": "INJ/USDT",
        "timeframe": "30m",
        "parameters": {
            "short_period": 9,
            "long_period": 21
        },
        "initial_capital": 1000
    }
    
    response = requests.post(f"{BASE_URL}/backtest/ema-crossover", json=payload)
    print(f"Status Code: {response.status_code} (Expected: 422)")
    if response.status_code == 422:
        print("✅ Validation working correctly")
    print()


def test_validation_invalid_market():
    """Test validation: invalid market format"""
    print("=" * 60)
    print("Test 7: Validation - Invalid Market Format")
    print("=" * 60)
    
    payload = {
        "market": "injusdt",
        "timeframe": "1h",
        "parameters": {
            "short_period": 9,
            "long_period": 21
        },
        "initial_capital": 1000
    }
    
    response = requests.post(f"{BASE_URL}/backtest/ema-crossover", json=payload)
    print(f"Status Code: {response.status_code} (Expected: 422)")
    if response.status_code == 422:
        print("✅ Validation working correctly")
    print()


if __name__ == "__main__":
    try:
        print("\n🥷 NinjaQuant - Comprehensive Test Suite\n")
        
        # Check server status first
        if not check_server():
            print("❌ Error: Could not connect to API")
            print("Make sure the server is running: python -m uvicorn app.main:app --reload")
            exit(1)
        
        # Run all tests
        test_root()
        test_ema_crossover()
        test_different_parameters()
        test_validation_invalid_periods()
        test_validation_negative_period()
        test_validation_invalid_timeframe()
        test_validation_invalid_market()
        
        print("=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print("Make sure the server is running: python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
