
> Name

Bollinger-Bands-Channel-Breakout-Mean-Reversion-Strategy

> Author

ChaoZhang

> Strategy Description


![IMG](https://www.fmz.com/upload/asset/894c61b24fe988aa15.png)
 
## Overview

This is a mean reversion breakout strategy based on the Bollinger Bands channel. It goes long when the price breaks below the lower band of the Bollinger Bands. The stop loss is set at the low of the breakout bar. The profit target is the upper band of the Bollinger Bands.

## Strategy Logic  

The strategy uses a 20-period Bollinger Bands channel, which consists of a middle band, an upper band and a lower band. The middle band is a 20-period simple moving average. The upper band is the middle band plus 2 standard deviations. The lower band is the middle band minus 2 standard deviations.  

When the price breaks below the lower band, it indicates the price has entered an oversold status. The strategy will go long at this point. After entering the position, the stop loss is set at the low of the entry bar, and the profit target is the upper band. Thus the strategy aims to capture the reversion process from oversold to the mean, in order to make profits.

## Advantage Analysis   

The advantages of this strategy are:

1. Use Bollinger Bands to judge overbought/oversold status, which has some timeliness
2. Reversion trading strategy, avoiding chasing highs and killing lows
3. Reasonable stop loss and take profit setting for better risk control

## Risk Analysis

The risks of this strategy include:
 
1. Bollinger Bands cannot perfectly determine price trends, breakouts may fail
2. Continous market crash may hit stop loss
3. Take profit near upper band has the risk of high cost

## Optimization Directions   

The strategy can be improved from the following aspects:

1. Optimize parameters of Bollinger Bands to find the best combination
2. Add filter indicators to improve entry accuracy 
3. Optimize stop loss and take profit for higher profitability

## Conclusion  

The strategy has clear logic and is tradable to some extent. However, its effectiveness in judging overbought/oversold with Bollinger Bands is limited, and it cannot perfectly determine the trend. Also, the stop loss and take profit mechanism needs improvement. Going forwards, it can be optimized by choosing more accurate indicators, tuning parameters, and enhancing the exit logic to improve profitability.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|20|Bollinger Bands Length|
|v_input_float_1|2|Multiplier|
|v_input_3_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_bool_1|true|(?Backtest Time Period)Filter Date Range of Backtest|
|v_input_1|timestamp(1 Jan 1997)|Start Date|
|v_input_2|timestamp(1 Sept 2023)|End Date|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-01-15 00:00:00
end: 2024-01-21 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Ronsword
//@version=5

strategy("bb 2ND target", overlay=true)
 
// STEP 1. Create inputs that configure the backtest's date range
useDateFilter = input.bool(true, title="Filter Date Range of Backtest",
     group="Backtest Time Period")
backtestStartDate = input(timestamp("1 Jan 1997"), 
     title="Start Date", group="Backtest Time Period",
     tooltip="This start date is in the time zone of the exchange " + 
     "where the chart's instrument trades. It doesn't use the time " + 
     "zone of the chart or of your computer.")
backtestEndDate = input(timestamp("1 Sept 2023"),
     title="End Date", group="Backtest Time Period",
     tooltip="This end date is in the time zone of the exchange " + 
     "where the chart's instrument trades. It doesn't use the time " + 
     "zone of the chart or of your computer.")

// STEP 2. See if the current bar falls inside the date range
inTradeWindow = true

// Bollinger Bands inputs
length = input.int(20, title="Bollinger Bands Length")
mult = input.float(2.0, title="Multiplier")
src = input(close, title="Source")
basis = ta.sma(src, length)
dev = mult * ta.stdev(src, length)
upper = basis + dev
lower = basis - dev

// EMA Settings
ema20 = ta.ema(close, 20)
plot(ema20, color=color.blue, title="20 EMA")

// Entry condition
longEntryCondition = ta.crossover(close, lower)

// Define stop loss level as the low of the entry bar
var float stopLossPrice = na
if longEntryCondition
    stopLossPrice := low

// Top Bollinger Band itself is set as the target
topBandTarget = upper

// Enter long position when conditions are met
if inTradeWindow and longEntryCondition
    strategy.entry("Long", strategy.long, qty=1)

// Set profit targets
strategy.exit("ProfitTarget2", from_entry="Long", limit=topBandTarget)

// Set stop loss
strategy.exit("StopLoss", stop=stopLossPrice)

// Plot Bollinger Bands with the same gray color
plot(upper, color=color.gray, title="Upper Bollinger Band")
plot(lower, color=color.gray, title="Lower Bollinger Band")


```

> Detail

https://www.fmz.com/strategy/439608

> Last Modified

2024-01-22 10:47:45
