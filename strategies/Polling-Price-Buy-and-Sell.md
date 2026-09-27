
> Name

Polling-Price-Buy-and-Sell

> Author

永赢量化-1

> Strategy Description

* Based on some characteristics of altcoins, subjective judgment is that certain prices are definitely worth buying and others can be sold for
* In order to improve fund utilization, orders cannot be placed in advance. This strategy is to set the currency price in the rotation configuration, and then place an order after setting the price.
* Thanks to Zinan's mid_class's idea support, I learned and wrote this strategy at station B to practice.
* I hope everyone can learn and make progress together

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|PRICE_PRECISION|{"BTC_USDT":4, "LTC_USDT":6}|Price precision list|
|AMOUNT_PRECISION|{"BTC_USDT":4, "LTC_USDT":6}|List of trading quantity precision|
|HANDS|{"BTC_USDT":4, "LTC_USDT":6}|Number of lots per trade|
|CAN_SELL_PRICE|{"BTC_USDT":[5000,6000], "LTC_USDT":[50,60]}|Sell price range|
|CAN_BUY_PRICE|{"BTC_USDT":[4000,5000], "LTC_USDT":[40,50]}|Buy price range|


> Source (python)

``` python
import numpy as np
import json

#Global Variables
price_precision = {}
amount_precision = {}
hands = {}
can_buy_price = {}
can_sell_price = {}
class mid_class():
    def __init__(self, this_exchange):
        '''
        Initialize data to fill in exchange information, obtain price for the first time, and obtain account information for the first time
        Set the key......
        
        Args:
            this_exchange: FMZExchange structure of
        
        '''
        self.init_timestamp = time.time()
        self.exchange = this_exchange
        self.name = self.exchange.GetName()
        self.jyd = self.exchange.GetCurrency()        
    
    def get_precision(self,pair):
        '''
        Obtain the price and quantity precision of a trading pair
        '''
        precision = [4,6,1]
        if pair not in price_precision.keys():
            Log('No price precision configured: ' + pair)
            return precision
        if pair not in amount_precision.keys():
            Log('No quantity precision configured: ' + pair)
            return precision
        if pair not in hands.keys():
            Log('No lot size configured: ' + pair)
            return precision
        return [price_precision[pair], amount_precision[pair], hands[pair]]
        
    def switch_currency(self,pair):
        '''
        Replace trading pair
        '''
        self.exchange.IO("currency",pair)

    def get_account(self):
        '''
        Get account information
        
        Returns:
            Returns True if information is successfully retrieved; returns False if retrieval fails.False
        '''
        self.Balance = '---'
        self.Amount = '---'
        self.FrozenBalance = '---'
        self.FrozenStocks = '---'
        
        try:
            self.account = self.exchange.GetAccount()

            self.Balance =  self.account['Balance']
            self.Amount = self.account['Stocks']
            self.FrozenBalance =  self.account['FrozenBalance']
            self.FrozenStocks = self.account['FrozenStocks']
            return True
        except:
            return False
    
    def get_ticker(self):
        '''
        Get market price information
        
        Returns:
            Returns True if information is successfully retrieved; returns False if retrieval fails.False
        '''
        self.high = '---'
        self.low = '---'
        self.Sell =  '---'
        self.Buy =  '---'
        self.last =  '---'
        self.Volume = '---'
        
        try:
            self.ticker = self.exchange.GetTicker()
        
            self.high = self.ticker['High']
            self.low = self.ticker['Low']
            self.Sell =  self.ticker['Sell']
            self.Buy =  self.ticker['Buy']
            self.last =  self.ticker['Last']
            self.Volume = self.ticker['Volume']
            return True
        except:
            return False
        
        
    def get_depth(self):
        '''
        Get depth information
        
        Returns:
            Returns True if information is successfully retrieved; returns False if retrieval fails.False
        '''
        self.Ask = '---'
        self.Bids = '---'
        
        try:
            self.Depth = self.exchange.GetDepth()
            self.Ask = self.Depth['Asks']
            self.Bids = self.Depth ['Bids']
            return True
        except:
            return False
        
        
    
    def get_ohlc_data(self, period = PERIOD_M1):
        '''
        Get candlestick information
        
        Args:
            period: KLine period, PERIOD_M1 refers to 1 minute, PERIOD_M5 refers to 5 minutes, PERIOD_M15 refers to 15 minutes,
            PERIOD_M30 Refers to 30 minutes, PERIOD_H1 refers to 1 hour, PERIOD_D1 refers to 1 day.
        '''
        self.ohlc_data = exchange.GetRecords(period)
        
        
    
    def create_order(self, order_type, price, amount):
        '''
        postAn order information
        
        Args:
            order_type:Order type, 'buy' means placing a buy order, 'sell' means placing a sell order
            price:Order Price
            amount:Number of pending orders
            
        Returns:
            Order Id, can be used to cancel the order
        '''
        if order_type == 'buy':
            try:
                order_id = self.exchange.Buy( price, amount)
            except:
                return False
            
        elif order_type == 'sell':
            try:
                order_id = self.exchange.Sell( price, amount)
            except:
                return False
        
        return order_id
    
    def get_orders(self):
        self.undo_ordes = self.exchange.GetOrders()
        return self.undo_ordes
    
    def cancel_order(self, order_id):
        '''
        Cancel an order information
        
        Args:
            order_id:ID number of the pending order you wish to cancel
            
        Returns:
            Returns True if order cancellation is successful; returns False if cancellation fails.False
        '''
        return self.exchange.CancelOrder(order_id)
        
    def refreash_data(self):
        '''
        Refresh information
        
        Returns:
            If the refresh information is successful, 'refresh_data_finish!' will be returned. Otherwise, the corresponding refresh failure information will be returned.
        '''

        if not self.get_account():
            return 'false_get_account'
        
        if not self.get_ticker():
            return 'false_get_ticker'
        if not self.get_depth():
            return 'false_get_depth'
        try:
            self.get_ohlc_data()
        except:
            return 'false_get_K_line_info'
        
        return 'refreash_data_finish!'

 
class qushi_class():
    def __init__(self, mid_class, amount_N, price_N):
        '''
        Set the initial parameters to be considered
        Args:
            mid_class: The exchange middle layer used
            amount_N:Quantity decimal limit
            price_N:Price decimal limit
            
        Attributes:
            amount_N:Quantity decimal limit
            price_N:Price decimal limit
            init_time:Initial time
            last_time:The time when the operation was last performed
            trade_list:Trading requestid
        '''
        self.jys = mid_class
        
        self.init_time = time.time()
        self.last_time = time.time()
        
        self.amount_N = amount_N
        self.price_N = price_N
        
        self.trade_list = []
    
    def cancel_orders(self):
        '''
        Traverse current pending orders, cancel if timeout occurs
        '''
        undo_orders = self.jys.get_orders()
        for i in range(len(undo_orders)):
           self.jys.cancel_order(undo_orders[i].Id)

            
    def refreash_data(self):
        '''
        Used to obtain the latest price and quantity information from the exchange
        
        Attributes:
            B:Quantity of commodity coin
            money:Quantity of pricing coin
            can_buy_B:The current theoretical quantity of the product coin that can be purchased
            Buy_price:The most recent pending buy price in the current market
        '''
        
        message = self.jys.refreash_data()
        if message == 'refreash_data_finish!':
            self.B = self.jys.Amount
            self.money = self.jys.Balance
            self.Buy_price = self.jys.Buy
            self.Sell_price = self.jys.Sell
            self.can_buy_B = self.money/ self.Sell_price * 0.9
            #Position must be30%
            if self.B > ((self.B + self.can_buy_B)*0.3):
                self.can_buy_B = 0
            else:
                self.can_buy_B = _N(self.can_buy_B, self.amount_N )
            return True
        else:
            return False
            
    def make_trade_by_dict(self, trade_dicts):
        '''
        Used to complete transaction orders in batches
        
        Attributes:
            trade_list:of the submitted transaction requestid
        '''
        for this_trade in trade_dicts:
            this_price = _N(this_trade['price'], self.price_N )
            this_amount = _N(this_trade['amount'], self.amount_N )
            
            this_trade_id = self.jys.create_order( this_trade['side'], this_price , this_amount ) 
            self.trade_list.append( this_trade_id )
    
    def condition_chicang(self, hands_num):
        '''
        Conditions for trade decision based on position status
        Args:
            hands_num:indicates the total number of lots traded (we assume each transaction does not exceed one lot)
            
        Attributes:
            min_trade_B: The maximum quantity of the product coin traded per lot
            min_trade_money: Maximum number of pricing coins per transaction
        
        '''
        self.min_trade_B = (self.can_buy_B + self.B) / hands_num
        self.min_buy_B = min(self.min_trade_B, self.can_buy_B)
        self.min_sell_B = min(self.min_trade_B, self.B)
        self.min_trade_money = self.min_trade_B* self.jys.Buy


    
    def condition_qushi(self):
        '''
        Conditions for making transaction decisions based on market price conditions
        '''
        rt = False
        currency = self.jys.jyd
        #Log('cur price' + self.jys.Sell)
        #Log('cur range' + can_buy_price[currency][0])
        if self.jys.Sell > can_buy_price[currency][0] and self.jys.Sell < can_buy_price[currency][1]:
            rt = 'Buy'
        if self.jys.Buy > can_sell_price[currency][0] and self.jys.Buy < can_sell_price[currency][1]:
            rt = 'Sell'
       
        return rt
    
    
    def make_trade_dicts(self, hands_num ):
        '''
        Create transaction dictionary form
        Args:
            hands_num:Total number of lots traded
            change_pct:How much the price changes to trade one lot
            
        Returns:
            this_trade_dicts: Create a list of dictionaries for trades based on current price changes.
        
        '''
        self.condition_chicang(hands_num)
        rt = self.condition_qushi()
        this_trade_dicts = []
        if rt:
            if rt == 'Buy':
                if self.min_buy_B > 10**-self.amount_N:
                    this_trade_dicts.append({
                        'side':'buy',
                        'price':self.jys.Buy,
                        'amount':self.min_buy_B
                    })
            else:
                if self.min_sell_B > 10**-self.amount_N:
                    this_trade_dicts.append({
                        'side':'sell',
                        'price':self.jys.Sell,
                        'amount':self.min_sell_B
                    })
            return this_trade_dicts
        else:
            return False



def main():

    #Get configured value
    global price_precision
    price_precision = json.loads(PRICE_PRECISION)
    global amount_precision 
    amount_precision = json.loads(AMOUNT_PRECISION)
    global hands 
    hands = json.loads(HANDS)
    global can_buy_price
    can_buy_price = json.loads(CAN_BUY_PRICE)
    global can_sell_price
    can_sell_price = json.loads(CAN_SELL_PRICE)
    round = 1
    while True:
        Sleep(1000)
        for i in range(len(exchanges)):
            #Define trading middleware
            test_mid = mid_class(exchanges[i])
            currency = test_mid.jyd
            #Get the price and quantity precision of the trading pair
            currency_precision = test_mid.get_precision(currency)
            #Generate strategy class
            test_qushi = qushi_class(test_mid , currency_precision[0], currency_precision[1])
            #Get the latest data
            result  = test_qushi.refreash_data()
            if result == True:
                now_trade_dicts = test_qushi.make_trade_dicts(currency_precision[2])
                if now_trade_dicts:
                    test_qushi.make_trade_by_dict(now_trade_dicts)
                    now_trade_dicts = False
            #Check order status
            if round % 20 == 0:
                Log('begins to cancel orders')
                Log(test_mid.account)
                test_qushi.cancel_orders()
        
        round = round + 1

```

> Detail

https://www.fmz.com/strategy/202935

> Last Modified

2020-05-11 11:17:14
