"""Trading strategy modules"""
from .base import Strategy
from .ema_crossover import EMAStrategy

__all__ = [
    "Strategy",
    "EMAStrategy"
]
