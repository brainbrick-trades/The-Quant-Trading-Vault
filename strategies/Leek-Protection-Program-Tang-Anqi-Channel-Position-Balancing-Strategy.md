
> Name

Leek-Protection-Program-Tang-Anqi-Channel-Position-Balancing-Strategy

> Author

去者伯仁

> Strategy Description

Applicable to all spot currencies

In fact, what you are eating is the bull market dividend. The function of the strategy is only to reduce the retracement and avoid the plunge.
Latest backtest result: successfully avoided the crash, empty position on 4.22
![](https://www.fmz.com![IMG](https://www.fmz.com/upload/asset/11b300fd2690d0eec7869.png) ) 

Usage requirements: One percent of your funds must be able to purchase the minimum trading unit of the currency 
![](https://www.fmz.com![IMG](https://www.fmz.com/upload/asset/11b032bdb578ffad9a820.png)) 

The boss who makes money is welcome to reward me with a cup of milk tea.
![](https://www.fmz.com![IMG](https://www.fmz.com/upload/asset/11c58db65dd31bc41a6c5.jpg))




> Source (python)

``` python
'''backtest
start: 2021-04-01 00:00:00
end: 2021-04-30 23:59:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Binance","currency":"ETH_USDT","stocks":0}]
'''

import time
class juncang_strategy():  
    def __init__(self,exchange):
        self.p = 0.5
        self.account = None
        self.cny = 0
        self.btc = 0
        self.exchange =exchange
    
    #KLinear synthesis function
    def k_compose(self,Recordlist,num):
        newRecordlist = []
        for i in range(len(Recordlist)):
            if (i+1)%num == 1:
                tempk = {}
                tempk["Time"]=Recordlist[i]["Time"]
                tempk["Open"]=Recordlist[i]["Open"]
                tempk["High"]=Recordlist[i]["High"]
                tempk["Low"]=Recordlist[i]["Low"]
                tempk["Close"]=Recordlist[i]["Close"]
                tempk["Volume"]=Recordlist[i]["Volume"]
                newRecordlist.append(tempk)
            elif (i+1)%num == 0:
                if Recordlist[i]["High"]>tempk["High"]:
                    tempk["High"] = Recordlist[i]["High"]
                if Recordlist[i]["Low"]<tempk["Low"]:
                    tempk["Low"] = Recordlist[i]["Low"]
                tempk["Time"]=Recordlist[i]["Time"]
                tempk["Close"]=Recordlist[i]["Close"]
                tempk["Volume"]=tempk["Volume"]+Recordlist[i]["Volume"]
                del(newRecordlist[-1])
                newRecordlist.append(tempk)
            else:
                if Recordlist[i]["High"]>tempk["High"]:
                    tempk["High"] = Recordlist[i]["High"]
                if Recordlist[i]["Low"]<tempk["Low"]:
                    tempk["Low"] = Recordlist[i]["Low"]
                del(newRecordlist[-1])
                newRecordlist.append(tempk)
        return newRecordlist

    #Tang Anqi channel calculation to analyze the current market conditions
    def donchian(self):
        exchange.SetMaxBarLen(2000)
        temp_k = _C(self.exchange.GetRecords,PERIOD_D1)
        week_kline = self.k_compose(temp_k,7)
        rt=False
        # Log(len(week_kline),week_kline[-1]["High"],TA.Highest(week_kline, 20, 'High'))
        if len(week_kline)>20:
            if week_kline[-1]["High"]>TA.Highest(week_kline, 20, 'High'):
                rt = 'Full Position'
            elif week_kline[-1]["High"]<TA.Highest(week_kline, 20, 'High') and week_kline[-1]["Low"]>TA.MA(week_kline, 10)[-1]:
                rt = 'Equal Stock'
            elif week_kline[-1]["Low"]<TA.MA(week_kline, 10)[-1]:
                rt = 'Short position'
        else:
            rt = 'Equal Stock'
        return rt
    def cancelAllOrders(self):
        orders = self.exchange.GetOrders()
        for order in orders:
            self.exchange.CancelOrder(order['Id'], order)
        return True
    #Full position buy function
    def allin(self):
        kr =  _C(self.exchange.GetRecords,PERIOD_H1)
        account = _C(self.exchange.GetAccount)
        self.cny = account.Balance
        buynum=_N(self.cny*0.99/kr[-1].Close,3)
        if buynum>0:
            Log("Full Positionallin")
            self.exchange.Buy(kr[-1].Close,buynum)
        
    #Full position sell function
    def allout(self):
        kr =  _C(self.exchange.GetRecords,PERIOD_H1)
        account = _C(self.exchange.GetAccount)
        self.btc = _N(account.Stocks,3)
        if self.btc>0:
            Log("Short positionallout")
            self.exchange.Sell(kr[-1].Close,self.btc)
    #Equal Position Function
    def balanceAccount(self):
        kr =  _C(self.exchange.GetRecords,PERIOD_H1)
        account = _C(self.exchange.GetAccount)
        if account is None:
            return

        #Assignment
        self.account = account

        #Assignment
        self.btc = account.Stocks
        self.cny = account.Balance
        
        accountmoney=self.btc * kr[-1].Close + self.cny
        self.p = self.btc * kr[-1].Close / accountmoney
        tradenum=_N(accountmoney/kr[-1].Close/100,3)
        if tradenum<0.001:
            tradenum=0.001
        #Judgmentself.pWhether the value is less than0.48
        # Log(self.p)
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

            self.exchange.Sell(kr[-1].Close, _N(tradenum*10,3))

            Log("Number of Coins Held:",self.btc,"Amount of Cash:",self.cny)
        elif (self.p <= 0.45):
            #CallLogFunction and pass in parameters"Start balancing", self.p
            Log("Start balancing, quick build position", self.p)

            self.exchange.Buy(kr[-1].Close, _N(tradenum*10,3))

            Log("Number of Coins Held:",self.btc,"Amount of Cash:",self.cny)
    #Trading Loop
    def loop(self):
        self.cancelAllOrders()
        rt=self.donchian()
        if rt=='Full Position':
            self.allin()
        elif rt=='Equal Stock':
            self.balanceAccount()
        else:
            self.allout()
        Sleep(1000*60)




#Functionmain
def main():
    #reaper Is Instance of Constructor
    reaper = juncang_strategy(exchange)
    while (True):
        reaper.loop()

```

> Detail

https://www.fmz.com/strategy/271523

> Last Modified

2021-07-20 17:27:39
