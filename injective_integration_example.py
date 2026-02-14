"""
Example: How to integrate real Injective market data

This shows how to replace the synthetic data with real Injective historical data.
"""

import pandas as pd
from pyinjective.async_client import AsyncClient
from pyinjective.core.network import Network
import asyncio


async def fetch_injective_market_data(market: str, timeframe: str) -> pd.DataFrame:
    """
    Fetch REAL historical OHLCV data from Injective
    
    This is how you would integrate with Injective in production.
    
    Args:
        market: Trading pair (e.g., "INJ/USDT")
        timeframe: Candle interval (e.g., "1h", "4h", "1d")
    
    Returns:
        DataFrame with columns: timestamp, open, high, low, close, volume
    """
    
    # Initialize Injective client
    network = Network.mainnet()  # or Network.testnet() for testing
    client = AsyncClient(network)
    
    # Map market string to Injective market ID
    # You would need to query available markets first
    market_id = get_market_id(market)
    
    # Map timeframe to resolution
    resolution_map = {
        "1m": 60,
        "5m": 300,
        "15m": 900,
        "1h": 3600,
        "4h": 14400,
        "1d": 86400
    }
    resolution = resolution_map.get(timeframe, 3600)
    
    # Fetch historical candles
    # This gets the last 500 candles
    candles = await client.get_historical_derivative_market_candles(
        market_id=market_id,
        resolution=resolution,
        limit=500
    )
    
    # Convert to DataFrame
    data = []
    for candle in candles:
        data.append({
            'timestamp': pd.to_datetime(candle.time, unit='ms'),
            'open': float(candle.open),
            'high': float(candle.high),
            'low': float(candle.low),
            'close': float(candle.close),
            'volume': float(candle.volume)
        })
    
    df = pd.DataFrame(data)
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    await client.close()
    
    return df


def get_market_id(market: str) -> str:
    """
    Map market symbol to Injective market ID
    
    In production, you would query the Injective API for available markets
    and cache this mapping.
    """
    # Example mapping (you'd get this from Injective API)
    market_map = {
        "INJ/USDT": "0x...",  # Actual market ID from Injective
        "BTC/USDT": "0x...",
        # Add more markets
    }
    
    return market_map.get(market, "")


# Synchronous wrapper for use in FastAPI
def fetch_market_data_sync(market: str, timeframe: str) -> pd.DataFrame:
    """
    Synchronous wrapper to use in FastAPI endpoints
    """
    return asyncio.run(fetch_injective_market_data(market, timeframe))


# ============================================================================
# ALTERNATIVE: Using REST API (simpler, no async needed)
# ============================================================================

import requests

def fetch_injective_data_rest(market: str, timeframe: str) -> pd.DataFrame:
    """
    Fetch Injective data using REST API (simpler approach)
    
    This is easier to integrate into FastAPI without async complexity.
    """
    
    # Injective API endpoint
    base_url = "https://api.injective.network"
    
    # Get market ID first
    markets_response = requests.get(f"{base_url}/api/explorer/v1/derivative_markets")
    markets = markets_response.json()
    
    # Find the market ID for your trading pair
    market_id = None
    for m in markets.get('markets', []):
        if m.get('ticker') == market:
            market_id = m.get('market_id')
            break
    
    if not market_id:
        raise ValueError(f"Market {market} not found")
    
    # Fetch historical candles
    candles_url = f"{base_url}/api/explorer/v1/derivative_market/{market_id}/candles"
    
    params = {
        'resolution': timeframe,
        'limit': 500
    }
    
    response = requests.get(candles_url, params=params)
    data = response.json()
    
    # Convert to DataFrame
    candles = []
    for candle in data.get('candles', []):
        candles.append({
            'timestamp': pd.to_datetime(int(candle['time']), unit='ms'),
            'open': float(candle['open']),
            'high': float(candle['high']),
            'low': float(candle['low']),
            'close': float(candle['close']),
            'volume': float(candle['volume'])
        })
    
    df = pd.DataFrame(candles)
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    return df


# ============================================================================
# HOW TO USE IN main.py
# ============================================================================

"""
Replace the fetch_market_data() function in main.py with:

def fetch_market_data(market: str, timeframe: str) -> pd.DataFrame:
    '''
    Fetch historical OHLCV data from Injective
    '''
    try:
        # Use real Injective data
        df = fetch_injective_data_rest(market, timeframe)
        return df
    except Exception as e:
        # Fallback to synthetic data if API fails
        print(f"Warning: Using synthetic data. Injective API error: {e}")
        return generate_synthetic_data()

def generate_synthetic_data() -> pd.DataFrame:
    '''Fallback synthetic data for demo'''
    np.random.seed(42)
    num_candles = 500
    base_price = 10.0
    returns = np.random.randn(num_candles) * 0.02
    prices = base_price * np.exp(np.cumsum(returns))
    
    df = pd.DataFrame({
        'timestamp': pd.date_range(start='2024-01-01', periods=num_candles, freq='1h'),
        'close': prices
    })
    return df
"""
