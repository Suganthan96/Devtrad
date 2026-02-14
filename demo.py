import requests
import json

# Test EMA Crossover endpoint
url = "http://localhost:8000/backtest/ema-crossover"

payload = {
    "market": "INJ/USDT",
    "timeframe": "1h",
    "parameters": {
        "short_period": 9,
        "long_period": 21
    },
    "initial_capital": 1000
}

print("🥷 NinjaQuant - EMA Crossover Backtest")
print("=" * 60)
print("\nRequest:")
print(json.dumps(payload, indent=2))

response = requests.post(url, json=payload)

print("\n" + "=" * 60)
print("Response:")
print("=" * 60)
print(json.dumps(response.json(), indent=2))
print("\n✅ Backtest completed successfully!")
