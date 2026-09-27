
> Name

Moving-Average-and-Super-Trend-Tracking-Stop-Loss-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/682d04e278352ca713.png)
 
## Overview

This strategy uses moving averages and the supertrend indicator to determine market trends, combined with a tracking stop loss mechanism, to design a tracking stop loss trading strategy. When the supertrend indicator judges an uptrend, if the closing price breaks through the 14-period moving average, go long; when the supertrend indicator judges a downtrend, if the closing price breaks through the 14-period moving average, go short. After going long or short, stop loss will be triggered based on the position of the stop loss point.

## Strategy Principle  

This strategy uses three technical indicators: moving average, supertrend and tracking stop loss.

First, calculate the 14-period and 44-period exponential moving averages. The 14-period moving average is used to determine short-term trends, while the 44-period moving average is used to determine long-term trends. When the short-term moving average crosses above the long-term moving average, it is a bullish signal, and vice versa.

Secondly, calculate the supertrend indicator to judge the current market trend. The supertrend indicator consists of the positive indicator DI+ and the negative indicator DI-. When DI+ is higher than DI-, it is a bullish trend; when DI- is higher than DI+, it is a bearish trend.

Finally, combine the moving average signal and the trend judgment of the supertrend indicator to generate trading signals. When the supertrend indicator shows bullish and the price breaks through the 14-period moving average, go long; when the supertrend indicator shows bearish and the price breaks through the 14-period moving average, go short. After entering the market, set the stop loss point near the 44-period moving average to realize tracking stop loss.

## Advantage Analysis   

This strategy combines the advantages of three technical indicators to make accurate judgments and timely stop losses, and has the following advantages:

1. Moving averages determine short-term and long-term trends, accurately identifying signals.
2. The supertrend indicator determines the main trend direction and reduces false signals.
3. The tracking stop loss mechanism reduces single stop loss and has an overall good stop loss effect.

## Risk Analysis

This strategy also has some risks:

1. Failed breakout risk. Prices may pull back again after breaking through moving averages, missing the best entry point.
2. Stop loss triggered risk. Tracking stop loss cannot completely avoid losses, and can only control single losses within a certain range. 
3. Parameter optimization risk. Improper settings of moving average periods, supertrend parameters, etc. will affect signal quality.

The corresponding solutions are:

1. Use other indicators to filter signals and improve breakout success rate.
2. Optimize tracking stop loss parameters to set stop loss point to reasonable position.
3. Test and optimize parameters to select the best parameter combination.  

## Optimization Directions

This strategy can also be optimized in the following directions:

1. Increase other indicators to filter out wrong signals and improve strategy win rate. For example, combine trading volume indicators to strengthen trends.

2. Optimize tracking stop loss methods to make stop loss more intelligent and flexible. For example, ATR stop loss, Chandelier Exit, etc.

3. Use machine learning methods to find more optimal parameters. For example, genetic algorithms, deep learning and other methods to find the optimal parameter combination.  

4. Run strategies over higher time frames to avoid high frequency noise interference.   

## Conclusion  

This strategy combines moving averages, supertrend indicators and tracking stop loss techniques to make accurate judgments and timely stop losses. It is a pragmatic and reliable tracking stop loss trading strategy. The effect of the strategy can be further enhanced by improving signal quality, optimizing stop loss methods, etc.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|3|ATR Length|
|v_input_float_1|true|Factor|
|v_input_int_1|14|Length|
|v_input_2_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_int_2|false|Offset|
|v_input_int_3|44|Length|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-09 00:00:00
end: 2024-01-16 00:00:00
period: 10m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Santanu Strategy", overlay=true)

atrPeriod = input(3, "ATR Length")
factor = input.float(1, "Factor", step = 0.01)

[supertrend, direction] = ta.supertrend(factor, atrPeriod)

bodyMiddle = plot((open + close) / 2, display=display.none)
upTrend = plot(direction < 0 ? supertrend : na, "Up Trend", color = color.green, style=plot.style_linebr)
downTrend = plot(direction < 0? na : supertrend, "Down Trend", color = color.red, style=plot.style_linebr)

fill(bodyMiddle, upTrend, color.new(color.green, 90), fillgaps=false)
fill(bodyMiddle, downTrend, color.new(color.red, 90), fillgaps=false)

len = input.int(14, minval=1, title="Length")
src = input(close, title="Source")
offset = input.int(title="Offset", defval=0, minval=-500, maxval=500)
out = ta.ema(src, len)

len44 = input.int(44, minval=1, title="Length")
out44 = ta.ema(src, len44)

isRising = ta.rising(out, 1)
isFalling = ta.falling(out, 1)

plotColor = color.black
if isRising
    plotColor := color.green
else if isFalling
    plotColor := color.red
    

plot(out, color=plotColor, title="MA", offset=offset)
plot(out44, color=color.blue, title="MA", offset=offset)

if direction < 0
    if close >= out
        //if low >= out44
        if isRising
            strategy.entry("Buy Now", strategy.long)

if direction > 0
    if close <= out
        //if high <= out44
        if isFalling
            strategy.entry("Sell Now", strategy.short)


//plot(strategy.equity, title="equity", color=color.red, linewidth=2, style=plot.style_areabr)
```

> Detail

https://www.fmz.com/strategy/439048

> Last Modified

2024-01-17 11:46:01
