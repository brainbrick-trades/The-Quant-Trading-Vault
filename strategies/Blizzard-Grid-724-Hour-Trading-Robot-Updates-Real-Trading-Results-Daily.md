
> Name

Blizzard-Grid-724-Hour-Trading-Robot-Updates-Real-Trading-Results-Daily

> Author

红色的雪



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|base_price|3|Base price - midline price|
|sale_buy_diff|0.03|Buy-sell spread, selling price - buying price|
|two_distance|0.01|When increasing or decreasing, the distance of each grid|
|trade_amount|2|Quantity per trade|
|sale_price_max|5|Maximum selling price|
|buy_price_min|true|Maximum buying price|


> Source (python)

``` python
#!python2
# -*- coding:utf-8 -*-
'''
Mainly uses the inventor's quantification API for grid trading, currently only supports single-product grid trading
'''
from time import sleep
import datetime,copy

sale_price_list = [] #Selling price list
buy_price_list = []  #Buying price list

class fmz_market():
    def get_data_depth(self):
        data_depth = exchange.GetDepth()
        return data_depth



    #Check if buy/sell operations can be performed currently
    def make_trade_check(self,symbol):
        trade_infor = {'price':0,'trade_type':''}
        #Make buy/sell list judgments, first update the trade record list
        trade_price_list = self.get_trade_price_list(symbol)
        sale_price_list = trade_price_list[0]
        buy_price_list = trade_price_list[1]
        #Fetch depth data
        data_depth = self.get_data_depth()
        #Buy Order List:
        data_depth_bids = data_depth.Bids[0]
        #Sell Order List:
        data_depth_asks = data_depth.Asks[0]
        #If buy record is not empty
        sale_buy_diff_now = two_distance*len(sale_price_list) if len(sale_price_list) >0 else sale_buy_diff
        sale_buy_diff_sale = two_distance if len(sale_price_list) > 0 else sale_buy_diff
        # sale_price_last = float(sale_price_list[len(sale_price_list)-1]) if len(sale_price_list) >0 else base_price
        # buy_price_last = float(buy_price_list[len(buy_price_list)-1]) if len(buy_price_list) >0 else base_price
        sale_price_last = float(sale_price_list[0]) if len(sale_price_list) > 0 and float(sale_price_list[0]) > base_price else base_price
        buy_price_last = float(buy_price_list[0]) if len(buy_price_list) > 0 and float(buy_price_list[0]) < base_price else base_price
        #Determine whether the current price meets the sell price request
        if float(data_depth_bids.Price) - sale_price_last > sale_buy_diff_sale and float(data_depth_bids.Amount) > trade_amount * 1.5:
            Log("Current Selling Price:",str(data_depth_bids.Price),"Highest sell price in the order:",str(sale_price_last),"Generate Sell Order")
            trade_infor['price'] = float(data_depth_bids.Price)
            trade_infor['trade_type'] = 'sale'
        #Determine whether the current price meets the buy price request
        if  buy_price_last - float(data_depth_asks.Price) > sale_buy_diff_now and float(data_depth_bids.Amount) > trade_amount * 1.5:
            #Log("Current Buying Price:", str(data_depth_asks.Price), "Highest buy price in the order:", str(sale_price_last),"Generate Buy Order")
            trade_infor['price'] = float(data_depth_bids.Price)
            trade_infor['trade_type'] = 'buy'
        #Determine whether the current price breaks the limit; if it does, clear the trading information
        if float(data_depth_bids.Price) - sale_price_max > 0 or buy_price_min - float(data_depth_asks.Price) > 0:
            trade_infor['price'] = 0
            trade_infor['trade_type'] = ''
        timestr = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        Log(trade_infor,"...time:",timestr)
        if trade_infor['price'] != 0:
            #Log(trade_infor,"...time:",timestr)
            pass
        return trade_infor

    #Generate a list of buy/sell prices based on order information
    def get_trade_price_list(self,symbol):
        sale_list = []
        buy_list = []
        #Get all trading records and allocate them to buy and sell lists according to different types
        orders = exchange.GetOrders()
        for i in range(len(orders)):
            if orders[i].Type == 1:
                sale_price = float(orders[i].Price)
                sale_price_bak = copy.deepcopy(sale_price)
                sale_list.append(sale_price_bak)
            if orders[i].Type == 0:
                buy_price = float(orders[i].Price)
                buy_price_bak = copy.deepcopy(buy_price)
                buy_list.append(buy_price_bak)
        #Judged as0Array processing of
        if len(sale_list) == 0:
            for i in range(len(buy_list)):
                sale_list.append(float('%.6f' % (buy_list[i] + sale_buy_diff)))
        if len(buy_list) == 0:
            for i in range(len(sale_list)):
                buy_list.append(float('%.6f' % (sale_list[i] - sale_buy_diff)))
        trade_price_list = [sale_list,buy_list]
        return trade_price_list

    #Grid trading entry:
    def grid_trade_start(self,symbol):
        #Get status, rising/Decline
        # trend_status = self.kline_trend_check(symbol)
        
        #Check if trading is possible
        trade_infor = self.make_trade_check(symbol)
        #Determine whether to trade, check if it can be sold
        # if trend_status == 'is_up' and trade_infor['price'] > 0 and trade_infor['trade_type'] == 'sale':
        if trade_infor['price'] > 0 and trade_infor['trade_type'] == 'sale':
            buy_price = float('%.6f' % (trade_infor['price'] - sale_buy_diff))
            #Call order function,Call sell first, then call buy
            order_id = exchange.Sell(trade_infor['price'], trade_amount)
            #Log('order_id:',order_id)
            #Check if the order was successful; if not, return directly
            if order_id is None:
                Log("Order failed, waiting600sContinue.........")
                sleep(600)
                return 0
            #Check whether the main trade was successful: determine if the sell order was successfully executed,If the trade is successful, place a buy order
            for i in range(100):
                sale_orders = exchange.GetOrder(order_id)
                #Log('sale_orders:',sale_orders)
                if sale_orders.Status == 1:
                    #If the sell order has been completed, submit the buy order.
                    exchange.Buy(buy_price, trade_amount)
                    return 0
                sleep(10)
            #If after looping 1000 times there is still no deal, cancel the order
            exchange.CancelOrder(order_id)
        # Determine whether to trade, check if it can be bought
        if trade_infor['price'] > 0 and trade_infor['trade_type'] == 'buy':
            sale_price = float('%.6f' % (trade_infor['price'] + sale_buy_diff))
            # Call the order function, call buy first, then call sell
            order_id = exchange.Buy(trade_infor['price'], trade_amount)
            # Check if the order was successful; if not, return directly
            if order_id is None:
                #Log("Order failed, waiting600sContinue.........")
                sleep(600)
                return 0
            # Check whether the main trade is successful: Determine whether the buy order is successful, and if successful, place a sell order
            for i in range(100):
                buy_orders = exchange.GetOrder(order_id)
                if buy_orders.Status == 1:
                    # If the buy order has been completed, submit the sell order
                    exchange.Sell(sale_price, trade_amount)
                    return 0
                sleep(10)
            # If after looping 1000 times there is still no deal, cancel the order
            exchange.CancelOrder(order_id)

    #Perform loop call
    def grid_trade_cycle(self,symbol):
        cycle_num = 0
        while(True):
            timestr = (datetime.datetime.now()).strftime('%H%M%S')
            self.grid_trade_start(symbol)
            sleep(10)
            cycle_num = cycle_num + 1
            if cycle_num % 100 == 0:
                account_infor = exchange.GetAccount()
                Log("Current user's account information:%s,....Number of cycles checked so far:%s"%(account_infor,str(cycle_num)))

def main():
    Log(exchange.GetAccount())
    Log("Test")
    fmz_market_instances = fmz_market()
    fmz_market_instances.grid_trade_cycle(100)
    #order_id = exchange.Sell(10000,1)
```

> Detail

https://www.fmz.com/strategy/175807

> Last Modified

2020-03-12 13:53:43
