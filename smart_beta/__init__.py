"""
smart_beta
==========
Factor-based smart beta portfolio strategy package.

Public API
----------
    Config               – All hyperparameters and ticker universe
    DataFetcher          – Yahoo Finance data retrieval
    RegimeDetector       – GMM market-regime detection
    PortfolioOptimizer   – Mean-variance optimiser with constraints
    Backtester           – Rolling-window backtest engine
    PerformanceAnalyzer  – Metrics computation and visualisation
"""

from .config import Config
from .data import DataFetcher
from .regime import RegimeDetector
from .optimizer import PortfolioOptimizer
from .backtester import Backtester
from .analytics import PerformanceAnalyzer

__all__ = [
    "Config",
    "DataFetcher",
    "RegimeDetector",
    "PortfolioOptimizer",
    "Backtester",
    "PerformanceAnalyzer",
]
