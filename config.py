"""Configuration settings for NinjaQuant API"""
import os
from typing import Literal


class Settings:
    """Application settings"""
    
    # API Configuration
    APP_TITLE: str = "NinjaQuant API"
    APP_DESCRIPTION: str = "Developer-first backtesting API built on Injective's historical market data"
    APP_VERSION: str = "1.0.0"
    
    # Injective Network Configuration
    INJECTIVE_NETWORK: Literal["mainnet", "testnet"] = os.getenv("INJECTIVE_NETWORK", "mainnet")
    
    # Data Client Configuration
    USE_REAL_DATA: bool = os.getenv("USE_REAL_DATA", "false").lower() == "true"
    DATA_FETCH_TIMEOUT: int = int(os.getenv("DATA_FETCH_TIMEOUT", "10"))
    DEFAULT_CANDLE_LIMIT: int = 500
    
    # CORS Configuration
    CORS_ORIGINS: list = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
