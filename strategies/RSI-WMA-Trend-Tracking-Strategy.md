
> Name

RSI-WMA-Trend-Tracking-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1334ca2ef7f1a4f65bf.png)
 
## Overview

The strategy is named "RSI/WMA Trend Tracking Strategy". It utilizes the advantages of both Relative Strength Index (RSI) and Weighted Moving Average (WMA) to determine overbought and oversold areas and price trend direction, thus effectively tracking price trends.

## Strategy Principle

The core idea is using RSI indicator to identify overbought/oversold situations. When RSI goes below the oversold line, it indicates oversold status and long positions can be opened. When RSI goes above the overbought line while long positions are opened, it presents good opportunities to close longs. In addition, WMA is used to measure price trend. Upward crossover of price and WMA shows uptrend while downward crossover shows downtrend. By combining judgment on overbought/oversold and price trend, price trends can be effectively tracked - go long at relative lows and close longs at relative highs.

Specifically, the trading logic is:

1. Enter long when RSI goes below the oversold line and set take profit. 

2. Close long when RSI goes above the overbought line while holding open long positions.

3. Cancel the take profit when price crosses above WMA.  

4. Close long when price crosses below WMA while holding open long positions.

This logic allows to track uptrend at relative lows and downtrend at relative highs, capturing part of the price move.

## Advantages

The main advantages are:

1. Utilize both RSI and WMA for better trend and overbought/oversold analysis.

2. Enter at relatively high/low levels by tracking overbought/oversold areas.  

3. Take profits quickly by setting exit orders, capturing parts of the price move.

4. Simple and easy-to-understand logic, easy to adjust parameters.

5. Allow both long and short, adaptable to all market conditions.

## Risks

There are some risks to note:

1. Lagging issues of RSI and WMA may lead to delayed signal.

2. Take profit orders may get stopped out prematurely. 

3. Parameters require constant optimization and tuning e.g. overbought/oversold levels.

4. Significant whipsaw may cause large losses.

The risks can be improved by incorporating stop loss, parameter tuning through optimization etc.

## Improvement Areas

The strategy can be further improved in the following areas:

1. Incorporate stop loss alongside take profits.

2. Optimize parameters like RSI/WMA periods through backtesting and paper trading.

3. Introduce position sizing for better risk management. 

4. Combine more indicators like MACD, KD to form indicator combos.

5. Utilize machine learning to auto-tune parameters for better performance.

## Conclusion

This strategy combines RSI and WMA to identify overbought/oversold levels and spot trend reversal, automatically tracking price trends and capturing part of the profits. There is good room for improvement by introducing more features, position sizing, machine learning etc. Overall a simple trend tracking strategy worth exploring.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|2|length|
|v_input_2|10|overSold|
|v_input_3|90|overBought|
|v_input_4|50|WMA Length|
|v_input_5|true|Enable Long Trades|
|v_input_6|true|Enable Long Exit|
|v_input_7|false|Enable Short Trades|
|v_input_8|false|Enable Short TradExites|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-10 00:00:00
end: 2024-01-11 06:00:00
period: 5m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
//Lets connect on LinkedIn (https://www.linkedin.com/in/lets-grow-with-quality/)
//
//I use my indicator it in real life with a zero commision broker ob S&P500 Daily.
//Best performace when used with S&, lomg only and pyramiding on daily timeframe.
//
//Please.. still use your brain for entries and exits: higher timeframes, market structure, trend ... 
//If you obviously can see, like when corona started, that cubic tons of selling volume is going to punsh the markets, wait until selling climax is over and so on..

strategy("RSI/WMA Strategy", overlay=true)

length = input(2)
overSold = input(10)
overBought = input(90)
wmaLength = input(50, title="WMA Length")

enableLongTrades = input(true, title="Enable Long Trades")
longExit = input(true, title="Enable Long Exit")
enableShortTrades = input(false, title="Enable Short Trades")
shortExit = input(false, title="Enable Short TradExites")

price = close
vrsi = ta.wma(ta.rsi(price, length), 2)
wma = ta.wma(price, wmaLength)


co = ta.crossunder(vrsi, overSold)
cu = ta.crossunder(vrsi, overBought)

if (not na(vrsi))
    if (enableLongTrades and co) 
        strategy.entry("RsiLE", strategy.long, comment="RsiLE")
    if (enableShortTrades and cu) 
        strategy.entry("RsiSE", strategy.short, comment="RsiSE")

// Close long position if price crosses above SMA
if (longExit and ta.crossover(price, wma))
    strategy.close("RsiLE", comment="Close Long")

// Close short position if price crosses below SMA
if (shortExit and ta.crossunder(price, wma))
    strategy.close("RsiSE", comment="Close Short")

// Plot für visuelle Überprüfung
plot(wma, title="wmi", color=color.blue)
```

> Detail

https://www.fmz.com/strategy/439237

> Last Modified

2024-01-18 15:35:37
