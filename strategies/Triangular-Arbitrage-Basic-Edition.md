
> Name

Triangular-Arbitrage-Basic-Edition

> Author

红色的雪





> Source (python)

``` python
#!python2
# -*- coding:utf-8 -*-
from time import sleep

Q3 = 0.5
tax = 0.0015   #Transaction rate,0.15%


class fmz_market():

    # Basic Market Data Processing, Fetch Data According to the Provided Trading Pair, and Return the Market Quotesdict
    def basic_data_handle(self, pair):
        pair_depth = {'sale_volume': 0, 'sale_price': 0, 'buy_volume': 0, 'buy_price': 0}
        depth = exchanges[pair].GetDepth()
        asks_infor = depth.Asks[0]
        bids_infor = depth.Bids[0]
        pair_depth['sale_volume'] = asks_infor.Amount
        pair_depth['sale_price'] = asks_infor.Price
        pair_depth['buy_volume'] = bids_infor.Amount
        pair_depth['buy_price'] = bids_infor.Price
        #Log(pair_depth)
        return pair_depth



    #Perform parameter calculation
    def profit_calculation(self):
        profit_obtain = 0
        #Get market data first
        P1_depth = self.basic_data_handle(0)
        P2_depth = self.basic_data_handle(1)
        P3_depth = self.basic_data_handle(2)
        #Organize buy-one price
        p1_sale_price =float(P1_depth['sale_price'])
        p1_buy_price = float(P1_depth['buy_price'])
        p2_sale_price = float(P2_depth['sale_price'])
        p2_buy_price = float(P2_depth['buy_price'])
        p3_sale_price = float(P3_depth['sale_price'])
        p3_buy_price = float(P3_depth['buy_price'])

        #Organize depth data
        p1_sale_volume = float(P1_depth['sale_volume'])
        p1_buy_volume = float(P1_depth['buy_volume'])
        p2_sale_volume = float(P2_depth['sale_volume'])
        p2_buy_volume = float(P2_depth['buy_volume'])
        p3_sale_volume = float(P3_depth['sale_volume'])
        p3_buy_volume = float(P3_depth['buy_volume'])
        # Conduct data analysis, forward transaction rate, P1: EOS_USDT, P2: BTC_USDT, P3: EOS_ETH, sell EOS, buy BTC, buy EOS (sell, buy, buy)
        if p1_buy_price / p2_sale_price > p3_sale_price:
            #Total handling fee calculation
            tax_account = (p1_buy_price + p3_sale_price*p2_sale_price + p3_sale_price*p2_sale_price) * Q3 * tax
            #Total profit calculation
            profit_sum = (p1_buy_price / p2_sale_price - p3_sale_price) * Q3 * p2_buy_price
            Log('P1;',p1_buy_price,',P2:',p2_sale_price,',P3:',p3_sale_price,',tax_account:',tax_account,',profit_sum:',profit_sum)
            #If total profit < fees, then exit directly
            if profit_sum < tax_account:
                return 0
            p1_accout_receive = p1_buy_price * Q3 * (1 - tax) #Sell EOS and get usdt, minus tax
            p3_accout_used = p3_sale_price * Q3 * (1 + tax)  #What is needed when calculating the purchase of Q3 EOSBTC
            p2_accout_used =  p2_sale_price *  p3_accout_used * (1 + tax) #Calculate the USDT amount needed to buy BTC
            #Total profit calculation
            profit_obtain = p1_accout_receive - p2_accout_used  #USDT obtained from selling EOS - the amount needed to buy the same amount of EOSUSDT
            return profit_obtain

        # Conduct data analysis, reverse transaction rate, P1: EOS_USDT, P2: BTC_USDT, P3: EOS_BTC, sell EOS-> BTC, sell BTC, buy EOS (sell, sell, buy)
        if p1_buy_price / p2_sale_price < p3_sale_price:
            # Total handling fee calculation
            tax_account = (p3_buy_price * p2_buy_price + p3_buy_price * p2_buy_price + p1_sale_price) * Q3 * tax
            # Total profit calculation
            profit_sum = (p3_sale_price - p1_buy_price / p2_sale_price) * Q3 * p2_buy_price
            Log('P1;', p1_buy_price, ',P2:', p2_sale_price, ',P3:', p3_sale_price, ',tax_account:', tax_account, ',profit_sum:', profit_sum)
            # If total profit < fees, then exit directly
            if profit_sum < tax_account:
                return 0
            p3_accout_receive = p3_buy_price * Q3 * (1 - tax)  # Sell EOS to get BTC, while deducting taxes
            p1_accout_used = p1_sale_price * Q3 * (1 + tax)  # What is needed when calculating the purchase of Q3 EOSUSDT
            p2_accout_receive = p2_buy_price * p3_accout_receive * (1 - tax)  # Calculate the amount of USDT obtained from selling BTC
            # Total profit calculation
            profit_obtain = p2_accout_receive - p1_accout_used   #USDT earned from selling BTC - the amount required to buy EOS locksusdt
            return profit_obtain

        return 0

    #Loop calculation
    def profit_calculation_cycle(self):
        usdt_remain = 0
        for i in range(10000):
            profit_obtain = self.profit_calculation()
            usdt_remain = usdt_remain + profit_obtain
            if profit_obtain > 0:
                Log(u'EOS:',Q3,u'.....USDT:',usdt_remain)



def main():
    Log(exchange.GetAccount())
    Log("Test")
    fmz_market_instances = fmz_market()
    fmz_market_instances.profit_calculation_cycle()
    # fmz_market_instances.basic_data_handle(0)
```

> Detail

https://www.fmz.com/strategy/151145

> Last Modified

2019-06-11 14:24:17
