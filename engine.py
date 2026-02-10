import pandas as pd


class Backtest_Engine:
    """
    Execution-only backtest engine.

    This class is responsible for:
    - validating input data (prices, weights)
    - enforcing execution constraints (long-only, no leverage)
    - executing portfolio returns without look-ahead bias

    The engine is deliberately strategy-agnostic:
    it does not generate signals, forecasts, or weights.
    """

    # Numerical tolerance used for floating-point comparisons
    TOL = 1e-6

    def __init__(self, prices, weights):
        """
        Initialize the backtest engine with exogenous inputs.

        Parameters
        ----------
        prices : pd.DataFrame
            Asset prices indexed by date.
        weights : pd.DataFrame
            Portfolio weights decided ex-ante
            (same index and columns as prices).
        """
        # Input price data
        self.prices = prices

        # Input portfolio weights
        self.weights = weights

        # Fundamental engine output:
        # per-asset return contributions (set after run)
        self.contributions = None

    # ------------------------------------------------------------------
    # Generic checks (shared by prices and weights)
    # ------------------------------------------------------------------

    def _check_clean_index(self, data, name):
        """
        Ensure that the index is:
        - strictly increasing
        - unique

        This prevents duplicated timestamps and look-ahead issues.
        """
        if not data.index.is_monotonic_increasing:
            raise ValueError(f"Sorted {name} index must be monotonic increasing")
        if not data.index.is_unique:
            raise ValueError(f"{name} index must be unique")

    def _check_no_nan(self, data, name):
        """
        Ensure that the input data contains no NaN values.
        """
        if data.isna().any().any():
            raise ValueError(f"{name} contains NaN")

    # ------------------------------------------------------------------
    # Weight-specific checks
    # ------------------------------------------------------------------

    def _check_net_exposure(self):
        """
        Enforce execution constraint:
        net exposure must not exceed 100%.

        This corresponds to a long-only, no-leverage mandate.
        """
        if (self.weights.sum(axis=1) > 1 + self.TOL).any():
            raise ValueError("Net exposure exceeds 100% (no leverage allowed)")

    def _check_not_negative(self, data, name):
        """
        Ensure that data is non-negative.
        Zero values are allowed (e.g. cash positions).
        """
        if (data < 0).any().any():
            raise ValueError(f"{name} must be non-negative")

    def validate_weights(self):
        """
        Validate portfolio weights under execution constraints.
        """
        self._check_no_nan(self.weights, "Weights")
        self._check_clean_index(self.weights, "Weights")
        self._check_not_negative(self.weights, "Weights")
        self._check_net_exposure()

    # ------------------------------------------------------------------
    # Price-specific checks
    # ------------------------------------------------------------------

    def _check_positive(self, data, name):
        """
        Ensure that price data is strictly positive.
        Prices equal to zero are considered invalid.
        """
        if (data <= 0).any().any():
            raise ValueError(f"{name} must be strictly positive")

    def validate_prices(self):
        """
        Validate input price data.
        """
        self._check_no_nan(self.prices, "Prices")
        self._check_clean_index(self.prices, "Prices")
        self._check_positive(self.prices, "Prices")

    # ------------------------------------------------------------------
    # Cross-data consistency checks
    # ------------------------------------------------------------------

    def validate_match_data(self):
        """
        Ensure that prices and weights are perfectly aligned:
        - same index (dates)
        - same columns (assets)
        """
        if not self.weights.index.equals(self.prices.index):
            raise ValueError("Prices and weights must have the same index")
        if not self.weights.columns.equals(self.prices.columns):
            raise ValueError("Prices and weights must have the same columns")

    # ------------------------------------------------------------------
    # Backtest execution
    # ------------------------------------------------------------------

    def run(self):
        """
        Execute the backtest.

        This method:
        - validates all inputs
        - computes asset returns (close-to-close)
        - applies weights decided at t-1
        - stores per-asset return contributions
        """
        # Validate all inputs before execution
        self.validate_prices()
        self.validate_weights()
        self.validate_match_data()

        # Compute asset returns (close-to-close)
        asset_returns = self.prices.pct_change()

        # Compute per-asset return contributions
        # using weights decided at the previous period (no look-ahead)
        contributions_returns = asset_returns * self.weights.shift(1)

        # Store fundamental engine output
        self.contributions = contributions_returns.dropna()

    # ------------------------------------------------------------------
    # Derived quantities
    # ------------------------------------------------------------------

    @property
    def returns(self):
        """
        Portfolio returns per period.

        This is a derived quantity obtained by aggregating
        per-asset return contributions.
        """
        if self.contributions is None:
            raise RuntimeError("Contributions not computed yet")
        return self.contributions.sum(axis=1)