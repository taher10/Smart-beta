# Smart Beta Index Strategy

A factor-based portfolio strategy that dynamically allocates across **Value, Momentum, Growth, Quality, and Size** ETFs using mean-variance optimisation, a turnover penalty, and quarterly rebalancing.  Performance is benchmarked against the S&P 500.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Strategy Details](#strategy-details)
- [Performance Metrics](#performance-metrics)

---

## Overview

This project implements a systematic smart beta strategy inspired by the Fama-French factor model.  At each quarterly rebalance the portfolio weights are solved via **SLSQP mean-variance optimisation** with:

- Per-factor weight floor (10 %) and cap (40 %)
- A 2 % uninvested cash buffer
- A 60 % combined cap on Value + Growth exposure
- A turnover penalty (λ = 0.01) to reduce unnecessary trading
- Flat one-way transaction costs (0.1 %) deducted from daily returns

Market regimes (bull / bear, low-vol / high-vol) are identified with a **Gaussian Mixture Model** and can be used as an optional overlay for regime-conditional tilts.

---

## Project Structure

```
Smart-beta/
├── main.py                  # CLI entry point — runs the full pipeline
├── Smart_beta_index.ipynb   # Interactive notebook (imports from package)
├── requirements.txt         # Python dependencies
└── smart_beta/
    ├── __init__.py          # Public API exports
    ├── config.py            # Config class — all hyperparameters
    ├── data.py              # DataFetcher — Yahoo Finance data retrieval
    ├── regime.py            # RegimeDetector — GMM market-regime detection
    ├── optimizer.py         # PortfolioOptimizer — mean-variance solver
    ├── backtester.py        # Backtester — rolling-window backtest engine
    └── analytics.py         # PerformanceAnalyzer — metrics & charts
```

---

## Installation

**Prerequisites:** Python 3.9 or later.

```bash
# 1. Clone the repository
git clone https://github.com/your-username/Smart-beta.git
cd Smart-beta

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Run the full pipeline from the command line

```bash
python main.py
```

This fetches data, runs the backtest, plots the cumulative performance chart, and prints the metrics table.

### Interactive exploration (Jupyter)

```bash
jupyter lab Smart_beta_index.ipynb
```

The notebook walks through each step — configuration, data fetch, regime detection, backtest, chart, and metrics — one cell at a time.

---

## Configuration

All hyperparameters are centralised in `smart_beta/config.py`.  Change a value there and every downstream component picks it up automatically.

| Parameter | Default | Description |
|---|---|---|
| `START_DATE` | `2018-01-01` | Backtest start date |
| `END_DATE` | `2024-09-30` | Backtest end date |
| `REBALANCE_PERIOD` | `63` | Trading days between rebalances (~quarterly) |
| `MIN_WEIGHT` | `0.10` | Per-factor weight floor |
| `MAX_WEIGHT` | `0.40` | Per-factor weight cap |
| `CASH_BUFFER` | `0.02` | Uninvested cash fraction |
| `VALUE_GROWTH_CAP` | `0.60` | Max combined Value + Growth weight |
| `TURNOVER_PENALTY` | `0.01` | Turnover regularisation lambda |
| `TRANSACTION_COST` | `0.001` | One-way transaction cost per unit of turnover |
| `RISK_FREE_RATE` | `0.02` | Annual risk-free rate (Sharpe / Sortino) |
| `N_REGIMES` | `2` | Number of GMM market regimes |

ETF universe (editable in `Config.ETF_TICKERS`):

| Factor | Ticker | ETF |
|---|---|---|
| Value | VTV | Vanguard Value ETF |
| Momentum | MTUM | iShares MSCI USA Momentum Factor ETF |
| Growth | VUG | Vanguard Growth ETF |
| Quality | QUAL | iShares MSCI USA Quality Factor ETF |
| Size | IJR | iShares Core S&P Small-Cap ETF |

---

## Strategy Details

1. **Data** — Daily adjusted close prices are downloaded from Yahoo Finance via `yfinance`.
2. **Returns** — Daily percentage returns are computed for each factor ETF and the S&P 500 benchmark.
3. **Regime Detection** — A Gaussian Mixture Model classifies each trading day into one of `N_REGIMES` market regimes.
4. **Optimisation** — At every rebalance point, SLSQP maximises the rolling Sharpe ratio subject to weight constraints and a turnover penalty.
5. **Backtest** — Net daily returns are computed by subtracting transaction costs proportional to portfolio turnover.

---

## Performance Metrics

The `PerformanceAnalyzer` computes the following metrics for both the strategy and the S&P 500 benchmark:

| Metric | Description |
|---|---|
| Total Return (%) | Cumulative return over the full backtest period |
| Annualized Return (%) | CAGR assuming 252 trading days per year |
| Volatility (%) | Annualised standard deviation of daily returns |
| Sharpe Ratio | Excess return per unit of total volatility |
| Sortino Ratio | Excess return per unit of downside volatility |
| Max Drawdown (%) | Largest peak-to-trough decline |

