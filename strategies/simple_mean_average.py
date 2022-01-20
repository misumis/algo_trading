from services.instrument import InstrumentHandler
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# SimpleMovingAverage Class

# In this class we apply simple moving average algorithm onto collected data and apply logic to create orders according to signals
# Improves candle plot with moving average line

class SimpleMovingAverage(InstrumentHandler):
    __MOVING_AVERAGE_PERIOD = 6
    __percentile_distribution = []

    def __init__(self, instrument, **kwargs):
        super(SimpleMovingAverage, self).__init__(instrument, **kwargs)
        self.__getStrategyIndicators()

    # Private Methods
    def __getMovingAverage(self):
        self.data['returns'] = self.data['c'].pct_change() * 100
        self.data['ma'] = self.data['c'].rolling(self.__MOVING_AVERAGE_PERIOD).mean()
        self.data['ratio'] = self.data['c'] / self.data['ma']

    def __getPercentiles(self):
        # TODO: Get percentiles as argument
        percentiles = [5,10,50,90,95]
        self.__percentile_distribution = np.percentile(self.data['ratio'].dropna(), percentiles)

    def __getSignals(self):
        short = self.__percentile_distribution[-1] # 95th percentile - SELL
        long = self.__percentile_distribution[0] # 5th percentile - BUY

        self.data['position'] = np.where(self.data.ratio > short, -1, np.nan)
        self.data['position'] = np.where(self.data.ratio < long, 1, self.data['position'])
        self.data['position'] = self.data['position'].fillna(0)

    def __getStrategyIndicators(self):
        self.__getMovingAverage()
        self.__getPercentiles()
        self.__getSignals()
    # Public methods

    def getPercDist(self):
        return self.__percentile_distribution

    def visualizePercentiles(self):
        self.data['ratio'].dropna().plot(legend=True)
        plt.axhline(self.__percentile_distribution[0], c = (.5,.5,.5), ls="--")
        plt.axhline(self.__percentile_distribution[2], c = (.5,.5,.5), ls="--")
        plt.axhline(self.__percentile_distribution[-1], c = (.5,.5,.5), ls="--")

    def visualizeSignals(self):
        self.data['position'].dropna().plot()
        
    def plotCandles(self):
        fig = go.Figure(
        data=[go.Ohlc(
                x=self.data.index.dropna(),
                open=self.data['o'].dropna(),
                high=self.data['h'].dropna(),
                low=self.data['l'].dropna(),
                close=self.data['c'].dropna()
            ),
            go.Scatter(x=self.data.index, y=self.data['ma'].dropna(), line=dict(color='blue', width=1)),
        ])
        fig.show()
    
    def getCurrentInsturmentPositions(self):
        #  For now only single position available BUY or SELL
        for position in self.getPositions()['positions']:
            if position['instrument'] == self.getInstrument():
                return position
        return None

    def applyStategy(self):
        self.updateInstrument()
        self.__getStrategyIndicators()

        curr_status = self.data.iloc[-1]
        pos = self.getCurrentInsturmentPositions()

        # BUY SIGNAL 
        print("Position: {} | Percentile Dist: {} | Ratio: {} | Close: {}".format(curr_status['position'], self.getPercDist()[0], curr_status['ratio'], curr_status['c']))
        if curr_status['position'] == 1:        
            if pos == None:
                print("I bought 0.01 {}!".format(self.getInstrument()))
                self.createOrder("BUY", self.getInstrument(), price=pos['c'], units=0.01)
            else:
                return None
                # Close order

        # SELL SIGNAL
        if curr_status['position'] == -1:     
            if pos == None:
                # TODO: Conisder shorting
                # self.createOrder("SELL", self.getInstrument(), price=pos['c'], units=0.01)
                return None
            else:
                print("I sold 0.01 {}!".format(self.getInstrument()))
                self.closePosition(self.getInstrument())       
        return None