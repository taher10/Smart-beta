"""Market-regime detection via Gaussian Mixture Model."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture


class RegimeDetector:
    """Identifies market regimes using a Gaussian Mixture Model (GMM).

    Two regimes are detected by default (e.g. bull/bear or
    low-vol/high-vol), but ``n_regimes`` can be increased for finer
    granularity.

    Parameters
    ----------
    n_regimes : int
        Number of distinct regimes to model (GMM components).
    random_state : int
        Seed for reproducibility.
    """

    def __init__(self, n_regimes: int = 2, random_state: int = 42):
        self.n_regimes = n_regimes
        self._model = GaussianMixture(
            n_components=n_regimes,
            covariance_type="full",
            random_state=random_state,
        )

    def fit_predict(
        self, returns: pd.DataFrame
    ) -> tuple[np.ndarray, np.ndarray]:
        """Fit the GMM on ``returns`` and return probabilities and labels.

        Parameters
        ----------
        returns : pd.DataFrame
            Factor return matrix (observations × factors).

        Returns
        -------
        probabilities : np.ndarray, shape (n_samples, n_regimes)
            Posterior regime probabilities for each observation.
        labels : np.ndarray, shape (n_samples,)
            Hard regime assignment (argmax of probabilities).
        """
        self._model.fit(returns)
        probabilities = self._model.predict_proba(returns)
        labels        = self._model.predict(returns)
        return probabilities, labels
