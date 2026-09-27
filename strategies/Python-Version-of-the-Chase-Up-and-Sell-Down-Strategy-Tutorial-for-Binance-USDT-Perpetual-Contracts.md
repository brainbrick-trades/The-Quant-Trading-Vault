
> Name

Python-Version-of-the-Chase-Up-and-Sell-Down-Strategy-Tutorial-for-Binance-USDT-Perpetual-Contracts

> Author

韬奋量化

> Strategy Description

Original code is the spot version:
https://www.fmz.com/bbs-topic/4908

Now switching to contract version.

---- Taofen Quantitative (WeChat):himandy)


A good trading platform can make your strategy soar to 90,000 miles. Register through the link to get a two-month VIP5 handling rate discount.:
(Spot: 0% for pending orders and 0.07% for take orders. Contract: 0% for pending orders, take orders0.04%)
https://www.kucoin.cc/ucenter/signup?rcode=1wxJ2fQ&lang=zh_CN&utmsource=VIP_TF

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|leverage|true|Leverage multiple|
|StopGain|0.05|take profit rate|
|StopLoss|0.05|stop loss rate|


> Source (python)

``` python
'''backtest
start: 2021-05-01 00:00:00
end: 2021-05-29 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
'''

# Original code is the spot version:
# https://www.fmz.com/bbs-topic/4908

# Now switching to contract version.

# ---- Taofen Quantitative (WeChat):himandy)


# A good trading platform can make your strategy soar to 90,000 miles. Register through the link to get a two-month VIP5 handling rate discount.:
# (Spot: 0% for pending orders and 0.07% for take orders. Contract: 0% for pending orders, take orders0.04%)
# https://www.kucoin.cc/ucenter/signup?rcode=1wxJ2fQ&lang=zh_CN&utmsource=VIP_TF

import time

basePrice = -1
ratio = 0.05
acc = _C(exchange.GetAccount)
pos = _C(exchange.GetPosition)
lastCancelAll = 0
minStocks = 0.01

def CancelAll():
    while True : 
        orders = _C(exchange.GetOrders)
        for i in range(len(orders)) :
            exchange.CancelOrder(orders[i]["Id"], orders[i])
        if len(orders) == 0 :
            break
        Sleep(1000)

def main():
    global basePrice, acc, lastCancelAll, leverage, StopGain, StopLoss
    #Log(StopLoss * -1)
    exchange.SetContractType("swap")
    exchange.SetMarginLevel(leverage)
    exchange.SetPrecision(2, 3)
    pos = _C(exchange.GetPosition)
    while True:
        ticker = _C(exchange.GetTicker)
        if basePrice == -1 :
            basePrice = ticker.Last
        if ticker.Last - basePrice > 0 and (ticker.Last - basePrice) / basePrice > ratio :
            acc = _C(exchange.GetAccount)            
            if acc.Balance * ratio * leverage / ticker.Last > minStocks and len(pos) == 0:
                exchange.SetDirection("buy")
                exchange.Buy(_N(ticker.Last, 2), _N(acc.Balance * ratio / ticker.Last, 3))
                basePrice = ticker.Last
                ts = time.time()
                if ts - lastCancelAll > 60 * 5 :
                    CancelAll()
                    lastCancelAll = ts
                pos = _C(exchange.GetPosition)
        if ticker.Last - basePrice < 0 and (basePrice - ticker.Last) / basePrice > ratio : 
            acc = _C(exchange.GetAccount)
            pos = _C(exchange.GetPosition)
            if acc.Balance * ratio * leverage / ticker.Last > minStocks and len(pos) == 0:
                exchange.SetDirection("sell")
                exchange.Sell(_N(ticker.Last, 2), _N(acc.Balance * ratio / ticker.Last, 3))
                basePrice = ticker.Last
                ts = time.time()
                if ts - lastCancelAll > 60 * 5 :
                    CancelAll()
                    lastCancelAll = ts
                pos = _C(exchange.GetPosition)
        if len(pos) == 1 :
        	#Log(pos)
            if pos[0]["Profit"] / pos[0]["Margin"] > StopGain :
                if pos[0]["Type"] == 0 :
                    exchange.SetDirection("closebuy")
                    exchange.Sell(-1, pos[0]["Amount"])
                    pos = _C(exchange.GetPosition)
                elif pos[0]["Type"] == 1 :
                    exchange.SetDirection("closesell")
                    exchange.Buy(-1, pos[0]["Amount"])
                    pos = _C(exchange.GetPosition)
            elif pos[0]["Profit"] / pos[0]["Margin"] < StopLoss * -1 :
                if pos[0]["Type"] == 0 :
                    exchange.SetDirection("closebuy")
                    exchange.Sell(-1, pos[0]["Amount"])
                    pos = _C(exchange.GetPosition)
                elif pos[0]["Type"] == 1 :
                    exchange.SetDirection("closesell")
                    exchange.Buy(-1, pos[0]["Amount"])
                    pos = _C(exchange.GetPosition)

        LogStatus(_D(), "\n", "Market information:",Tiker,"\n", "Account information.":", acc)
        if exchange.GetName() == "Futures_Binance" and IsVirtual() == false :
            LogProfit(_N(float(acc["Info"]["totalWalletBalance"], 4)))
        Sleep(500)
```

> Detail

https://www.fmz.com/strategy/286091

> Last Modified

2021-05-30 16:35:25
