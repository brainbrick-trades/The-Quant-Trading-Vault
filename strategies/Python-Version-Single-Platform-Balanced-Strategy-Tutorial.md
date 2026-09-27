
> Name

Python-Version-Single-Platform-Balanced-Strategy-Tutorial

> Author

发明者量化-小小梦

> Strategy Description

Quoted from the single-platform balanced strategy in JavaScript version
> This requires opening a position. For example, the account has 5,000 yuan and 1 coin. If the value of the coin is greater than the account balance of 5,000 and the price difference exceeds the threshold, for example, the currency is now worth 6,000 yuan, sell it (600 0-5000)/6000/2 coins, it means the currency has appreciated, exchange the money back. If the currency has depreciated, for example, 4000 yuan, buy (5000-4000)/4000/2 coins, When the currency falls, buy some back, and if it rises again, sell it again. It's like a balance, with different hedging on both sides, so I named it a balanced strategy.

Article address: https://www.fmz.com/bbs-topic/4986

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|threshold|0.05|Threshold|
|Interval|2000|Error retry interval (milliseconds)|
|LoopInterval|60|Polling interval (seconds)|
|MinStock|0.001|Minimum transaction volume|
|XPrecision|4|quantity precision|
|ZPrecision|8|Price Precision|


> Source (python)

``` python
'''backtest
start: 2019-12-01 00:00:00
end: 2020-02-01 11:00:00
period: 1m
exchanges: [{"eid":"OKEX","currency":"BTC_USDT","stocks":1}]
'''

InitAccount = None

def CancelPendingOrders():
    ret = False
    while True:
        orders = _C(exchange.GetOrders)
        if len(orders) == 0 :
            return ret

        for j in range(len(orders)):
            exchange.CancelOrder(orders[j].Id)
            ret = True
            if j < len(orders) - 1:
                Sleep(Interval)
    return ret 

def onTick():
    acc = _C(exchange.GetAccount)
    ticker = _C(exchange.GetTicker)
    spread = ticker.Sell - ticker.Buy
    diffAsset = (acc.Balance - (acc.Stocks * ticker.Sell)) / 2
    ratio = diffAsset / acc.Balance
    LogStatus("ratio:", ratio, _D())
    if abs(ratio) < threshold:
        return False
    if ratio > 0 :
        buyPrice = _N(ticker.Sell + spread, ZPrecision)
        buyAmount = _N(diffAsset / buyPrice, XPrecision)
        if buyAmount < MinStock:
            return False
        exchange.Buy(buyPrice, buyAmount, diffAsset, ratio)
    else :
        sellPrice = _N(ticker.Buy - spread, ZPrecision)
        sellAmount = _N(-diffAsset / sellPrice, XPrecision)
        if sellAmount < MinStock:
            return False 
        exchange.Sell(sellPrice, sellAmount, diffAsset, ratio)
    return True

def main():
    global InitAccount, LoopInterval
    InitAccount = _C(exchange.GetAccount)
    LoopInterval = max(LoopInterval, 1)
    while True:
        if onTick():
            Sleep(1000)
            CancelPendingOrders()
            Log(_C(exchange.GetAccount))
        Sleep(LoopInterval * 1000)
```

> Detail

https://www.fmz.com/strategy/183374

> Last Modified

2020-02-05 10:19:20
