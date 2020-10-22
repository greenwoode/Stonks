import pandas as pd
import numpy as np
np.set_printoptions(precision=3, suppress=True)

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

from datetime import datetime
from os import path
import os
import time

class write:

    def __init__(self, api):
        self.api = api
        pass

    def __readLastLine(self, file):
        f = open(file, 'rb')

        f.seek(-2, 2)
        while f.read(1) != b'\n':
            f.seek(-2, 1)
        r = f.read().decode('utf-8')
        return r

    def __readLastTime(self, file):
        return int(self.__readLastLine(file)[1]) + 86400000

    def __writeToCSV(self, file, df, mode='w'):

        print('writing to file ' + file)
        df.to_csv(file, mode=mode)
        print('finished writing to ' + file)

    def __websocket(self, ticker):
        pass
        while True:
            df = pd.DataFrame()
            clock = api.get_clock()
            while clock.is_open:

                clock = api.get_clock()
                df.append()

                clock = api.get_clock()
                time.sleep(60 - (clock.timestamp.timestamp() % 60))

            self.__writeToCSV(df, mode='a')
            time.sleep((clock.next_open.timestamp() - clock.timestamp.timestamp()) + 60)

    def getHistData(self, ticker):
        """Grabs ticker data and saves in a file from previous week to beginning of available data; recommended to thread
        
        Uses Polygon market data api through the alpaca library to grab historical market data with a granularity of 1 minute.
        automatically saves collected data into a .csv file labeled with the passed ticker, and located in './StockData/'
        Limitations with the Polygon data api only allow for data to be gathered at a rate of 1 week per call;
         with this limited rate and the timeframes of the data, a single call can take minutes.
        """

        file = (r'StockData/' + ticker +'.csv')
        filet = (r'StockData/' + ticker +'_temp.csv')
        fe = path.isfile(file)

        end = datetime.today().timestamp()*1000
        end = end - ((end - 1596254400000)%604800000) #align with sunday to saturday

        if fe:
            curr = self.__readLastTime(file)
            print(file + ' found, appending')
        rc = False

        if fe and curr == end:
                rc = True
                return

        start = end - 604800000 #set start and end a week apart 

        df = self.api.polygon.historic_agg_v2(ticker, 1, 'minute', _from=start, to=end).df
        end -= 604800000 #roll back a week
        start -= 604800000

        while True:

            if fe and curr == end:
                rc = True
                break
            
            df2 = self.api.polygon.historic_agg_v2(ticker, 1, 'minute', _from=start, to=end).df
            if len(df2.index) == 0:
                break
            df2.columns = df.columns
            df = pd.concat([df2, df])
            end -= 604800000 #roll back a week at a time
            start -= 604800000

        self.__writeToCSV(filet, df, mode='w') #fix timestamp column by writing to csv then reading
        df = pd.read_csv(filet)
        os.remove(filet)

        df.insert(0,'UTCtimestamps', df.apply((lambda x: datetime.strptime((x['timestamp']), '%Y-%m-%d %H:%M:%S%z').timestamp()*1000), axis=1))
                                                                                    #2010-06-29 08:25:00-04:00

        if fe and rc:
            self.__writeToCSV(file, df, mode='a')
        else:
            self.__writeToCSV(file, df, mode='w')

        

        print(ticker + ': ' + str(len(df.index)) + ' lines')


class read:

    def __init__(self, api, file):
        self.api = api
        self.df = pd.read_csv(file)
        self.da = np.array(self.df)[:,1:]
        

    def readBetweenTimestamp(self, start=-1, stop=-1):



        if start == -1:
            start = self.da[0][0]

        if stop == -1:
            stop = self.da[-1][0]

        return self.da[(np.argwhere(self.da == start)[0])[0]:(np.argwhere(self.da == stop)[0])[0]][:]

    def test(self):
        self.da[:][0] = self.da[:][0]