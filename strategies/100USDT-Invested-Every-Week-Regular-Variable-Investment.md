
> Name

100USDT-Invested-Every-Week-Regular-Variable-Investment

> Author

jfyh5388

> Strategy Description

Fixed investment of about 100 USDT every week, with no fixed amount on a regular basis. Buy more when it goes down, buy less when it goes up, and the rate of return is better than the fixed amount.



> Source (python)

``` python
def main():
    amountAll = 0                                              #Total Holdings
    cost = 0                                                   #Cost
    marketValueCurrent = 0                                     #Current total market value of holdings
    marketValueExpected = 0                                    #Current expected total market capitalization
    rateOfReturn = 0                                           #Yield
    eachBuy = 100
    while True:
        marketValueExpected = marketValueExpected + eachBuy        #Calculate the current expected total market value
        ticker = exchange.GetTicker()
        price = ticker['Last']                                 #Get current price
        amount = marketValueExpected / price - amountAll       #Calculate the purchase amount this time
        if amount > 0:
            exchange.Buy(price,amount)                         #buy         
        else:
            amount = 0
        amountAll = amountAll + amount                         #Calculate total holding amount
        cost = cost + amount * price                           #Calculate total cost
        marketValueCurrent = amountAll * price                 #Calculate the current total market value held
        rateOfReturn = (marketValueCurrent - cost) / cost      #Calculate return rate
        Log("Amount invested this time:", amount * price, "Principal:", cost,"Current total holdings", amountAll,"Current total market value:", marketValueCurrent, "Yield:", rateOfReturn * 100,"%" ,"Current Price:", price, )
        Sleep(7 * 24 * 60 * 60 * 1000)                         #Wait for a Week
                    
```

> Detail

https://www.fmz.com/strategy/260056

> Last Modified

2021-04-16 16:54:06
