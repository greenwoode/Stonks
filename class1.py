import alpaca_trade_api as trading
import pandas as pd
import time, datetime, pytz

class trader:

    acount = ''
    time_zone = 'America/New_York'

    def __init__(self):

        with open('UserData\API_Keys.txt', 'r') as API_Info:

            self.endpoint = API_Info.readline().replace('\n', '')
            self.key = API_Info.readline().replace('\n', '')
            self.secret_key = API_Info.readline().replace('\n', '')

        self.api = trading.REST(self.key, self.secret_key, base_url=self.endpoint)

        print(f'endpoint: {self.endpoint}')
        print(f'key: {self.key}')
        print(f'secret: {self.secret_key}')


    def get_user_data(self):

        self.acount = self.api.get_account()

    def buy(self):

        start = pytz.timezone(self.time_zone).localize(datetime.datetime(2012, 9, 28, 0, 0)).timestamp()*1000
        
        end = pytz.timezone(self.time_zone).localize(datetime.datetime(2012, 10, 2, 0, 0)).timestamp()*1000

        df = self.api.polygon.historic_agg_v2('AES', 1, 'minute', _from=start, to=end).df
        df.to_csv(r'StockData\\' + str(start) + '_to_' + str(end) +'.csv', index=True, header=True)
        print(df)

    def test(self, message):
        print(message)
    



    
        
test = trader()
test.buy()

