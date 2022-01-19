from services.instrument import InstrumentHandler
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# MomentumStrategy Class

class MomentumStrategy(InstrumentHandler):
    
    def __init__(self, instrument, **kwargs):
        super(MomentumStrategy, self).__init__(instrument, **kwargs)

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