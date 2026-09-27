
> Name

Momentum-Breakout-Trading-Strategy-440531

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1a0b254642e7fa1ecc6.png)
 
### Overview

This is a momentum-based trend following breakout trading strategy. It calculates the highest and lowest prices over a certain period to determine the trend direction, and enters long or short trades when prices break key levels.  

### Strategy Logic

The core logic of this strategy is:

1. Use the highest() and lowest() functions to calculate the highest and lowest prices of the recent 20 candlesticks, as momentum indicators to judge the trend.

2. When the latest close price breaks above the highest price of the previous period, go long. This is an upward breakout signal.

3. When the latest close price breaks below the lowest price of the previous period, go short. This is a downward breakout signal.

4. To control risks, set a 1% stop loss distance and 2% take profit distance, giving a risk-reward ratio of 2:1.

5. Plot the highest and lowest prices within the 20 candlesticks to visually determine the trend direction and breakout levels.

The above is the core trading logic of this strategy. It uses momentum indicators to judge the trend, and trades breakouts of key levels, making it a trend following breakout strategy.

### Advantages

The advantages of this strategy include:

1. Catching the direction and strength of trends with high precision. Calculating highest and lowest prices helps filter out false signals from range-bound markets. 

2. Simple and clear logic. Just long above previous highest, and short below previous lowest. Easy to understand and implement.

3. Controllable risks. The max loss is 1% and max profit is 2% with stop loss and take profit set, giving a reasonable risk-reward ratio.

4. Easy to optimize. The calculation period can be adjusted for better entry timing. Stop loss and take profit levels can also be tuned for more profits or lower risks.

### Risks

There are also some risks:

1. Stop loss being hit is still possible with fast, huge price swings.

2. Missing reversal signals if the calculation period is too long. Trend judgment then lags behind.

3. Improper parameter settings may lead to unprofitability. The calculation period and stop loss/take profit levels need careful testing and optimization.

### Optimization

This strategy can be improved in aspects like:

1. Adding filters to ensure sufficient trend strength before entering trades. Trend metrics can be used.

2. Adjusting the period parameter to balance timeliness and stability of trend judgment. Too short leads to false signals, too long leads to lag.

3. Incorporating trailing stop loss to lock in profits and avoid stop loss being hit. 

4. Parameter optimization through historical backtesting to find the optimal combinations of settings.

### Conclusion  
This is a typical trend following breakout trading strategy. It uses momentum indicators to determine the trend, and trades breakouts of key levels. The pros are simplicity, controllable risks, and ease of understanding/optimization. But it may underperform in certain market environments. Further optimizations can improve its robustness and efficiency.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|20|Length|
|v_input_2|true|Stop Loss %|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-31 00:00:00
end: 2024-01-30 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Trend Following Breakout Strategy with 2:1 RRR", overlay=true)

// Define calculation of previous high and low
length = input(20, minval=1, title="Length")
highestHigh = highest(high, length)
lowestLow = lowest(low, length)

// Define conditions for buying and selling
longCondition = close > highestHigh[1] // The current closing price is higher than the previous period's high
shortCondition = close < lowestLow[1] // The current closing price is lower than the previous period's low

// To ensure a profit-loss ratio of2:1,We need to define stop-loss and target price
stopLoss = input(1, title="Stop Loss %") / 100
takeProfit = stopLoss * 2

// If buy conditions are met, enter long
if (longCondition)
    strategy.entry("Long", strategy.long)
    strategy.exit("Long TP", "Long", profit=takeProfit * close, loss=stopLoss * close)

// If sell conditions are met, enter short
if (shortCondition)
    strategy.entry("Short", strategy.short)
    strategy.exit("Short TP", "Short", profit=takeProfit * close, loss=stopLoss * close)

// Drawing shows previous high and previous low
plot(highestHigh, color=color.green, title="Previous High")
plot(lowestLow, color=color.red, title="Previous Low")

```

> Detail

https://www.fmz.com/strategy/440531

> Last Modified

2024-01-31 14:14:56
