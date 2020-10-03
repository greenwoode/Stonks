import alpaca_trade_api as trading

import time, datetime, pytz

class trader:

    acount = ''
    time_zone = 'America/New_York'

    def __init__(self):


        #change with your own info here
        with open('user data/Quinn paper info.dat', 'r') as f:

            self.endpoint = f.readline().replace('\n', '')
            self.key = f.readline().replace('\n', '')
            self.secret_key = f.readline().replace('\n', '')

        self.api = trading.REST(self.key, self.secret_key, base_url=self.endpoint)

        print(f'endpoint: {self.endpoint}')
        print(f'key: {self.key}')
        print(f'secret: {self.secret_key}')


    def get_user_data(self):

        self.acount = self.api.get_account()

    def buy(self):

        start = pytz.timezone(self.time_zone).localize(datetime.datetime(2011, 11, 4, 0, 0)).timestamp()*1000
        
        end = pytz.timezone(self.time_zone).localize(datetime.datetime(2011, 11, 4, 0, 30)).timestamp()*1000

        df = self.api.polygon.historic_agg_v2('AES', 1, 'minute', _from=start, to=end).df

        print(df)

    def test(self, message):
        print(message)
    



    
        
test = trader()
test.buy()

