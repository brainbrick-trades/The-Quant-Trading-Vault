
> Name

Bollinger-Bands-and-RSI-Combined-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/9902c112406b3a786f.png)






> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-27 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Bollinger Bands + RSI Strategy", shorttitle="BB_RSI", overlay=true)

// Define the Bollinger Bands parameters
length = input(20, title="Length")
mult = input(2.5, title="Multiplier")
basis = ta.sma(close, length)
dev = mult * ta.stdev(close, length)
upper = basis + dev
lower = basis - dev

// Define the RSI parameters
rsiLength = input(14, title="RSI Length")
rsiOverbought = input(70, title="RSI Overbought Level")
rsiOversold = input(30, title="RSI Oversold Level")
rsi = ta.rsi(close, rsiLength)

// Plot the Bollinger Bands and RSI
plot(basis, "Basis", color=color.yellow)
p1 = plot(upper, "Upper", color=color.red)
p2 = plot(lower, "Lower", color=color.green)
fill(p1, p2, color=color.rgb(255, 255, 255, 90))
hline(rsiOverbought, "Overbought", color=color.red)
hline(rsiOversold, "Oversold", color=color.green)

// Generate Buy and Sell signals
buyCondition = close < lower and rsi < rsiOversold
sellCondition = close > upper and rsi > rsiOverbought

if (buyCondition)
    strategy.entry("Buy", strategy.long)

if (sellCondition)
    strategy.close("Buy")

// Optional: Add exit strategy for buys
exitCondition = rsi > 50
if (exitCondition)
    strategy.close("Buy")

// Plot RSI on a separate panel
plot(rsi, "RSI", color=color.purple)

```

> Detail

https://www.fmz.com/strategy/473266

> Last Modified

2024-11-28 17:13:43
