
> Name

Averaging-Strategy

> Author

去者伯仁

> Strategy Description

When encountering a faith coin but worried about holding it, use an averaging strategy: fully auto high sell and low buy, always keeping the value of the coin and U balanced.
Only supports cryptocurrency spot
One percent of your funds must be able to buy the minimum transaction amount of the currency



> Source (python)

``` python
'''backtest
start: 2020-04-03 00:00:00
end: 2021-04-02 23:59:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Binance","currency":"BTC_USDT","stocks":0}]
'''

import time
class juncang_strategy():  
    def __init__(self,exchange):
        self.p = 0.5
        self.account = None
        self.cny = 0
        self.btc = 0
        self.exchange =exchange
        #All of the aboveselfobject properties

    def cancelAllOrders(self):
        orders = _C(self.exchange.GetOrders)
        for order in orders:
            exchange.CancelOrder(order['Id'], order)
        return True


    def balanceAccount(self):
        self.cancelAllOrders()

        kr =  _C(self.exchange.GetRecords,PERIOD_M1)
        account = _C(self.exchange.GetAccount)
        if account is None:
            return

        #Assignment
        self.account = account

        #Assignment
        self.btc = account.Stocks+account.FrozenStocks
        self.cny = account.Balance+account.FrozenBalance
        
        accountmoney=self.btc * kr[-1].Close + self.cny
        self.p = self.btc * kr[-1].Close / accountmoney
        # Log(self.p)
        tradenum=accountmoney/kr[-1].Close/100
        if tradenum<0.001:
            tradenum=0.001
        #Judgmentself.pWhether the value is less than0.48
        Log(self.p)
        if (0.45<self.p < 0.49):
            #CallLogFunction and pass in parameters"Start balancing", self.p
            Log("Start balancing", self.p)

            self.exchange.Buy(kr[-1].Close, tradenum)

            Log("Number of Coins Held:",self.btc,"Amount of Cash:",self.cny)

            #Judgmentself.pWhether the value is greater than0.52
        elif (0.55 > self.p > 0.51):
            #CallLogFunction and pass in parameters"Start balancing", self.p
            Log("Start balancing", self.p)

            #CallSellFunction and pass in the corresponding parameters
            self.exchange.Sell(kr[-1].Close, tradenum)

            Log("Number of Coins Held:",self.btc,"Amount of Cash:",self.cny)
        elif (self.p >= 0.55):
            #CallLogFunction and pass in parameters"Start balancing", self.p
            Log("Start balancing,Quick close position", self.p)

            self.exchange.Sell(kr[-1].Close, tradenum*10)

            Log("Number of Coins Held:",self.btc,"Amount of Cash:",self.cny)
        elif (self.p <= 0.45):
            #CallLogFunction and pass in parameters"Start balancing", self.p
            Log("Start balancing, quick build position", self.p)

            self.exchange.Buy(kr[-1].Close, tradenum*10)

            Log("Number of Coins Held:",self.btc,"Amount of Cash:",self.cny)




#Functionmain
def main():
    #reaper Is Instance of Constructor
    reaper = juncang_strategy(exchange)
    while (True):
        #Call through instancepollMethod
        reaper.balanceAccount()
        Sleep(1000*10)

```

> Detail

https://www.fmz.com/strategy/266142

> Last Modified

2021-05-12 11:32:05
