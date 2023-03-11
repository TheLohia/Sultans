import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin


class LimitRatio(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        x = x.copy()

        x['LimitDownRatio'] = x['OpeningPrice'] / x['LimitDownPrice']
        x['LimitUpRatio'] = x['LimitUpPrice'] / x['OpeningPrice']

        return x


class WeightedAvgComPriceSpread(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        x = x.copy()

        x['WeightedAvgComPriceSpread'] = x['WeightedAverageCommissionedSellingPriceToTick'] -\
                                         x['WeightedAverageCommissionedBuyingPriceToTick']

        return x


class LatestTransactionPriceToTickDiff(BaseEstimator, TransformerMixin):

    def __init__(self, shift=1):
        self.shift = shift

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        x = x.copy()

        prev_price = 'LatestTransactionPriceToTickShift{}Diff'.format(str(self.shift))
        curr_price = 'LatestTransactionPriceToTick'
        x[prev_price] = x.sort_values(['TickTime']) \
                         .groupby('StockCode')[curr_price] \
                         .shift(self.shift)
        
        x[prev_price] = x[curr_price] - x[prev_price]
        
        return x


class Spread(BaseEstimator, TransformerMixin):

    def __init__(self, price_index=1):
        self.price_index = price_index

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        x = x.copy()

        selling_price = 'SellingPrice' + str(self.price_index)
        buying_price = 'BuyingPrice' + str(self.price_index)
        spread = 'Spread' + str(self.price_index)

        x[spread] = x[selling_price] - x[buying_price]

        return x


class RollingComPriceSpreadMean(BaseEstimator, TransformerMixin):

    def __init__(self, window=5):
        self.window = window

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        x = x.copy()

        rolling_com_price = 'RollingComPriceSpreadMean' + str(self.window)

        se_rolling_com_price = x.sort_values(['TickTime']) \
                                .groupby('StockCode')['WeightedAvgComPriceSpread'] \
                                .rolling(self.window).mean()
        x = x.set_index(['StockCode', x.index])
        x[rolling_com_price] = se_rolling_com_price
        x = x.reset_index()

        return x


class RollingTransPriceMean(BaseEstimator, TransformerMixin):

    def __init__(self, window=5):
        self.window = window

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        x = x.copy()

        rolling_com_price = 'RollingTransPriceMean' + str(self.window)

        se_rolling_com_price = x.sort_values(['TickTime']) \
                                .groupby('StockCode')['LatestTransactionProceToTick'] \
                                .rolling(self.window).mean()
        x = x.set_index(['StockCode', x.index])
        x[rolling_com_price] = se_rolling_com_price
        x = x.reset_index()

        return x


class TransactionVolume(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):

        x['TransactionVolume'] = x.sort_values(['TickTime']) \
                                  .groupby('StockCode')['CumulativeTransactionVolumeToTick'] \
                                  .shift(1).fillna(0)

        x['TransactionVolume'] = x['CumulativeTransactionVolumeToTick'] - x['TransactionVolume']

        return x