
> Name

Zichen-Quantitative-Shannon-Grid-Trading-Strategy

> Author

子辰量化



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|totalInvestment|10000|Total Investment Amount|
|buyRatio|0.02|How much does it fall to buy?|
|sellRatio|0.02|Sell by how much it rises|


> Source (python)

``` python
##
# Shannon Grid Trading Strategy (Public Version))
# Author: Zichen Quantification
# Last Modified: 2024-1-4
##

import time

assetRatio = 0.5 # Asset investment ratio

originalTotalMoney = totalInvestment # Base investment amount, total investment amount + all equity after profits and losses.
originalAssetMoney = totalInvestment * assetRatio # Base asset value
originalCashMoney = totalInvestment * (1 - assetRatio) # Base Cash

remainCashMoney = originalCashMoney # Current remaining cash
investAssetMoney = 0 # Current asset value
inverstAssetAmount = 0 # Current asset quantity

boolInited = False # Has the first position been completed?

i = 0 # tickCalculation

def num_cut(num, c):
    str_num = str(num)
    return float(str_num[:str_num.index('.') + 1 + c])

def onTick():
    global assetRatio
    global originalTotalMoney
    global originalAssetMoney
    global originalCashMoney
    global remainCashMoney
    global investAssetMoney
    global inverstAssetAmount
    global boolInited
    global i

    ticker = exchange.GetTicker()
    # Log(ticker)
    openTime = time.localtime(ticker.Time / 1000) # ticker time
    openTimeStr = time.strftime("%Y-%m-%dT%H:%M:%S", openTime) 
    price = ticker.Last

    # Initial position opening
    if not boolInited:
        money = originalAssetMoney
        id = exchange.Buy(-1, money) # market order
        # Log("order id:", id)
        order = exchange.GetOrder(id)
        Log("buy money:", money)
        Log("order id:", order["Id"], "Price:", order["Price"], "Amount:", order["Amount"], "DealAmount:", order["DealAmount"], "AvgPrice:", order["AvgPrice"], "Status:", order["Status"], "Type:", order["Type"])
        money = order["Amount"] # Transactionmoney
        dealAmount = order["DealAmount"] # The number of assets after deducting handling fees
        price = order["AvgPrice"] # Average Transaction Price
        investAssetMoney = originalAssetMoney
        remainCashMoney = originalCashMoney
        inverstAssetAmount = dealAmount       
        boolInited = True
        Log(f"use ${investAssetMoney} buy {inverstAssetAmount} asset at price ${price} at time {openTimeStr}")

        Log(f"{i} summary:")
        originalTotalMoney = originalAssetMoney + originalCashMoney
        investAssetMoney = inverstAssetAmount * price
        currentTotalMoney = investAssetMoney + remainCashMoney
        Log(f"originalAssetMoney: ${originalAssetMoney}")
        Log(f"originalCashMoney: ${originalCashMoney}")
        Log(f"originalTotalMoney: ${originalTotalMoney}")
        Log(f"inverstAssetAmount: ${inverstAssetAmount}")
        Log(f"investAssetMoney: ${investAssetMoney}")
        Log(f"remainCashMoney: ${remainCashMoney}")
        Log(f"currentTotalMoney: ${currentTotalMoney}")
        # account = exchange.GetAccount()
        # Log("Balance:", account["Balance"], "FrozenBalance:", account["FrozenBalance"], "Stocks:", account["Stocks"], "FrozenStocks:", account["FrozenStocks"])

    # buy
    money = inverstAssetAmount * price # pirce
    if money < originalAssetMoney * (1 - buyRatio):
        money = originalAssetMoney * buyRatio / 2 # Purchase amount
        account = exchange.GetAccount()
        if remainCashMoney > money and account["Balance"] > money: # Check if there is enough cash, double-check
            # amount = money / price
            id = exchange.Buy(-1, money) # market order
            # Log("order id:", id)
            order = exchange.GetOrder(id)
            Log("buy money:", money)
            Log("order id:", order["Id"], "Price:", order["Price"], "Amount:", order["Amount"], "DealAmount:", order["DealAmount"], "AvgPrice:", order["AvgPrice"], "Status:", order["Status"], "Type:", order["Type"])
            money = order["Amount"] # Transactionmoney
            dealAmount = order["DealAmount"] # The number of assets after deducting handling fees
            price = order["AvgPrice"] # Average Transaction Price  
            originalAssetMoney -= money #
            originalCashMoney -= money #
            remainCashMoney -= money
            inverstAssetAmount = inverstAssetAmount + dealAmount
            Log(f"bull/bear buy {dealAmount} asset at ${price} at time {openTimeStr}")

            Log(f"{i} summary:")
            originalTotalMoney = originalAssetMoney + originalCashMoney
            investAssetMoney = inverstAssetAmount * price
            currentTotalMoney = investAssetMoney + remainCashMoney
            Log(f"originalAssetMoney: ${originalAssetMoney}")
            Log(f"originalCashMoney: ${originalCashMoney}")
            Log(f"originalTotalMoney: ${originalTotalMoney}")
            Log(f"inverstAssetAmount: ${inverstAssetAmount}")
            Log(f"investAssetMoney: ${investAssetMoney}")
            Log(f"remainCashMoney: ${remainCashMoney}")
            Log(f"currentTotalMoney: ${currentTotalMoney}")
            # account = exchange.GetAccount()
            #Log("Balance:", account["Balance"], "FrozenBalance:", account["FrozenBalance"], "Stocks:", account["Stocks"], "FrozenStocks:", account["FrozenStocks"])

    # sell
    money = inverstAssetAmount * price # pirce
    if money > (originalAssetMoney * (1 + sellRatio)):
        money = originalAssetMoney * sellRatio / 2 # Selling amount
        amount = money / price
        id = exchange.Sell(-1, amount) # market order
        # Log("order id:", id)
        order = exchange.GetOrder(id)
        Log("sell money:", money)
        Log("sell amount:", amount)
        Log("order id:", order["Id"], "Price:", order["Price"], "Amount:", order["Amount"], "DealAmount:", order["DealAmount"], "AvgPrice:", order["AvgPrice"], "Status:", order["Status"], "Type:", order["Type"])
        amount = order["Amount"] # Planned quantity of assets sold
        dealAmount = order["DealAmount"] # The amount of transaction assets, does this seem to be the handling fee deducted from the balance??
        # According to the logs, amount == dealAmount, so fees are deducted from the balance.
        price = order["AvgPrice"] # Average Transaction Price
        dealMoney = dealAmount * price # No handling fee deducted
        remainCashMoney += dealMoney # Here, the handling fee needs to be deducted
        originalAssetMoney += money #
        originalCashMoney += money #
        inverstAssetAmount = inverstAssetAmount - dealAmount
        Log(f"bull/bear sell {amount} asset at ${price} at time {openTimeStr}")

        Log(f"{i} summary:")
        originalTotalMoney = originalAssetMoney + originalCashMoney
        investAssetMoney = inverstAssetAmount * price
        currentTotalMoney = investAssetMoney + remainCashMoney
        Log(f"originalAssetMoney: ${originalAssetMoney}")
        Log(f"originalCashMoney: ${originalCashMoney}")
        Log(f"originalTotalMoney: ${originalTotalMoney}")
        Log(f"inverstAssetAmount: ${inverstAssetAmount}")
        Log(f"investAssetMoney: ${investAssetMoney}")
        Log(f"remainCashMoney: ${remainCashMoney}")
        Log(f"currentTotalMoney: ${currentTotalMoney}")
        # account = exchange.GetAccount()
        # Log("Balance:", account["Balance"], "FrozenBalance:", account["FrozenBalance"], "Stocks:", account["Stocks"], "FrozenStocks:", account["FrozenStocks"])

    # tickCount
    i = i + 1

def main():
    Log(totalInvestment, buyRatio, sellRatio)

    while True:
        onTick()
        Sleep(1000) # 1second

def onexit():
    global inverstAssetAmount

    # close all positions
    Log("close all positions")
    if inverstAssetAmount > 0:
        amount = num_cut(inverstAssetAmount * (1-0.0001), 8) # Leave a tiny 0.01%, control decimal places
        id = exchange.Sell(-1, amount) # market order
        Log("order id:", id)
        order = exchange.GetOrder(id)
        Log("order id:", order["Id"], "Price:", order["Price"], "Amount:", order["Amount"], "DealAmount:", order["DealAmount"], "AvgPrice:", order["AvgPrice"], "Status:", order["Status"], "Type:", order["Type"])        
    # Countdown
    beginTime = time.time() * 1000
    while True:
        ts = time.time() * 1000
        Log("Program stops countdown...,has passed:", (ts - beginTime) / 1000, "second!")
        Sleep(1000) # 1second

```

> Detail

https://www.fmz.com/strategy/425193

> Last Modified

2024-03-20 14:21:21
