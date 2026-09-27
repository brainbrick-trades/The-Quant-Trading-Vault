
> Name

Iceberg-Commissioned-Purchase-Jason

> Author

Jason_MJ

> Strategy Description

**1. Premise:**
    First time learning to write strategies -- Iceberg Order:
    This article mainly refers to the strategy of experts:https://www.fmz.com/strategy/188435
Largely similar to the strategies of experts, but the writing is rougher. Mainly used for learning and getting started. Looking forward to guidance.

**2.Cause**
    When buying or selling digital currencies in large amounts, the large transaction amount may affect the market price of the currency you want to buy/sell. This is even more true for digital currencies with poor liquidity. A large buy order can ** pull the market **, and a large sell order can ** destroy the market.**.
    ①Pumping: driving the price up to raise the coin's price
    ②Smashing: selling the currency directly regardless of the price, causing the currency price to fall.
    ③Trading Currency Stocks: The currency used for trading. For example, in the BTC/USDT trading pair, **BTC is the trading currency**
    ④Pricing currency Balance: The currency denominated by the user, taking the BTC/USDT trading pair as an example, **USDT is the pricing currency**

**Iceberg order:**
    Operation: refers to automatically splitting a large order into **multiple orders**, and automatically placing small orders based on the current latest buy/sell price and the price strategy set by the customer. **When the previous order is fully traded or the latest price deviates significantly from the current order, the order is automatically re-placed.**
    Effect: Reduce the impact of large buy/sell orders on the market price. When making large purchases, you can **prevent your own buying costs from increasing due to price increases due to large buy orders**; when selling large amounts, you can **prevent your selling profits from lowering prices due to large sell orders.**

**Data parameter comparison:**
1. Order price = latest buy 1 price X (1 - order depth))
2. Actual market order depth = (last transaction price - previous order price) / previous order price.
3. Random single purchase quantity = average single purchase quantity X (100 - single average floating point number) % + (single average floating point number X2) %0~1
4. Available Amount = Obtain the account pricing currency, randomly purchase the quantity per transaction, and the minimum remaining total amount to purchase
5. Purchase quantity = available amount / order price
6. Total remaining purchase amount = total purchase amount - (initial account denominated currency - account denominated currency)


**Rules:**
1. Automatically cancel the order when the latest transaction price deviates from the order by more than X2 of the order depth (indicating the deviation is too large))
2. Stop the order when the total trading volume of the strategy is equal to the total order quantity
3. Stop orders if the latest transaction price exceeds the maximum buy limit
4. Restore the order when the latest transaction price is lower than the maximum buying price

**Main parameters:**
1. Purchase amount
2. Single purchase quantity
3. Commission Depth
4. Highest price
5. Price polling interval
6. Average single purchase quantity as a float
7. Minimum transaction volume

**Thought Process:**
1. Retrieve all unfilled orders and cancel orders
2. Get the initial account balance and determine whether it is greater than the total purchase amount
3. Calculate the order price
4. Calculate single purchase quantity
5. Calculate available amount
6. Calculate purchase quantity
7. Execute purchase
8. Rest for a specified time
9. Determine whether the last order was successfully purchased
10. Successfully output log
11. Determine if the deviation is too large; if too large, cancel

**Suggestion**
1. It is recommended to backtest with ETH_USDT

**Strategy is not perfect, hope passing experts can offer guidance**

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|buyAmount|10000|Purchase amount|
|buyNum|100|Average quantity per single purchase|
|depthStatus|0.1|Commission Depth|
|highPrice|20000|Highest price|
|priceInterval|true|Query price interval|
|minBuyNum|0.0001|Minimum transaction volume|
|buyOncePoint|10|Average single purchase quantity as a float|


> Source (python)

``` python
import random


def main():
    # Get all pending orders of the account
    Log("Cancel all unfilled orders")
    orders = _C(exchange.GetOrders)
    if len(orders) > 0:
        for i in range(len(orders)):
            exchange.CancelOrder(orders[i]["Id"])
            Sleep(priceInterval*1000)

    # Compare account balance
    Log("Get user's initialized account")
    initAccount = _C(exchange.GetAccount)
    if initAccount["Balance"] < buyAmount:
        Log("Insufficient account balance")
        return
    
    #Compare the average quantity of a single purchase*Whether the market's best bid price is greater than the account balance
    ticker = _C(exchange.GetTicker)
    if (ticker['Last'] * buyNum) > initAccount['Balance']:
        Log("The average price of a single purchase is higher than the account balance, please adjust the parameters")
        return

    lastBuyPrice = 0

    while (True):
        Sleep(priceInterval*1000)
        #Get account information
        account = _C(exchange.GetAccount)
        #Get current market
        ticker = _C(exchange.GetTicker)
        # Last time the purchase price was not empty, check if the order was completed; if not, cancel
        if lastBuyPrice > 0:
            orders1 = exchange.GetOrders()
            if len(orders1) > 0:
                for j in range(len(orders1)):
                    #Calculate the actual market order depth
                    if ticker["Last"] > lastBuyPrice and ((ticker["Last"] - lastBuyPrice)/lastBuyPrice) > (2* (depthStatus/100)):
                        Log("Order price deviates too much, latest transaction price:",ticker["Last"],"order price",lastBuyPrice)
                        exchange.CancelOrder(orders1[j]["Id"])
                        lastBuyPrice = 0
                continue
            else:
                Log("Buy order completed, Total cost:", _N(initAccount["Balance"] - account["Balance"]), "Average buying price:", _N((initAccount["Balance"] - account["Balance"]) / (account["Stocks"] - initAccount["Stocks"])))
                lastBuyPrice = 0
                continue     
        else:
            Log("Remaining balance:",account["Balance"])
            #Order price = Latest best buy price*(1-Commission Depth/100)
            entrustPrice = _N(ticker["Buy"]*(1-depthStatus/100))
            Log("Order price:",entrustPrice)
            #Determine if the order price is higher than the maximum price limit
            if entrustPrice > highPrice:
                continue
            #Random purchase quantity = Average quantity per transaction * ((100-Single average float)/100)+(Single average float*2 /100* Average quantity per transaction *random number0~1)  
            randomBuyNum = (buyNum*((100-buyOncePoint)/100))+(buyOncePoint*2/100 *buyNum*random.random())
            #Available quantity and amount 
            useMoney = min(account["Balance"],randomBuyNum,buyAmount - (initAccount["Balance"] - account["Balance"]))
            #Purchase quantity
            orderBuyNum = _N(useMoney/entrustPrice)
            Log("Transaction quantity:",orderBuyNum)
            #Determine whether it is less than the minimum trading volume
            if orderBuyNum < minBuyNum:
                break
            #Because fees need to be deducted, roughly for the account99.7%
            if (entrustPrice*orderBuyNum)>(account["Balance"]*0.997):
                Log("Amount is",(entrustPrice*orderBuyNum))
                Log("Account balance is",(account["Balance"]))
                continue
            #Update last purchase price
            lastBuyPrice = entrustPrice
            #Place Order
            exchange.Buy(entrustPrice,orderBuyNum)
            
    account = _C(exchange.GetAccount)  
    Log("Iceberg order buy completed,Total cost:",_N(initAccount["Balance"]-account["Balance"]),"Average unit price is:",_N((initAccount["Balance"]-account["Balance"])/(account["Stocks"]-initAccount["Stocks"])))        

```

> Detail

https://www.fmz.com/strategy/271475

> Last Modified

2021-04-16 10:26:23
