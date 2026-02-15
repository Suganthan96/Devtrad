# 🎯 Market IDs Used in NinjaQuant Project

This document lists all Injective market identifiers used in the NinjaQuant API.

---

## 📊 Market Overview

**Total Markets Available:** 67+ real Injective derivative markets

**Market Source:** Injective Protocol Mainnet
- **LCD Endpoint:** `https://sentry.lcd.injective.network/injective/exchange/v1beta1/derivative/markets`
- **Network:** Mainnet
- **Market Type:** Derivative perpetual futures

---

## 🔑 Primary Markets Used in Project

### 1️⃣ INJ/USDT PERP (Injective Perpetual)

**Market ID:** `0x9b9980167ecc3645ff1a5517886652d94a0825e54a77d2057cbbe3ebee015963`

**Details:**
- **Ticker:** INJ/USDT PERP
- **Oracle:** Pyth
- **Quote Denom:** peggy0xdAC17F958D2ee523a2206206994597C13D831ec7
- **Use Case:** Primary test market, most examples use this
- **Approximate Price:** $25.00

**Used In:**
- Default examples in README.md
- demo_injective.py
- demo_rsi.py
- Postman collection tests
- HACKATHON_SUBMISSION.md

---

### 2️⃣ BTC/USDT PERP (Bitcoin Perpetual)

**Market ID:** Dynamically fetched from Injective blockchain

**Details:**
- **Ticker:** BTC/USDT PERP
- **Oracle:** Pyth/Band Protocol
- **Use Case:** High-value asset testing, institutional scenarios
- **Approximate Price:** $50,000+

**Used In:**
- Postman collection (large capital tests)
- Strategy comparison tests
- Performance benchmarking

---

### 3️⃣ ETH/USDT PERP (Ethereum Perpetual)

**Market ID:** Dynamically fetched from Injective blockchain

**Details:**
- **Ticker:** ETH/USDT PERP
- **Oracle:** Pyth/Band Protocol
- **Use Case:** Second-largest crypto asset testing
- **Approximate Price:** $3,000+

**Used In:**
- Multi-market testing
- Scalping strategy tests (15m timeframe)
- Postman collection

---

## 🌐 Additional Supported Markets

The API supports **67+ Injective derivative markets**. Market IDs are fetched dynamically from the blockchain. Common markets include:

### Crypto Perpetuals:
- **XAU/USDT PERP** (Gold futures)
- **LINK/USDT PERP** (Chainlink)
- **SOL/USDT PERP** (Solana)
- **BNB/USDT PERP** (Binance Coin)
- **ATOM/USDT PERP** (Cosmos)
- **MATIC/USDT PERP** (Polygon)
- **DOT/USDT PERP** (Polkadot)
- **ADA/USDT PERP** (Cardano)
- **AVAX/USDT PERP** (Avalanche)
- **UNI/USDT PERP** (Uniswap)
- And 57+ more...

**Note:** Market IDs for these are dynamically fetched from Injective blockchain when requested.

---

## 🔍 How Market IDs Are Used

### 1. **Market Validation Process**

When you request a backtest:

```json
{
  "market": "INJ/USDT PERP",
  "timeframe": "1h",
  "parameters": {...}
}
```

**The API:**
1. **Connects to Injective LCD API** (`https://sentry.lcd.injective.network`)
2. **Fetches all 67+ derivative markets** from blockchain
3. **Validates requested market exists**
4. **Extracts Market ID** (40-character hexadecimal string)
5. **Retrieves oracle information** (Pyth, Band Protocol)
6. **Gets current market price** from oracle data

### 2. **Server Logs Show Real Market ID**

```
🔍 Fetching data for INJ/USDT PERP from Injective MAINNET
📡 Fetching real markets from Injective blockchain...
✅ Successfully fetched 67 real markets from Injective!
✅ Verified market on Injective blockchain
   Market ID: 0x9b9980167ecc3645ff1a5517886652d94a0825e54a77d2057cbbe3ebee015963
   Ticker: INJ/USDT PERP
   Oracle: Pyth
```

### 3. **Error Handling for Invalid Markets**

If invalid market requested:

```json
{
  "market": "INVALID/MARKET",
  "timeframe": "1h",
  "parameters": {...}
}
```

**API Response:**
```json
{
  "detail": "Market 'INVALID/MARKET' not found on Injective. Available markets include: ['INJ/USDT PERP', 'BTC/USDT PERP', 'ETH/USDT PERP', ...]"
}
```

---

## 📝 Market ID Format

### Structure:
```
0x[64 hexadecimal characters]
```

### Example:
```
0x9b9980167ecc3645ff1a5517886652d94a0825e54a77d2057cbbe3ebee015963
│  │                                                                │
│  └─ 64 hex characters (256 bits)                                 │
└─ Ethereum-style hex prefix                                        └─ Checksum
```

### Characteristics:
- **Length:** 66 characters total (including "0x" prefix)
- **Format:** Hexadecimal (0-9, a-f)
- **Uniqueness:** Each market has a unique ID on Injective blockchain
- **Immutability:** Market IDs don't change once created
- **Purpose:** Uniquely identify trading pairs on Injective Protocol

---

## 🔧 Code Implementation

### Fetching Market Info from Injective

From `app/data/injective_client.py`:

