"""Risk/return metrics computation and performance visualisation."""

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class PerformanceAnalyzer:
    """Computes risk/return metrics and generates comparison visualisations.

    Parameters
    ----------
    risk_free_rate : float
        Annual risk-free rate used in Sharpe and Sortino ratio computation.
    """

    def __init__(self, risk_free_rate: float = 0.02):
        self.risk_free_rate = risk_free_rate

    # ── Private helpers ───────────────────────────────────────────────────────

    def _compute_metrics(self, returns: np.ndarray) -> dict:
        """Compute a standard set of risk/return metrics for a return stream."""
        cum     = np.cumprod(1 + returns)
        ann_ret = cum[-1] ** (252 / len(returns)) - 1
        vol     = np.std(returns) * np.sqrt(252)
        sharpe  = (ann_ret - self.risk_free_rate) / vol if vol else np.nan

        peaks  = np.maximum.accumulate(cum)
        max_dd = ((cum / peaks) - 1).min()

        downside = returns[returns < 0]
        dd_vol   = np.std(downside) * np.sqrt(252) if len(downside) else np.nan
        sortino  = (ann_ret - self.risk_free_rate) / dd_vol if dd_vol else np.nan

        return {
            "Total Return (%)":      round((cum[-1] - 1) * 100, 2),
            "Annualized Return (%)": round(ann_ret * 100,        2),
            "Volatility (%)":        round(vol * 100,            2),
            "Sharpe Ratio":          round(sharpe,               3),
            "Sortino Ratio":         round(sortino,              3),
            "Max Drawdown (%)":      round(max_dd * 100,         2),
        }

    def _align(
        self, portfolio: pd.Series, benchmark: pd.Series
    ) -> tuple[pd.Series, pd.Series]:
        """Return portfolio and benchmark aligned on a shared date index."""
        bench = benchmark.reindex(portfolio.index).dropna()
        port  = portfolio.reindex(bench.index)
        return port, bench

    # ── Public API ────────────────────────────────────────────────────────────

    def summary_table(
        self,
        portfolio_returns: pd.Series,
        benchmark_returns: pd.Series,
    ) -> pd.DataFrame:
        """Return a side-by-side metrics DataFrame.

        Parameters
        ----------
        portfolio_returns : pd.Series
            Daily strategy net returns.
        benchmark_returns : pd.Series
            Daily benchmark returns.

        Returns
        -------
        pd.DataFrame
            One column per series, one row per metric.
        """
        port, bench = self._align(portfolio_returns, benchmark_returns)
        return pd.DataFrame({
            "Smart Beta Strategy": self._compute_metrics(port.values),
            "S&P 500 Benchmark":   self._compute_metrics(bench.values),
        })

    def plot_cumulative(
        self,
        portfolio_returns: pd.Series,
        benchmark_returns: pd.Series,
        base: float = 100.0,
        save_path: str | None = None,
    ) -> None:
        """Plot growth of ``base`` dollars invested at strategy inception.

        Parameters
        ----------
        portfolio_returns : pd.Series
            Daily strategy net returns.
        benchmark_returns : pd.Series
            Daily benchmark returns.
        base : float
            Starting investment value (default ``$100``).
        save_path : str or None
            If provided, the chart is saved to this file path and no
            interactive window is opened.  Useful when running from a
            terminal where ``plt.show()`` would block.
        """
        port, bench = self._align(portfolio_returns, benchmark_returns)

        port_curve  = base * np.cumprod(1 + port)
        bench_curve = base * np.cumprod(1 + bench)

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(port_curve,  label=f"Smart Beta Strategy  (${base:.0f} start)", linewidth=1.8)
        ax.plot(bench_curve, label=f"S&P 500 Benchmark    (${base:.0f} start)", linestyle="--", alpha=0.85)
        ax.set_title("Portfolio Performance vs. S&P 500", fontsize=14, fontweight="bold")
        ax.set_xlabel("Date")
        ax.set_ylabel("Portfolio Value ($)")
        ax.legend()
        ax.grid(alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        fig.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches="tight")
            plt.close(fig)
        else:
            plt.show()
