"""Rolling-window backtest engine with periodic rebalancing."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .config import Config
from .optimizer import PortfolioOptimizer


class Backtester:
    """Runs a rolling-window backtest with periodic rebalancing.

    At every ``REBALANCE_PERIOD`` trading days, new optimal weights are
    computed on the in-sample window.  Daily net returns subtract a
    flat transaction-cost estimate proportional to portfolio turnover.

    Parameters
    ----------
    optimizer : PortfolioOptimizer
        Optimiser instance used to compute weights at each rebalance.
    cfg : Config
        Strategy configuration object.
    """

    def __init__(self, optimizer: PortfolioOptimizer, cfg: Config):
        self.optimizer = optimizer
        self.cfg       = cfg

    def run(
        self, returns: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.Series]:
        """Execute the full backtest.

        Parameters
        ----------
        returns : pd.DataFrame
            Daily factor returns (dates × factors).

        Returns
        -------
        weights_df : pd.DataFrame
            Daily factor weight allocation (same index as ``returns``).
        portfolio_returns : pd.Series
            Daily net strategy returns (same index as ``returns``).
        """
        n_assets  = returns.shape[1]
        n_periods = len(returns)
        target    = 1.0 - self.cfg.CASH_BUFFER

        all_weights       = np.zeros((n_periods, n_assets))
        portfolio_returns = np.zeros(n_periods)
        prev_weights      = np.full(n_assets, target / n_assets)

        for t in range(0, n_periods, self.cfg.REBALANCE_PERIOD):
            window  = returns.iloc[t : t + self.cfg.REBALANCE_PERIOD]
            opt_w   = self.optimizer.optimize(window.mean(), window.cov(), prev_weights)
            end_idx = min(t + self.cfg.REBALANCE_PERIOD, n_periods)

            all_weights[t:end_idx] = opt_w

            # Transaction cost is a one-off charge on the rebalance day only.
            # Both opt_w and prev_weights are constant within the window so
            # applying tc inside the day-loop would multiply it by ~63×.
            rebalance_cost = self.cfg.TRANSACTION_COST * np.sum(np.abs(opt_w - prev_weights))

            window_returns = returns.iloc[t:end_idx].values @ opt_w  # vectorised daily gross returns
            window_returns[0] -= rebalance_cost                       # deduct cost once on day t
            portfolio_returns[t:end_idx] = window_returns

            prev_weights = opt_w

        weights_df = pd.DataFrame(all_weights, index=returns.index, columns=returns.columns)
        returns_s  = pd.Series(portfolio_returns, index=returns.index, name="Strategy")
        return weights_df, returns_s
