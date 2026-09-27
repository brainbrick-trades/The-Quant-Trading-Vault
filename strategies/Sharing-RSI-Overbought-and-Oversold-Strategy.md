
> Name

Sharing-RSI-Overbought-and-Oversold-Strategy

> Author

盯盘狗 - 策略出租





> Source (python)

``` python
import talib
import numpy as np
import time

# Initialize strategy parameters
symbol = 'huobip/btc_usdt'
period = '1m'
rsi_period = 14
rsi_buy = 30
rsi_sell = 70
amount = 0.01
last_buy_price = 0

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

    # Calculate RSI indicator
    close_prices = np.array([float(k['Close']) for k in klines])
    rsi = talib.RSI(close_prices, rsi_period)

    # Get current price
    current_price = float(klines[-1]['Close'])

    # Determine whether it is overbought or oversold
    if rsi[-1] < rsi_buy and last_buy_price == 0:
        # Oversold, buy
        buy_price = current_price
        buy_amount = amount / buy_price
        exchange.Buy(buy_price, buy_amount)
        last_buy_price = buy_price
        print('Buy', buy_amount, 'BTC, at price', buy_price)
    elif rsi[-1] > rsi_sell and last_buy_price != 0:
        # Overbought, sell
        sell_price = current_price
        sell_amount = amount / sell_price
        exchange.Sell(sell_price, sell_amount)
        last_buy_price = 0
        print('Sell ', sell_amount, ' BTC, price', sell_price)

    # Wait for next loop
    time.sleep(60)

```

> Detail

https://www.fmz.com/strategy/410112

> Last Modified

2023-04-18 12:46:08
