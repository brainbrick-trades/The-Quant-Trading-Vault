
> Name

Share-Gambler-Strategy-Martin-Strategy

> Author

盯盘狗 - 策略出租

> Strategy Description

This strategy uses the Exchange API provided by the FMZ platform for trading. In the main loop, first get the candlestick data, and then get the current price. If the current price is lower than a certain percentage of the last purchase price, a stop loss operation will be performed; if the current price is higher than a certain percentage of the last purchase price, a take profit operation will be performed; if there is no current position, an initial position purchase operation will be performed; if the current position quantity is less than the set maximum number of positions, an additional position operation will be performed. Finally wait for the next cycle. It should be noted that the Martin strategy has certain risks and needs to be operated with caution.



> Source (python)

``` python
import time

# Initialize strategy parameters
symbol = 'huobip/btc_usdt'
period = '1m'
amount = 0.01
martingale_factor = 2
max_martingale_times = 5
stop_loss = 0.05
stop_profit = 0.1
last_buy_price = 0
martingale_times = 0

# ConnectAPI
exchange = Exchange()
exchange.SetContractType(symbol)
exchange.SetPeriod(period)

# Main loop
while True:
    # Get candlestick data
    klines = exchange.GetRecords()
    if not klines:
        continue

    # Get current price
    current_price = float(klines[-1]['Close'])

    # Determine whether to add position
    if last_buy_price != 0 and current_price < last_buy_price * (1 - stop_loss):
        # Stop loss, sell all positions
        sell_price = current_price
        sell_amount = exchange.GetPosition()['Amount']
        exchange.Sell(sell_price, sell_amount)
        last_buy_price = 0
        martingale_times = 0
        print('Stop loss, sell all positions, price', sell_price)
    elif last_buy_price != 0 and current_price > last_buy_price * (1 + stop_profit):
        # Take profit, sell all positions
        sell_price = current_price
        sell_amount = exchange.GetPosition()['Amount']
        exchange.Sell(sell_price, sell_amount)
        last_buy_price = 0
        martingale_times = 0
        print('Take profit, sell all positions, price', sell_price)
    elif last_buy_price == 0:
        # Buy an initial position
        buy_price = current_price
        buy_amount = amount / buy_price
        exchange.Buy(buy_price, buy_amount)
        last_buy_price = buy_price
        martingale_times = 0
        print('Buy initial position, price', buy_price)
    elif martingale_times < max_martingale_times:
        # add to position
        buy_price = current_price * martingale_factor
        buy_amount = amount / buy_price
        exchange.Buy(buy_price, buy_amount)
        last_buy_price = (last_buy_price * martingale_times + buy_price) / (martingale_times + 1)
        martingale_times += 1
        print('Add position, price', buy_price)

    # Wait for next loop
    time.sleep(60)

```

> Detail

https://www.fmz.com/strategy/410114

> Last Modified

2023-04-18 12:51:35
