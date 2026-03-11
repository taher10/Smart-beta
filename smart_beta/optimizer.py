"""Mean-variance portfolio optimiser with turnover penalty and concentration limits."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from .config import Config


class PortfolioOptimizer:
    """Mean-variance optimiser with turnover penalty and concentration limits.

    Maximises the portfolio Sharpe ratio while penalising excessive turnover
    and enforcing per-factor floors/caps plus a Value + Growth concentration
    cap.

    Parameters
    ----------
    cfg : Config
        Strategy configuration object that supplies all constraint values.
    """

    def __init__(self, cfg: Config):
        self.cfg = cfg

    def optimize(
        self,
        expected_returns: pd.Series,
        cov_matrix: pd.DataFrame,
        prev_weights: np.ndarray,
    ) -> np.ndarray:
        """Solve for optimal factor weights.

        Parameters
        ----------
        expected_returns : pd.Series
            Per-factor expected daily returns for the look-back window.
        cov_matrix : pd.DataFrame
            Sample covariance matrix for the same window.
        prev_weights : np.ndarray
            Previous period's weights used to compute turnover cost.

        Returns
        -------
        np.ndarray
            Optimal weight vector (sums to ``1 - CASH_BUFFER``).
        """
        n          = len(expected_returns)
        target     = 1.0 - self.cfg.CASH_BUFFER
        cov_values = cov_matrix.values

        def objective(w: np.ndarray) -> float:
            ret      = np.dot(w, expected_returns)
            vol      = np.sqrt(w @ cov_values @ w)
            turnover = np.sum(np.abs(w - prev_weights))
            return -(ret / vol) + self.cfg.TURNOVER_PENALTY * turnover

        # Indices follow ETF_TICKERS insertion order: Value=0, Growth=2
        constraints = [
            {"type": "eq",   "fun": lambda w: np.sum(w) - target},
            {"type": "ineq", "fun": lambda w: self.cfg.VALUE_GROWTH_CAP - (w[0] + w[2])},
        ]
        bounds     = [(self.cfg.MIN_WEIGHT, self.cfg.MAX_WEIGHT)] * n
        init_guess = np.full(n, target / n)

        result = minimize(
            objective,
            init_guess,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )
        return result.x
