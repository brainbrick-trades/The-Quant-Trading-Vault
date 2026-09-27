
> Name

Share-Strategies-for-Grabbing-New-Spot-Products

> Author

盯盘狗 - 策略出租





> Source (python)

``` python
import time

# Initialize strategy parameters
symbol = 'huobip/ht_usdt'
amount = 10
max_price = 1.5
min_price = 0.5
interval = 0.1

# ConnectAPI
exchange = Exchange()
exchange.SetContractType(symbol)

# Main loop
while True:
    # Get current market depth
    depth = exchange.GetDepth()

    # Get the current best bid and ask prices
    buy_price = float(depth['Bids'][0]['Price'])
    sell_price = float(depth['Asks'][0]['Price'])

    # Determine whether conditions are met
    if buy_price <= max_price and sell_price >= min_price:
        # If the conditions are met, execute a buy operation
        buy_amount = amount / buy_price
        exchange.Buy(buy_price, buy_amount)
        print('Buy', buy_amount, 'HT, price', buy_price)

        # Wait for a period of time before executing the sell operation
        time.sleep(interval)
        sell_price = float(depth['Asks'][0]['Price'])
        sell_amount = amount / sell_price
        exchange.Sell(sell_price, sell_amount)
        print('Sell', sell_amount, 'HT, at price', sell_price)

    # Wait for next loop
    time.sleep(1)


#This strategy usesFMZProvided by the platformExchange APIto trade. In the main loop, first get the current market depth, then get the current bid and ask prices. If the buying price is less than or equal to the set maximum price and the selling price is greater than or equal to the set minimum price, a buying operation is performed. Wait for a period of time and then obtain the current selling price to perform the selling operation. Finally wait for the next cycle. It should be noted that there are certain risks in the strategy of grabbing new spot goods, so you need to operate with caution.
```

> Detail

https://www.fmz.com/strategy/410113

> Last Modified

2023-04-18 12:47:36
