"""Test RSI Strategy API Endpoint"""
import requests
import json


API_URL = "http://localhost:8000"


def test_rsi_endpoint():
    """Test RSI Mean Reversion backtest endpoint"""
    print("=" * 70)
    print("🧪 Testing RSI Mean Reversion Strategy API")
    print("=" * 70)
    print()
    
    # Test with INJ/USDT PERP market
    payload = {
        "market": "INJ/USDT PERP",
        "timeframe": "1h",
        "parameters": {
            "period": 14,
            "oversold": 30,
            "overbought": 70
        },
        "initial_capital": 1000.0
    }
    
    print(f"📊 Testing market: {payload['market']}")
    print(f"⏱️  Timeframe: {payload['timeframe']}")
    print(f"🔧 Parameters:")
    print(f"   - RSI Period: {payload['parameters']['period']}")
    print(f"   - Oversold: {payload['parameters']['oversold']}")
    print(f"   - Overbought: {payload['parameters']['overbought']}")
    print(f"💰 Initial Capital: ${payload['initial_capital']}")
    print()
    
    try:
        response = requests.post(
            f"{API_URL}/backtest/rsi-mean-reversion",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Response: SUCCESS")
            print()
            print(f"Strategy: {data['strategy']}")
            print(f"Market: {data['market']}")
            print(f"Timeframe: {data['timeframe']}")
            print()
            print("📈 Performance Metrics:")
            print("-" * 50)
            
            results = data['results']
            print(f"  Win Rate:       {results['win_rate']*100:.2f}%")
            print(f"  Total Return:   {results['total_return']*100:.2f}%")
            print(f"  Max Drawdown:   {results['max_drawdown']*100:.2f}%")
            print(f"  Sharpe Ratio:   {results['sharpe_ratio']:.2f}")
            print(f"  Total Trades:   {results['total_trades']}")
            print()
            
            # Calculate final capital
            final_capital = payload['initial_capital'] * (1 + results['total_return'])
            profit = final_capital - payload['initial_capital']
            print(f"💵 Capital: ${payload['initial_capital']:.2f} → ${final_capital:.2f} (${profit:+.2f})")
            print()
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is the server running?")
        print("   Start with: python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_multiple_markets():
    """Test RSI strategy with multiple Injective markets"""
    print("=" * 70)
    print("🌐 Testing RSI Strategy on Multiple Injective Markets")
    print("=" * 70)
    print()
    
    markets = [
        "INJ/USDT PERP",
        "BTC/USDT PERP",
        "ETH/USDT PERP"
    ]
    
    for market in markets:
        print(f"\n📊 Testing {market}...")
        
        payload = {
            "market": market,
            "timeframe": "1h",
            "parameters": {
                "period": 14,
                "oversold": 30,
                "overbought": 70
            },
            "initial_capital": 1000.0
        }
        
        try:
            response = requests.post(
                f"{API_URL}/backtest/rsi-mean-reversion",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data['results']
                print(f"   ✅ Win Rate: {results['win_rate']*100:.1f}% | "
                      f"Return: {results['total_return']*100:+.2f}% | "
                      f"Trades: {results['total_trades']}")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")


def test_different_parameters():
    """Test RSI with different parameter sets"""
    print()
    print("=" * 70)
    print("🔬 Testing Different RSI Parameters")
    print("=" * 70)
    print()
    
    parameter_sets = [
        {"period": 7, "oversold": 30, "overbought": 70, "name": "Fast RSI (7)"},
        {"period": 14, "oversold": 30, "overbought": 70, "name": "Standard RSI (14)"},
        {"period": 21, "oversold": 30, "overbought": 70, "name": "Slow RSI (21)"},
        {"period": 14, "oversold": 20, "overbought": 80, "name": "Wide Bands (20/80)"},
        {"period": 14, "oversold": 40, "overbought": 60, "name": "Tight Bands (40/60)"},
    ]
    
    for params in parameter_sets:
        print(f"\n🔧 {params['name']}...")
        
        payload = {
            "market": "INJ/USDT PERP",
            "timeframe": "1h",
            "parameters": {
                "period": params['period'],
                "oversold": params['oversold'],
                "overbought": params['overbought']
            },
            "initial_capital": 1000.0
        }
        
        try:
            response = requests.post(
                f"{API_URL}/backtest/rsi-mean-reversion",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data['results']
                print(f"   Return: {results['total_return']*100:+.2f}% | "
                      f"Win Rate: {results['win_rate']*100:.1f}% | "
                      f"Trades: {results['total_trades']} | "
                      f"Sharpe: {results['sharpe_ratio']:.2f}")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")


def compare_ema_vs_rsi():
    """Compare EMA and RSI strategies on same market"""
    print()
    print("=" * 70)
    print("⚔️  EMA vs RSI Strategy Comparison")
    print("=" * 70)
    print()
    
    market = "INJ/USDT PERP"
    timeframe = "1h"
    initial_capital = 1000.0
    
    print(f"Market: {market} | Timeframe: {timeframe}")
    print()
    
    # Test EMA
    print("📊 EMA Crossover Strategy...")
    ema_payload = {
        "market": market,
        "timeframe": timeframe,
        "parameters": {"short_period": 9, "long_period": 21},
        "initial_capital": initial_capital
    }
    
    try:
        ema_response = requests.post(
            f"{API_URL}/backtest/ema-crossover",
            json=ema_payload,
            timeout=30
        )
        
        if ema_response.status_code == 200:
            ema_data = ema_response.json()
            ema_results = ema_data['results']
            print(f"   Return: {ema_results['total_return']*100:+.2f}% | "
                  f"Win Rate: {ema_results['win_rate']*100:.1f}% | "
                  f"Trades: {ema_results['total_trades']} | "
                  f"Sharpe: {ema_results['sharpe_ratio']:.2f}")
        else:
            print(f"   ❌ Error: {ema_response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test RSI
    print()
    print("📊 RSI Mean Reversion Strategy...")
    rsi_payload = {
        "market": market,
        "timeframe": timeframe,
        "parameters": {"period": 14, "oversold": 30, "overbought": 70},
        "initial_capital": initial_capital
    }
    
    try:
        rsi_response = requests.post(
            f"{API_URL}/backtest/rsi-mean-reversion",
            json=rsi_payload,
            timeout=30
        )
        
        if rsi_response.status_code == 200:
            rsi_data = rsi_response.json()
            rsi_results = rsi_data['results']
            print(f"   Return: {rsi_results['total_return']*100:+.2f}% | "
                  f"Win Rate: {rsi_results['win_rate']*100:.1f}% | "
                  f"Trades: {rsi_results['total_trades']} | "
                  f"Sharpe: {rsi_results['sharpe_ratio']:.2f}")
        else:
            print(f"   ❌ Error: {rsi_response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()


if __name__ == "__main__":
    print()
    print("🚀 NinjaQuant API - RSI Strategy Test Suite")
    print()
    
    # Run all tests
    test_rsi_endpoint()
    test_multiple_markets()
    test_different_parameters()
    compare_ema_vs_rsi()
    
    print("=" * 70)
    print("✅ RSI Strategy Testing Complete!")
    print("=" * 70)
    print()
    print("📚 View interactive docs at: http://localhost:8000/docs")
    print()
