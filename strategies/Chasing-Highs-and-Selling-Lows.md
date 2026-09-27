
> Name

Chasing-Highs-and-Selling-Lows

> Author

ChildeTang



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|PERIOD|60|timeframe|
|LENGTH|1440|Length|


> Source (python)

``` python
list=[]

def doTicker():
    #Log(exchange.GetAccount())
    #Log(list)
    ticker = exchange.GetTicker()
    last = ticker.Last
    if len(list) < LENGTH:
        list.append(last)
    else:
        pMax = max(list)
        pMin = min(list)
        if last > pMax:
            Log("buy " + str(exchange.GetAccount()))
            account = exchange.GetAccount()
            if account.Balance > last:
                #id = exchange.Buy(last, 1)
                id = exchange.Buy(-1, 1)
                Log("buy id --> " + str(id))
        elif last < pMin:
            Log("sell " + str(exchange.GetAccount()))
            account = exchange.GetAccount()
            if account.Stocks > 0:
                #id = exchange.Sell(last, 1)
                id = exchange.Sell(-1, 1)
                Log("sell id --> " + str(id))
        list.pop(0)
        list.append(last)

def main():
    while(true):
        doTicker() #Execution Strategy
        Sleep(PERIOD * 1000) #Rest for a while

```

> Detail

https://www.fmz.com/strategy/96634

> Last Modified

2018-06-06 16:32:06
