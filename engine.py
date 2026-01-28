import pandas as pd
import numpy as np

class Backtest_Engine:
    def __init__(self):
        pass

    def _check_clean_index(self,data):
        if not data.index.is_monotonic_increasing:
            raise ValueError('Sorted index must be monotonic increasing')
        if not data.index.is_unique:
            raise ValueError('Index must be unique')

    # Vérifications concernant les poids
    def _check_no_nan(self, data):
        if data.isna().any().any():
            raise ValueError("Data can not be NaN")

    def _check_normalized_weights(self, weights):
        if (abs(weights.sum(axis=1) - 1 )> 1e-6).any() :
            raise ValueError("Weights must be normalized")

    def _check_positive_weights(self, weights):
        if (weights <0).any().any() :
            raise ValueError("Weights must be positive")

    def validate_weights(self,weights):
        self._check_no_nan(weights)
        self._check_clean_index(weights)
        self._check_positive_weights(weights)
        self._check_normalized_weights(weights)

    def validate_match_data(self, weights,prices):
        if not weights.index.equals(prices.index):
            raise ValueError("Prices and weights must have same index")
        if not weights.columns.equals(prices.columns):
            raise ValueError("Weights and prices must have same columns")

    #Vérifications concernant les prix
    def _check_positive_prices(self, prices):
        if (prices <=0).any().any() :
            raise ValueError("Prices must be positive")

    def validate_prices(self,prices):
        self._check_no_nan(prices)
        self._check_clean_index(prices)
        self._check_positive_prices(prices)




    def validate_position(self):
        pass

    #La fonction run calcule les contributions aux rendements pondérés par les poids donnés
    def compute_contributions(self, prices: pd.DataFrame , weights: pd.DataFrame) -> pd.DataFrame:
        #Calcul es contributions
        self.validate_weights(weights)
        self.validate_prices(prices)
        self.validate_match_data(weights,prices)

        returns = prices.pct_change()
        return (returns * weights.shift(1)).dropna()

    def compute_returns(self, prices: pd.DataFrame, weights: pd.DataFrame) -> pd.Series:
        return self.compute_contributions(prices,weights).sum(axis=1)



