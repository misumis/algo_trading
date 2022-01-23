import requests
import json
from config.constants import HEADERS, BASE_URL

# AccountManager Class
# This class contains methods that allow to retrieve information about account and make orders.
# It allows to:
# Get orders
# Get positions
# Get account details
# Create buy and sell orders
# Close Position


class AccountManager(object):

    __accountId = None

    def __init__(self):
        self.getAccountId()

    def getAccountId(self):
        if self.__accountId != None:
            return self.__accountId
        account = requests.get('{}accounts'.format(
            BASE_URL), headers=HEADERS).json()
        # TODO: Check if account exists else thor init error
        self.__accountId = account['accounts'][0]['id']
        return self.__accountId

    def getAccountDetails(self):
        return requests.get('{}accounts/{}'.format(BASE_URL, self.getAccountId()), headers=HEADERS).json()

    def getOrders(self):
        return requests.get('{}accounts/{}/orders'.format(BASE_URL, self.getAccountId()), headers=HEADERS).json()

    def getInstruments(self):
        return requests.get('{}accounts/{}/instruments'.format(BASE_URL, self.getAccountId()), headers=HEADERS).json()

    def getPositions(self):
        return requests.get('{}accounts/{}/positions'.format(BASE_URL, self.getAccountId()), headers=HEADERS).json()

    def createOrder(self, type, instrument, price, units=0.01):
        if type == "SELL" or type == "BUY":
            if type == "SELL":
                units = -units

            # TODO: Change limits to something more tangible. 1.03 and 0.98 are magic numbes
            takeProfit = round(price*1.03, 1)
            stopLoss = round(price*0.98, 1)

            # TODO: Decide which body should be used.

            # Create Stop Loss Take Profit Limit order
            # body = {
            #     "order": {
            #         "price": str(price),
            #         "stopLossOnFill": {
            #             "timeInForce": "GTC",
            #             "price": str(stopLoss)
            #         },
            #         "takeProfitOnFill": {
            #             "price": str(takeProfit),
            #             "timeInForce": "GTC",
            #         },
            #         "instrument": instrument,
            #         "units": units,
            #         "type": "LIMIT",
            #         "positionFill": "DEFAULT"
            #     }
            # }
            # Create Fulfill or kill order
            body = {
                "order": {
                    "units": str(units),
                    "instrument": instrument,
                    "timeInForce": "FOK",
                    "type": "MARKET",
                    "positionFill": "DEFAULT"
                }
            }
            body = json.dumps(body)
            return requests.post("{}accounts/{}/orders".format(BASE_URL, self.getAccountId()), headers=HEADERS, data=body)

    def closePosition(self, instrument):
        body = {
            "longUnits": "ALL"
        }
        body = json.dumps(body)
        return requests.put("{}accounts/{}/positions/{}/close".format(BASE_URL, self.getAccountId(), instrument), headers=HEADERS, data=body)
