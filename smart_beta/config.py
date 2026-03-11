"""Central, version-controlled configuration for the Smart Beta strategy.

All hyperparameters live here so every experiment can be tracked and
reproduced simply by changing this class or subclassing it.
"""


class Config:
    """Strategy hyperparameters, ticker universe, and date range.

    Attributes
    ----------
    ETF_TICKERS : dict
        Mapping of factor name → Yahoo Finance ticker symbol.
    BENCHMARK_TICKER : str
        Ticker for the benchmark index (default S&P 500).
    START_DATE / END_DATE : str
        Backtest window in ``YYYY-MM-DD`` format.
    MIN_WEIGHT / MAX_WEIGHT : float
        Per-factor weight floor / cap enforced by the optimiser.
    CASH_BUFFER : float
        Fraction of the portfolio kept in cash (not invested).
    VALUE_GROWTH_CAP : float
        Maximum combined weight allowed for Value + Growth factors.
    REBALANCE_PERIOD : int
        Number of trading days between portfolio rebalances.
    TURNOVER_PENALTY : float
        Lambda (λ) applied to turnover in the optimisation objective.
    TRANSACTION_COST : float
        One-way flat transaction cost per unit of turnover.
    RISK_FREE_RATE : float
        Annual risk-free rate used in Sharpe / Sortino computation.
    N_REGIMES : int
        Number of GMM components for market-regime detection.
    """

    # ── Universe ──────────────────────────────────────────────────────────────
    ETF_TICKERS: dict = {
        "Value":    "VTV",   # Vanguard Value ETF
        "Momentum": "MTUM",  # iShares MSCI USA Momentum Factor ETF
        "Growth":   "VUG",   # Vanguard Growth ETF
        "Quality":  "QUAL",  # iShares MSCI USA Quality Factor ETF
        "Size":     "IJR",   # iShares Core S&P Small-Cap ETF
    }
    BENCHMARK_TICKER: str = "^GSPC"

    # ── Backtest period ───────────────────────────────────────────────────────
    START_DATE: str = "2018-01-01"
    END_DATE:   str = "2024-09-30"

    # ── Portfolio constraints ─────────────────────────────────────────────────
    MIN_WEIGHT:       float = 0.10   # Floor per factor
    MAX_WEIGHT:       float = 0.40   # Cap per factor
    CASH_BUFFER:      float = 0.02   # Uninvested cash reserve
    VALUE_GROWTH_CAP: float = 0.60   # Max combined Value + Growth exposure

    # ── Rebalancing ───────────────────────────────────────────────────────────
    REBALANCE_PERIOD: int   = 63     # Trading days (~quarterly)
    TURNOVER_PENALTY: float = 0.01   # Lambda for turnover regularisation
    TRANSACTION_COST: float = 0.001  # One-way transaction cost (bps * 10)

    # ── Risk model ────────────────────────────────────────────────────────────
    RISK_FREE_RATE: float = 0.02  # Annual risk-free rate
    N_REGIMES:      int   = 2     # Number of market regimes (GMM)