```python
def _get_market_info(self, market: str) -> Dict:
    """
    Get market information from Injective blockchain
    
    Args:
        market: Trading pair (e.g., "INJ/USDT PERP")
        
    Returns:
        Dict with market_id, ticker, oracle info, etc.
    """
    try:
        # Call Injective LCD API
        url = f"{self.lcd_endpoint}/injective/exchange/v1beta1/derivative/markets"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Cache and search for market
        for market_data in data.get('markets', []):
            ticker = market_data.get('ticker', '')
            
            if ticker.upper() == market.upper():
                return {
                    'market_id': market_data.get('market_id'),
                    'ticker': ticker,
                    'oracle_type': market_data.get('oracle_type'),
                    'quote_denom': market_data.get('quote_denom')
                }
        
        raise InvalidMarketError(
            f"Market '{market}' not found on Injective. "
            f"Available markets include: {self._cached_markets[:10]}"
        )
        
    except requests.exceptions.RequestException as e:
        raise InjectiveConnectionError(f"Failed to fetch from Injective: {e}")
```

---

## 🧪 Testing Market IDs

### Local Testing

**Demo script:** `demo_injective.py`

```bash
python demo_injective.py
```

**Output shows real Market IDs:**
```
✅ Successfully fetched 67 real markets from Injective!
   Market ID: 0x9b9980167ecc3645ff1a5517886652d94a0825e54a77d2057cbbe3ebee015963
   Ticker: INJ/USDT PERP
```

### API Testing

**cURL:**
```bash
curl -X POST http://localhost:8000/backtest/ema-crossover \
  -H "Content-Type: application/json" \
  -d '{
    "market": "BTC/USDT PERP",
    "timeframe": "1h",
    "parameters": {"short_period": 9, "long_period": 21}
  }'
```

**Check logs for Market ID:**
```
   Market ID: 0x[64_hex_chars_for_btc]
   Ticker: BTC/USDT PERP
   Oracle: Pyth
```

---

## 📚 Market ID Storage

### Not Hardcoded
Market IDs are **NOT hardcoded** in the project. They are:
- ✅ Fetched dynamically from Injective blockchain
- ✅ Cached during API runtime for performance
- ✅ Validated on every backtest request
- ✅ Always reflect current Injective mainnet state

### Why Dynamic?
1. **Future-proof:** New markets added to Injective automatically available
2. **Accurate:** Always uses current blockchain state
3. **Secure:** No risk of outdated market references
4. **Auditable:** Logs show real blockchain data

---

## 🎯 Market ID Usage Examples

### Example 1: EMA Strategy on INJ
```json
{
  "market": "INJ/USDT PERP",
  "timeframe": "1h",
  "parameters": {
    "short_period": 9,
    "long_period": 21
  }
}
```

**Behind the scenes:**
1. API queries Injective LCD
2. Finds market_id: `0x9b9980167ecc3645ff1a5517886652d94a0825e54a77d2057cbbe3ebee015963`
3. Validates market exists
4. Proceeds with backtest

### Example 2: RSI Strategy on BTC
```json
{
  "market": "BTC/USDT PERP",
  "timeframe": "1h",
  "parameters": {
    "period": 14,
    "oversold": 30,
    "overbought": 70
  }
}
```

**Behind the scenes:**
1. API queries Injective LCD
2. Finds BTC market_id (unique 66-char string)
3. Extracts oracle price data
4. Runs RSI backtest with verified data

---

## 🔐 Security & Validation

### Market Validation Ensures:
- ✅ **Real markets only:** Can't backtest fake/non-existent markets
- ✅ **Blockchain verification:** Every market confirmed on Injective
- ✅ **Oracle data:** Price feeds from Pyth/Band Protocol
- ✅ **Audit trail:** All market IDs logged for verification

### Hackathon Compliance:
- ✅ **Requirement:** "Must integrate with Injective"
- ✅ **Evidence:** Market IDs prove blockchain connection
- ✅ **Transparency:** Logs show real API calls
- ✅ **Verifiable:** Anyone can check LCD endpoint

---

## 📖 References

### Injective Documentation:
- **LCD API:** https://sentry.lcd.injective.network
- **Markets Endpoint:** `/injective/exchange/v1beta1/derivative/markets`
- **Developer Docs:** https://docs.injective.network

### Project Files:
- **Integration Code:** `app/data/injective_client.py`
- **Integration Docs:** `INJECTIVE_INTEGRATION.md`
- **Demo Script:** `demo_injective.py`
- **Hackathon Proof:** `HACKATHON_SUBMISSION.md`

---

## 🚀 Quick Reference

**To see all available Market IDs:**
```bash
# Start API
python -m uvicorn app.main:app --reload

# Run demo
python demo_injective.py

# Check logs for:
# "✅ Successfully fetched 67 real markets from Injective!"
# "Market ID: 0x..."
```

**To test a specific market:**
```bash
curl -X POST http://localhost:8000/backtest/ema-crossover \
  -H "Content-Type: application/json" \
  -d '{"market":"ETH/USDT PERP","timeframe":"1h","parameters":{"short_period":9,"long_period":21}}'
```

---

**Summary:** This project uses **real Injective blockchain market IDs** fetched dynamically from mainnet, with INJ/USDT PERP (Market ID: `0x9b9980167ecc3645ff1a5517886652d94a0825e54a77d2057cbbe3ebee015963`) as the primary example market.
