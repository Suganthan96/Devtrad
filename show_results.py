"""
Show exactly what you get from the EMA Crossover API
"""
import requests
import json

url = "http://localhost:8000/backtest/ema-crossover"

# Your request
payload = {
    "market": "INJ/USDT",
    "timeframe": "1h",
    "parameters": {
        "short_period": 9,
        "long_period": 21
    },
    "initial_capital": 1000
}

print("=" * 70)
print("🥷 WHAT YOU GET FROM EMA CROSSOVER BACKTEST")
print("=" * 70)

print("\n📤 YOUR REQUEST:")
print("-" * 70)
print(json.dumps(payload, indent=2))

print("\n📥 WHAT YOU RECEIVE:")
print("-" * 70)

response = requests.post(url, json=payload)
result = response.json()

print(json.dumps(result, indent=2))

print("\n" + "=" * 70)
print("📊 INTERPRETATION:")
print("=" * 70)

results = result["results"]

print(f"\n1️⃣  WIN RATE: {results['win_rate']:.2%}")
print(f"   → {int(results['win_rate'] * results['total_trades'])} winning trades out of {results['total_trades']}")
if results['win_rate'] > 0.5:
    print("   ✅ More winners than losers")
else:
    print("   ❌ More losers than winners")

print(f"\n2️⃣  TOTAL RETURN: {results['total_return']:.2%}")
initial = payload['initial_capital']
final = initial * (1 + results['total_return'])
profit = final - initial
print(f"   → Started with: ${initial:,.2f}")
print(f"   → Ended with:   ${final:,.2f}")
print(f"   → Profit/Loss:  ${profit:,.2f}")
if results['total_return'] > 0:
    print("   ✅ Made money")
else:
    print("   ❌ Lost money")

print(f"\n3️⃣  MAX DRAWDOWN: {results['max_drawdown']:.2%}")
max_loss = initial * results['max_drawdown']
print(f"   → Worst loss from peak: ${max_loss:,.2f}")
if results['max_drawdown'] < 0.1:
    print("   ✅ Low risk")
elif results['max_drawdown'] < 0.2:
    print("   ⚠️  Moderate risk")
else:
    print("   ❌ High risk")

print(f"\n4️⃣  SHARPE RATIO: {results['sharpe_ratio']:.4f}")
if results['sharpe_ratio'] > 1:
    print("   ✅ Good risk-adjusted return")
elif results['sharpe_ratio'] > 0:
    print("   🟡 Positive but low")
else:
    print("   ❌ Negative (losing money)")

print(f"\n5️⃣  TOTAL TRADES: {results['total_trades']}")
if results['total_trades'] > 30:
    print("   ✅ Good sample size")
elif results['total_trades'] > 10:
    print("   🟡 Moderate sample size")
else:
    print("   ⚠️  Small sample (need more data)")

print("\n" + "=" * 70)
print("🎯 FINAL VERDICT:")
print("=" * 70)

if results['total_return'] > 0.05 and results['sharpe_ratio'] > 1.0:
    verdict = "✅ GOOD - Consider using this strategy"
elif results['total_return'] > 0 and results['sharpe_ratio'] > 0:
    verdict = "🟡 OKAY - Needs improvement"
else:
    verdict = "❌ BAD - Don't use these parameters"

print(f"\n{verdict}\n")
print("=" * 70)
