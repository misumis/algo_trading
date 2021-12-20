import requests
import plotly.graph_objects as go
import pandas as pd
from config.constants import HEADERS, BASE_URL, INSTRUMENT, GRANULARITY, PERIOD
from services.account import AccountManager

# InstrumentHandler Class

# Inherits AccountManager class
# This class is strictly connected to Instrument only.
# It main purpose is to create dataframe that can be used for further usage.
# Additionaly can visualize Instruments candle plot. 
# Used as a base for strategies. 

class InstrumentHandler(AccountManager): 
    __instrument = INSTRUMENT

    def __init__(self, instrument):
        self.__instrument = instrument
        self.data = pd.DataFrame()
        self.initializeInstrument()
        print("{} Initialized".format(instrument))
    
    def __getInstrument(self, period):
        url = '{}instruments/{}/candles?granularity={}&count={}'.format(BASE_URL, self.__instrument, GRANULARITY, period)
        return requests.get(url, headers=HEADERS).json()

    def __getInstrumentDataframe(self, period = PERIOD):
        df = pd.DataFrame()
        for i, row in enumerate(list(self.__getInstrument(period)['candles'])):
            df.loc[i, 'time'] = pd.to_datetime(row['time'])
            df.loc[i, 'o'] = pd.to_numeric(row['mid']['o'])
            df.loc[i, 'h'] = pd.to_numeric(row['mid']['h'])
            df.loc[i, 'l'] = pd.to_numeric(row['mid']['l'])
            df.loc[i, 'c'] = pd.to_numeric(row['mid']['c'])
        df = df.set_index("time")
        return df

    def getInstrument(self):
        return self.__instrument

    def plotCandles(self):
        fig = go.Figure(
        data=[go.Ohlc(
                x=self.data.index,
                open=self.data['o'],
                high=self.data['h'],
                low=self.data['l'],
                close=self.data['c']
            ),
        ])
        fig.show()
    
    def updateInstrument(self):
        self.data = pd.concat([self.data, self.__getInstrumentDataframe(1)])

    def initializeInstrument(self):
        self.data = self.__getInstrumentDataframe()