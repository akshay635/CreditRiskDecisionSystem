
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import PowerTransformer

class SkewTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, numeric_features, threshold_low=1, threshold_high=3):
        self.numeric_features = numeric_features
        self.threshold_low = threshold_low
        self.threshold_high = threshold_high
        self.power_transformers = {}

    def fit(self, X, y=None):
        X = pd.DataFrame(X).copy()
        for col in self.numeric_features:
            skew = X[col].skew()
            if skew >= self.threshold_high:
                pwtr = PowerTransformer(method='yeo-johnson')
                pwtr.fit(X[[col]])
                self.power_transformers[col] = pwtr
        return self

    def transform(self, X):
        X = pd.DataFrame(X).copy()
        for col in self.numeric_features:
            skew = X[col].skew()
            if self.threshold_low <= skew < self.threshold_high:
                X[col] = np.log1p(X[col])
            elif skew >= self.threshold_high and col in self.power_transformers:
                X[col] = pd.Series(self.power_transformers[col].transform(X[[col]]).ravel(), index=X.index)

        return X