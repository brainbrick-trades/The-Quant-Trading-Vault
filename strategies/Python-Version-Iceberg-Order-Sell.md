
> Name

Python-Version-Iceberg-Order-Sell

> Author

发明者量化-小小梦

> Strategy Description

Teaching strategy, related article link:https://www.fmz.com/bbs-topic/5080

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|TotalSellStocks|10|Total quantity sold (coins))|
|AvgSellOnce|0.3|Average quantity per sale (Coin))|
|FloatPoint|10|Single average floating point number (percentage)|
|EntrustDepth|0.1|Order depth (percentage)|
|MinSellPrice|3800|Lowest sell price (yuan)|
|Interval|1000|Retry on failure (milliseconds))|
|MinStock|0.0001|Minimum transaction volume|
|LoopInterval|300|Price polling interval (milliseconds)|


> Source (python)

``` python
import random

def CancelPendingOrders():
    while True:
        orders = _C(exchange.GetOrders)
        if len(orders) == 0:
            return
        
        for j in range(len(orders)):
            exchange.CancelOrder(orders[j]["Id"])
            if j < len(orders) - 1:
                Sleep(Interval)

LastSellPrice = 0
InitAccount = None

def dispatch():
    global LastSellPrice, InitAccount
    account = None
    ticker = _C(exchange.GetTicker)
    LogStatus(_D(), "ticker:", ticker)
    if LastSellPrice > 0:
        if len(_C(exchange.GetOrders)) > 0:
            if ticker["Last"] < LastSellPrice and ((LastSellPrice - ticker["Last"]) / ticker["Last"]) > (2 * (EntrustDepth / 100)):
                Log("Too much deviation, latest transaction price:", ticker["Last"], "order price", LastSellPrice)
                CancelPendingOrders()
            else :
                return True
        else :
            account = _C(exchange.GetAccount)
            Log("Buy order completed, cumulative sales:", _N(InitAccount["Stocks"] - account["Stocks"]), "Average selling price:", _N((account["Balance"] - InitAccount["Balance"]) / (InitAccount["Stocks"] - account["Stocks"])))
            LastSellPrice = 0

    SellPrice = _N(ticker["Sell"] * (1 + EntrustDepth / 100))
    if SellPrice < MinSellPrice:
        return True

    if not account:
        account = _C(exchange.GetAccount)

    if (InitAccount["Stocks"] - account["Stocks"]) >= TotalSellStocks:
        return False 

    RandomAvgSellOnce = (AvgSellOnce * ((100.0 - FloatPoint) / 100.0)) + (((FloatPoint * 2) / 100.0) * AvgSellOnce * random.random())
    SellAmount = min(TotalSellStocks - (InitAccount["Stocks"] - account["Stocks"]), RandomAvgSellOnce)
    if SellAmount < MinStock:
        return False 

    LastSellPrice = SellPrice
    exchange.Sell(SellPrice, SellAmount, "Last transaction price", ticker["Last"])
    return True

def main():
    global InitAccount, LoopInterval
    CancelPendingOrders()
    InitAccount = _C(exchange.GetAccount)
    Log(InitAccount)
    if InitAccount["Stocks"] < TotalSellStocks:
        raise Exception("Insufficient coins in the account")
    LoopInterval = max(LoopInterval, 1)
    while dispatch():
        Sleep(LoopInterval)
    Log("All commissions completed", _C(exchange.GetAccount))


```

> Detail

https://www.fmz.com/strategy/188754

> Last Modified

2020-03-07 16:57:48
