"""Custom exception classes for NinjaQuant"""


class NinjaQuantException(Exception):
    """Base exception for all NinjaQuant errors"""
    pass


class InjectiveConnectionError(NinjaQuantException):
    """Raised when connection to Injective network fails"""
    pass


class InvalidMarketError(NinjaQuantException):
    """Raised when market symbol is not found or invalid"""
    pass


class InsufficientDataError(NinjaQuantException):
    """Raised when insufficient historical data is available"""
    pass


class StrategyExecutionError(NinjaQuantException):
    """Raised when strategy execution fails"""
    pass
