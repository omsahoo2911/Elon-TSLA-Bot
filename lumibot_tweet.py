from config import ALPACA_CONFIG
from datetime import datetime
from lumibot.backtesting import YahooDataBacktesting
from lumibot.brokers import Alpaca
from lumibot.strategies import Strategy
from lumibot.traders import Trader
import pandas as pd
import sqlite3
from IPython.display import display


class elon_tweet(Strategy):

    data = []
    order_number = 0
    tweet_date = 0
    
    conn = sqlite3.connect("sen_twt.db")
    cur = conn.cursor()
    tweets_db= pd.read_sql_query("SELECT * from tweets", conn)
    tweets = pd.DataFrame(tweets_db, columns=["Text","CreatedAt","positive"])
    tweets = tweets[tweets['positive']>=0.9]
    tweets_arr = tweets['CreatedAt'].tolist()
    tweets_arr = [x[:10] for x in tweets_arr]
    tweets_arr = list(dict.fromkeys(tweets_arr))
    display(tweets_arr)
        
    def initialize(self):
        self.sleeptime = "1D"

    def on_trading_iteration(self):
        if self.first_iteration:
            symbol = "GOOG"
            price = self.get_last_price(symbol)
            quantity = self.cash // price
            order = self.create_order(symbol, quantity, "buy")
            self.submit_order(order)

    # def on_trading_iteration(self):
    #     symbol ="TSLA"
    #     entry_price = self.get_last_price(symbol)
    #     self.log_message(f"Position: {self.get_position(symbol)}")
    #     today_price = self.get_last_price(symbol)
    #     self.data.append(today_price)
    #     today = self.get_datetime().strftime('%Y-%m-%d')[:10]

    #     # if today in self.tweets_arr: 
    #     #     print(today, today in self.tweets_arr)
        
        
    #     if today in self.tweets_arr and self.cash>0:
    #         amount = 10 if self.cash>= today_price*10 else self.cash
    #         order = self.create_order(symbol, quantity = amount, side = "buy")
    #         self.submit_order(order)
            
    #         # temp = self.data[-3:]
    #         # if temp[-1] > temp[1] > temp[0]:
    #         #     self.log_message(f"Last 3 prints: {temp}")
    #         #     order = self.create_order(symbol, quantity = 10, side = "buy")
    #         #     self.submit_order(order)
    #         #     self.order_number += 1
    #         #     if self.order_number == 1:
    #         #         self.log_message(f"Entry price: {temp[-1]}")
    #         #         entry_price = temp[-1] # filled price
    #         # if self.get_position(symbol) and self.data[-1] < entry_price * .995:
    #         #     self.sell_all()
    #         #     self.order_number = 0
    #         # elif self.get_position(symbol) and self.data[-1] >= entry_price * 1.015:
    #         #     self.sell_all()
    #         #     self.order_number = 0
                
                
    def before_market_closes(self):
        print("selling")
        self.sell_all()


if __name__ == "__main__":
    trade = False
    if trade:
        broker = Alpaca(ALPACA_CONFIG)
        strategy = elon_tweet(broker=broker)
        trader = Trader()
        trader.add_strategy(strategy)
        trader.run_all()
    else:
        start = datetime(2019, 6, 1)
        end = datetime(2023, 12, 31)
        elon_tweet.backtest(
            YahooDataBacktesting,
            start,
            end
        )