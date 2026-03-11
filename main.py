"""
Smart Beta Index Strategy — entry point
========================================
Run this script to execute the full pipeline:

    python main.py

Steps
-----
1. Fetch factor-ETF and benchmark price data from Yahoo Finance.
2. Compute daily returns and run the rolling-window backtest.
3. Plot cumulative performance vs. S&P 500.
4. Print the risk/return metrics summary table.
"""

import warnings
warnings.filterwarnings("ignore")

from smart_beta import (
    Config,
    DataFetcher,
    PortfolioOptimizer,
    Backtester,
    PerformanceAnalyzer,
)


def main() -> None:
    cfg = Config()

    # ── 1. Fetch market data ──────────────────────────────────────────────────
    print("Fetching market data …")
    fetcher          = DataFetcher(cfg.START_DATE, cfg.END_DATE)
    prices           = fetcher.fetch_prices(cfg.ETF_TICKERS)
    benchmark_prices = fetcher.fetch_benchmark(cfg.BENCHMARK_TICKER)

    factor_returns    = prices.pct_change().dropna()
    benchmark_returns = benchmark_prices.pct_change().dropna()

    print(f"  Factor returns   : {factor_returns.shape[0]} days × {factor_returns.shape[1]} factors")
    print(f"  Benchmark returns: {len(benchmark_returns)} days")

    # ── 2. Optimise & run backtest ────────────────────────────────────────────
    print("\nRunning backtest …")
    optimizer  = PortfolioOptimizer(cfg)
    backtester = Backtester(optimizer, cfg)
    _, portfolio_returns = backtester.run(factor_returns)

    # ── 3. Analyse results ────────────────────────────────────────────────────
    analyzer   = PerformanceAnalyzer(risk_free_rate=cfg.RISK_FREE_RATE)
    chart_path = "performance.png"

    analyzer.plot_cumulative(portfolio_returns, benchmark_returns, save_path=chart_path)
    print(f"\nChart saved → {chart_path}")

    print("\nPerformance Summary")
    print("─" * 44)
    metrics     = analyzer.summary_table(portfolio_returns, benchmark_returns)
    csv_path    = "results.csv"
    metrics.to_csv(csv_path)
    print(metrics.to_string())
    print(f"\nResults saved  → {csv_path}")


if __name__ == "__main__":
    main()
