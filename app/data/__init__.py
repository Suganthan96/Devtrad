"""Data fetching modules"""
from .injective_client import InjectiveDataClient
from .synthetic_client import SyntheticDataClient

__all__ = [
    "InjectiveDataClient",
    "SyntheticDataClient"
]
