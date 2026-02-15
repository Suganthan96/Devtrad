"""
Verify Real Market IDs for BTC, ETH, and INJ from Injective Blockchain
"""
import requests
import json

print("=" * 80)
print("🔍 VERIFYING MARKET IDs FROM INJECTIVE BLOCKCHAIN")
print("=" * 80)
print()

# The actual Injective LCD endpoint used in the project
INJECTIVE_LCD_URL = "https://sentry.lcd.injective.network/injective/exchange/v1beta1/derivative/markets"

# Expected Market IDs (from Injective Explorer screenshots)
EXPECTED_MARKET_IDS = {
    'BTC/USDT PERP': '0x4ca0f92fc28be0c9761326016b5a1a2177dd6375558365116b5bdda9abc229ce',
    'ETH/USDT PERP': '0x54d4505adef6a5cef26bc403a33d595620ded4e15b9e2bc3dd489b714813366a',
    'INJ/USDT PERP': '0x9b9980167ecc3645ff1a5517886652d94a0825e54a77d2057cbbe3ebee015963'
}

print("📡 Fetching live market data from Injective...")
print(f"   URL: {INJECTIVE_LCD_URL}")
print()

try:
    response = requests.get(INJECTIVE_LCD_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    markets = data.get('markets', [])
    print(f"✅ Successfully fetched {len(markets)} markets from Injective blockchain")
    print()
    
    print("=" * 80)
    print("🎯 VERIFYING MARKET IDs")
    print("=" * 80)
    print()
    
    verified_count = 0
    
    for ticker, expected_id in EXPECTED_MARKET_IDS.items():
        print(f"🔎 Searching for {ticker}...")
        
        found = False
        for market_wrapper in markets:
            market = market_wrapper.get('market', {})
            
            if market.get('ticker') == ticker:
                found = True
                actual_id = market.get('market_id')
                oracle_type = market.get('oracle_type')
                oracle_base = market.get('oracle_base')
                
                print(f"   ✅ FOUND on blockchain!")
                print(f"   Market ID: {actual_id}")
                print(f"   Oracle: {oracle_type}")
                print(f"   Oracle Base: {oracle_base}")
                
                # Verify the Market ID matches
                if actual_id == expected_id:
                    print(f"   ✅ VERIFIED: Market ID matches expected value!")
                    verified_count += 1
                else:
                    print(f"   ⚠️  WARNING: Market ID doesn't match!")
                    print(f"      Expected: {expected_id}")
                    print(f"      Got:      {actual_id}")
                
                print()
                break
        
        if not found:
            print(f"   ❌ NOT FOUND on blockchain")
            print()
    
    print("=" * 80)
    print(f"✅ VERIFICATION COMPLETE: {verified_count}/{len(EXPECTED_MARKET_IDS)} Market IDs verified")
    print("=" * 80)
    print()
    
    if verified_count == len(EXPECTED_MARKET_IDS):
        print("🎉 SUCCESS: All Market IDs are REAL and match Injective blockchain!")
        print()
        print("These are the EXACT Market IDs used in the NinjaQuant project:")
        for ticker, market_id in EXPECTED_MARKET_IDS.items():
            print(f"  • {ticker}: {market_id}")
        print()
    else:
        print("⚠️  Some Market IDs could not be verified")
        print()
    
    print("🔗 You can verify these on Injective Explorer:")
    print("   https://explorer.injective.network/markets/")
    print()
    
except requests.exceptions.RequestException as e:
    print(f"❌ Error fetching from Injective: {e}")
    print()

print("=" * 80)
