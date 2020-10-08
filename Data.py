import pandas as pd
from datetime import datetime


class Data:

    def __init__(self, api):
        self.api = api
        pass

    def getHistData(self, ticker):
        """Grabs ticker data and saves in a file from previous week to beginning of available data; recommended to thread
        
        Uses Polygon market data api through the alpaca library to grab historical market data with a granularity of 1 minute.
        automatically saves collected data into a .csv file labeled with the passed ticker, and located in './StockData/'
        Limitations with the Polygon data api only allow for data to be gathered at a rate of 1 week per call;
         with this limited rate and the timeframes of the data, a single call can take minutes.
        """

        end = datetime.today().timestamp()*1000
        end = end - ((end - 1596254400000)%604800000) #align with sunday to saturday

        start = end - 604800000 #set start and end a week apart 

        df = self.api.polygon.historic_agg_v2(ticker, 1, 'minute', _from=start, to=end).df
        end -= 604800000 #roll back a week
        start -= 604800000

        while True:
            df2 = self.api.polygon.historic_agg_v2(ticker, 1, 'minute', _from=start, to=end).df
            if len(df2.index) == 0:
                break
            df2.columns = df.columns
            df = pd.concat([df2, df])
            end -= 604800000 #roll back a week at a time
            start -= 604800000

        df.to_csv(r'StockData/' + ticker +'.csv', index=True, header=True)
        print(ticker + ': ' + str(len(df.index)) + ' lines')