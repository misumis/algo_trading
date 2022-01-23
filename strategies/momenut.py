from services.instrument import InstrumentHandler
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# MomentumStrategy Class


class MomentumStrategy(InstrumentHandler):
    def __init__(self, instrument, window_length=14, **kwargs):
        super(MomentumStrategy, self).__init__(instrument, **kwargs)
        self.window_length = window_length  # default value set on 14
        self.__count_returns()
        self.__define_movement()
        self.__calculate_rsi()
        self.__count_total()

    def __count_returns(self):
        self.data['return'] = self.data['c'].pct_change()

    def __define_movement(self):
        self.data['movement'] = self.data['c'] - self.data['c'].shift(1)
        self.data['up'] = np.where(
            (self.data['movement'] > 0), self.data['movement'], 0)
        self.data['down'] = np.where(
            (self.data['movement'] < 0), self.data['movement'], 0)

    def __calculate_rsi(self):
        # calculate moving average of the last 14 days  gains
        up = self.data['up'].rolling(self.window_length).mean()
        # calculate moving average of the last 14 days  losses
        down = self.data['down'].abs().rolling(self.window_length).mean()

        RS = up / down
        self.data['rsi'] = 100.0 - (100.0 / (1.0 + RS))

    def __count_total(self):
        self.data['long'] = np.where((self.data['rsi'] < 30), 1, np.nan)
        self.data['long'] = np.where(
            (self.data['rsi'] > 70), 0, self.data['long'])

        self.data['long'].ffill(inplace=True)

        self.data['gain_loss'] = self.data['long'].shift(
            1) * self.data['return']

        self.data['total'] = self.data['gain_loss'].cumsum()
