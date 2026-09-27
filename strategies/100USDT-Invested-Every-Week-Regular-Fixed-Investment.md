
> Name

100USDT-Invested-Every-Week-Regular-Fixed-Investment

> Author

jfyh5388

> Strategy Description

Invest 100 USDT weekly, with fixed periodic amounts



> Source (python)

``` python
def main():
    amountAll = 0                                              #Total Holdings
    cost = 0                                                   #Cost
    marketValueCurrent = 0                                     #Current total market value of holdings
    rateOfReturn = 0                                           #Yield
    while True:
        ticker = exchange.GetTicker()
        price = ticker['Last']                                 #Get current price
        amount = 100 / price                                   #Calculate the purchase amount this time
        exchange.Buy(price,amount)                             #buy
        amountAll = amountAll + amount                         #Calculate total holding amount
        cost = cost + 100                                      #Calculate total cost
        marketValueCurrent = amountAll * price                 #Calculate the current total market value held
        rateOfReturn = (marketValueCurrent - cost) / cost      #Calculate return rate        
        Log("Amount invested this time:", 100, "Principal:", cost, "Current total market value:", marketValueCurrent, "Yield:", rateOfReturn * 100,"%","Current Price",price)
        Sleep(7 * 24 * 60 * 60 * 1000)                         #Wait for a Week
                    
```

> Detail

https://www.fmz.com/strategy/260013

> Last Modified

2021-04-06 08:35:55
