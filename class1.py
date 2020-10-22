import alpaca_trade_api as trading
import pandas as pd
import time, pytz
from datetime import datetime
from os import path
import threading


import Data

class Trader:

    time_zone = 'America/New_York'

    def __init__(self):

        with open('UserData/API_Keys.txt', 'r') as API_Info:

            self.endpoint = API_Info.readline().replace('\n', '')
            self.key = API_Info.readline().replace('\n', '')
            self.secret_key = API_Info.readline().replace('\n', '')

        self.api = trading.REST(self.key, self.secret_key, base_url=self.endpoint)

        print(f'endpoint: {self.endpoint}\n')
        

    def get_user_data(self):

        return self.api.get_account()

    def buy(self, ticker):

        start = pytz.timezone(self.time_zone).localize(datetime.datetime(2000, 6, 27, 0, 0)).timestamp()*1000
        
        end = pytz.timezone(self.time_zone).localize(datetime.datetime(2000, 6, 30, 0, 0)).timestamp()*1000

        df = self.api.polygon.historic_agg_v2(ticker, 1, 'minute', _from=start, to=end).df
        df.to_csv(r'StockData/' + ticker +'.csv', index=True, header=True)
        print(df)

    def test(self, message):
        print(message)

    def getHistData(self, ticker):
        pass

test = Trader()
#print(test2.readBetween('2004-01-02 09:32:00-05:00'))

hist = Data.write(test.api)
hist.getHistData('DOW')

#test2 = Data.read(test.api, './StockData/DOW.csv')
#print(test2.da)

#
#tickers = ['AES', 'MSFT', 'AMZN', 'NVDA', 'DIS', 'AMD', 'AAPL', 'NFLX', 'TSLA', 'GOOG', 'IBM', 'SPY', 'DOW', 'PYPL', 'INTC']
#
#threads = []
#
#for ticker in tickers:
#    print('starting ' + ticker)
#    thread = threading.Thread(target=hist.getHistData, args=(ticker,), daemon=True)
#    thread.start()
#    threads.append(thread)
#
#while len(threads) != 0:
#    
#    for thread in threads:
#        if not thread.is_alive():
#            threads.remove(thread)
#    time.sleep(0.1)