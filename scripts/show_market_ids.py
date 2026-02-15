"""Display the hardcoded Injective Market IDs used by the API"""
from app.data.injective_client import INJECTIVE_MARKETS

print("\n" + "="*70)
print("INJECTIVE MARKET IDs (Hardcoded)")
print("="*70)
print("\nThese Market IDs are used directly without dynamic API fetching:\n")

for ticker, info in INJECTIVE_MARKETS.items():
    print(f"📊 {ticker}")
    print(f"   Market ID: {info['market_id']}")
    print(f"   Oracle:    {info['oracle_type']}")
    print(f"   Base:      {info['oracle_base']}")
    print()

print("="*70)
print(f"Total Markets: {len(INJECTIVE_MARKETS)}")
print("="*70)
print("\n✅ All Market IDs are hardcoded for fast, reliable access")
print("🔗 Verify on Injective Explorer: https://explorer.injective.network/\n")
