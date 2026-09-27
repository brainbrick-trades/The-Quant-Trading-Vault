
> Name

Automatically-Retrieve-Minimum-Opening-Unit-Precision-for-Binance-Perpetual-Contracts-Abandoned

> Author

GCC

> Strategy Description

    Originally, directly obtaining trading precision from the trading rules was reasonable, but Binance often does not update this promptly, so it was abandoned.



> Source (python)

``` python
def init():
    global symbols, min_value
    # Get Trading Rules
    exchange.SetBase('https://dapi.binance.com')
    rule = exchange.IO("api", "GET", "/dapi/v1/exchangeInfo", "", "")["symbols"]
    Log(rule)
    # Get trading pair name
    for i in range(len(exchanges)):
        exchanges[i].SetMarginLevel(M)
        exchanges[i].SetContractType("swap")  # Set Perpetual Contract
        _symbol = exchanges[i].GetCurrency().split("_")[0]   # +'USDT'Coin-margined trading pair name
        # Set Trading Precision
        j = 0
        flag1 = False
        flag2 = False
        #Log(rule)
        while (j < len(rule)) and flag1 == False and flag2 == False:
            if str(rule[j]["symbol"]).rfind(_symbol)>=0:
                for x in rule[j]["filters"]:
                    if x["filterType"] == "PRICE_FILTER" and flag1 == False:
                        #Log("Price",x["tickSize"])
                        #Log(len(str(float(x["tickSize"])).split('.')[-1]))
                        price_precision = len(str(float(x["tickSize"])).split('.')[-1])
                        flag1 = True
                    elif x["filterType"] == "LOT_SIZE" and flag2 == False:
                        amount_precision = len(x["minQty"].split('.')[-1])
                        flag2 = True
            j = j + 1
        exchanges[i].SetPrecision(price_precision, amount_precision)
    Log("initialization finished")
```

> Detail

https://www.fmz.com/strategy/322632

> Last Modified

2021-11-12 15:44:44
