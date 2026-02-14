"""Injective network data client for real market data"""
import pandas as pd
import requests
from typing import Optional
import logging
from ..core.exceptions import InjectiveConnectionError, InvalidMarketError, InsufficientDataError

logger = logging.getLogger(__name__)


class InjectiveDataClient:
    """Client for fetching real historical data from Injective network"""
    
    def __init__(self, network: str = "mainnet"):
        """
        Initialize Injective data client
        
        Args:
            network: "mainnet" or "testnet"
        """
        self.network = network
        if network == "mainnet":
            self.base_url = "https://api.injective.network"
        elif network == "testnet":
            self.base_url = "https://testnet.api.injective.network"
        else:
            raise ValueError(f"Unknown network: {network}")
        
        self._market_cache = None
        logger.info(f"Initialized InjectiveDataClient for {network}")
    
    def fetch_historical_candles(
        self, 
        market: str, 
        timeframe: str, 
        limit: int = 500
    ) -> pd.DataFrame:
        """
        Fetch historical OHLCV candles from Injective
        
        Args:
            market: Trading pair (e.g., "INJ/USDT")
            timeframe: Candle interval (1m, 5m, 15m, 1h, 4h, 1d)
            limit: Number of candles to fetch (default: 500)
            
        Returns:
            DataFrame with columns: timestamp, open, high, low, close, volume
            
        Raises:
            InjectiveConnectionError: If connection fails
            InvalidMarketError: If market is not found
            InsufficientDataError: If not enough data available
        """
        try:
            # Step 1: Get market ID from symbol
            market_id = self._get_market_id(market)
            
            # Step 2: Map timeframe to Injective resolution
            resolution = self._map_timeframe_to_resolution(timeframe)
            
            # Step 3: Fetch candles from Injective API
            candles_url = f"{self.base_url}/api/explorer/v1/derivative_market/{market_id}/candles"
            
            params = {
                'resolution': resolution,
                'limit': limit
            }
            
            logger.info(f"Fetching {limit} candles for {market} ({timeframe})")
            response = requests.get(candles_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Step 4: Convert to DataFrame
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
            
            if len(candles) == 0:
                raise InsufficientDataError(f"No candle data available for {market}")
            
            df = pd.DataFrame(candles)
            df = df.sort_values('timestamp').reset_index(drop=True)
            
            logger.info(f"Successfully fetched {len(df)} candles for {market}")
            return df
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Injective API connection error: {e}")
            raise InjectiveConnectionError(f"Failed to connect to Injective API: {str(e)}")
        except KeyError as e:
            logger.error(f"Unexpected API response format: {e}")
            raise InjectiveConnectionError(f"Invalid API response format: {str(e)}")
    
    def _get_market_id(self, market: str) -> str:
        """
        Map market symbol to Injective market ID
        
        Args:
            market: Trading pair (e.g., "INJ/USDT")
            
        Returns:
            Injective market ID
            
        Raises:
            InvalidMarketError: If market not found
        """
        try:
            # Fetch available markets (with caching)
            if self._market_cache is None:
                markets_url = f"{self.base_url}/api/explorer/v1/derivative_markets"
                response = requests.get(markets_url, timeout=10)
                response.raise_for_status()
                self._market_cache = response.json()
            
            # Search for market by ticker
            for m in self._market_cache.get('markets', []):
                if m.get('ticker') == market:
                    return m.get('market_id')
            
            # Market not found
            available = [m.get('ticker') for m in self._market_cache.get('markets', [])]
            raise InvalidMarketError(
                f"Market '{market}' not found. Available markets: {', '.join(available[:10])}..."
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch market list: {e}")
            raise InjectiveConnectionError(f"Failed to fetch market list: {str(e)}")
    
    def _map_timeframe_to_resolution(self, timeframe: str) -> str:
        """
        Map API timeframe string to Injective resolution
        
        Args:
            timeframe: API timeframe (1m, 5m, 15m, 1h, 4h, 1d)
            
        Returns:
            Injective resolution string
        """
        # Injective uses similar format, so pass through
        # In future, might need more complex mapping
        return timeframe
    
    def get_available_markets(self) -> list:
        """
        Get list of all available markets on Injective
        
        Returns:
            List of market tickers
        """
        try:
            markets_url = f"{self.base_url}/api/explorer/v1/derivative_markets"
            response = requests.get(markets_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return [m.get('ticker') for m in data.get('markets', [])]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch markets: {e}")
            raise InjectiveConnectionError(f"Failed to fetch markets: {str(e)}")
