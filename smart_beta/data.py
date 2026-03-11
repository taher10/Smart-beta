"""Market data retrieval from Yahoo Finance."""

import pandas as pd
import yfinance as yf


class DataFetcher:
    """Handles all market data retrieval from Yahoo Finance.

    Parameters
    ----------
    start_date : str
        Start of the download window (``YYYY-MM-DD``).
    end_date : str
        End of the download window (``YYYY-MM-DD``).
    """

    def __init__(self, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date   = end_date

    def fetch_prices(self, tickers: dict) -> pd.DataFrame:
        """Download adjusted close prices for each factor ETF.

        Parameters
        ----------
        tickers : dict
            Mapping of factor name → ticker symbol (e.g. ``{"Value": "VTV"}``).

        Returns
        -------
        pd.DataFrame
            Daily adjusted close prices, one column per factor, NaN rows dropped.
        """
        data = {
            name: yf.download(
                ticker,
                start=self.start_date,
                end=self.end_date,
                progress=False,
                auto_adjust=True,
            )["Close"].squeeze()
            for name, ticker in tickers.items()
        }
        return pd.DataFrame(data).dropna()

    def fetch_benchmark(self, ticker: str) -> pd.Series:
        """Download a single benchmark price series.

        Parameters
        ----------
        ticker : str
            Benchmark ticker (e.g. ``"^GSPC"``).

        Returns
        -------
        pd.Series
            Daily adjusted close prices, NaN values dropped.
        """
        prices = yf.download(
            ticker,
            start=self.start_date,
            end=self.end_date,
            progress=False,
            auto_adjust=True,
        )["Close"]
        return prices.squeeze().dropna()
