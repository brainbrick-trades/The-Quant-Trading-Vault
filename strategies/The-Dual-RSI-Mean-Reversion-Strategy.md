
> Name

The-Dual-RSI-Mean-Reversion-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1c7f9b7ce76020d8ea6.png)

## Overview

The two-way RSI moving average recovery strategy is a trend following strategy that uses the RSI indicator in two different time periods to identify overbought and oversold conditions. This strategy aims to profit by going long after oversold and short after overbought. This strategy uses Moving Average Convergence and Divergence, RSI indicator, and position opening color filters to identify trading opportunities.

## Strategy Logic

This strategy uses two RSI indicators with different time periods - one on the 5-minute chart and one on the 1-hour chart. For the RSI indicator, oversold levels are considered below 30 and overbought levels are above 70.

It tracks the RSI value and looks for situations where the RSI remains in the oversold or overbought zone for a certain period, indicating an expanded oversold or overbought state. 

In addition, it uses the smoothed moving average of convergence and divergence to check the red or green candlestick of a certain period to confirm the trend direction before entering the transaction. Open position color filter helps avoid false signals.

When the conditions of RSI and smoothed moving average of convergence and divergence are met, this strategy will go long after oversold and short after overbought, betting that the price will return to the moving average.

Close positions at the end of each day to avoid overnight holding.

## Advantage Analysis

- Use multiple timeframes to identify overbought and oversold conditions
- Smoothed Moving Average Convergence and Divergence filters out noise and identifies trend direction 
- Open position color filter to avoid false signals
- Match clear opening and closing rules based on two indicators
- Close positions before each day to control risks

## Risk Analysis

- If the strong trend continues, the RSI may experience volatility after signaling overbought and oversold signals
- Market gaps may trigger stop loss
- The lagging of the smoothed moving average of convergence and divergence may delay the opening of positions and miss the market.
- Possible gains from closing positions before the end of each day and giving up overnight positions

## Optimization Direction

- Add additional filters like volume or volatility to confirm signals
- Optimize RSI period and overbought/oversold level parameters
- Consider dynamic position control based on volatility
- Test take-profit and stop-loss exit instead of closing the position before the end of each day
- Test effects and adjust parameters across different varieties

## Summary

The two-way RSI moving average reversal strategy uses a rule-based approach to trade momentum. By combining two time frames, overbought and oversold indicators, candlestick pattern analysis, and entry filters, it aims to identify high-probability moving average reversal opportunities. Strict risk management and prudent position control help manage drawdowns while making profits. Further optimization and robustness testing will assist in successfully deploying this strategy across various markets.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Long|
|v_input_2|true|Short|
|v_input_3|100|Lot, %|
|v_input_4|14|RSI period|
|v_input_5|30|RSI limit|
|v_input_6|3|RSI signals|
|v_input_7|true|Use Open Color Filter|
|v_input_8|2|Open Color, Bars|
|v_input_9|true|Show indicator RSI|
|v_input_10|2018|From Year|
|v_input_11|2100|To Year|
|v_input_12|true|From Month|
|v_input_13|12|To Month|
|v_input_14|true|From Day|
|v_input_15|31|To Day|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-09-01 00:00:00
end: 2023-09-30 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//Gidra
//2018

//@version=2
strategy(title = "Gidra's Vchain Strategy v0.1", shorttitle = "Gidra's Vchain Strategy v0.1", overlay = false, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, pyramiding = 100)

//Settings
needlong = input(true, defval = true, title = "Long")
needshort = input(true, defval = true, title = "Short")
capital = input(100, defval = 100, minval = 1, maxval = 10000, title = "Lot, %")
rsiperiod = input(14, defval = 14, minval = 2, maxval = 100, title = "RSI period")
rsilimit = input(30, defval = 30, minval = 1, maxval = 50, title = "RSI limit")
rsibars = input(3, defval = 3, minval = 1, maxval = 20, title = "RSI signals")
useocf = input(true, defval = true, title = "Use Open Color Filter")
openbars = input(2, defval = 2, minval = 1, maxval = 20, title = "Open Color, Bars")
showrsi = input(true, defval = true, title = "Show indicator RSI")
fromyear = input(2018, defval = 2018, minval = 1900, maxval = 2100, title = "From Year")
toyear = input(2100, defval = 2100, minval = 1900, maxval = 2100, title = "To Year")
frommonth = input(01, defval = 01, minval = 01, maxval = 12, title = "From Month")
tomonth = input(12, defval = 12, minval = 01, maxval = 12, title = "To Month")
fromday = input(01, defval = 01, minval = 01, maxval = 31, title = "From Day")
today = input(31, defval = 31, minval = 01, maxval = 31, title = "To Day")


//Heikin Ashi Open/Close Price
o=open
c=close
h=high
l=low
haclose = (o+h+l+c)/4
haopen = na(haopen[1]) ? (o + c)/2 : (haopen[1] + haclose[1]) / 2
hahigh = max (h, max(haopen,haclose))
halow = min (l, min(haopen,haclose))
col=haopen>haclose ? red : lime
plotcandle(haopen, hahigh, halow, haclose, title="heikin", color=col)

//RSI
uprsi = rma(max(change(close), 0), rsiperiod)
dnrsi = rma(-min(change(close), 0), rsiperiod)
rsi = dnrsi == 0 ? 100 : uprsi == 0 ? 0 : 100 - (100 / (1 + uprsi / dnrsi))
uplimit = 100 - rsilimit
dnlimit = rsilimit
rsidn = rsi < dnlimit ? 1 : 0
rsiup = rsi > uplimit ? 1 : 0

//RSI condition
rsidnok = highest(rsidn, rsibars) == 1? 1 : 0
rsiupok = highest(rsiup, rsibars) == 1? 1 : 0

//Color Filter
bar = haclose > haopen ? 1 : haclose < haopen ? -1 : 0
gbar = bar == 1 ? 1 : 0
rbar = bar == -1 ? 1 : 0
openrbarok = sma(gbar, openbars) == 1 or useocf == false
opengbarok = sma(rbar, openbars) == 1 or useocf == false

//Signals
up = openrbarok and rsidnok
dn = opengbarok and rsiupok

lot = strategy.position_size == 0 ? strategy.equity / close * capital / 100 : lot[1]

//Indicator RSI
colbg = showrsi == false ? na : rsi > uplimit ? red : rsi < dnlimit ? lime : na
bgcolor(colbg, transp = 20)

//Trading
if up
    strategy.entry("Long", strategy.long, needlong == false ? 0 : lot, when=(time > timestamp(fromyear, frommonth, fromday, 00, 00) and time < timestamp(toyear, tomonth, today, 23, 59)))

if dn
    strategy.entry("Short", strategy.short, needshort == false ? 0 : lot, when=(time > timestamp(fromyear, frommonth, fromday, 00, 00) and time < timestamp(toyear, tomonth, today, 23, 59)))
    
if time > timestamp(toyear, tomonth, today, 23, 59)// or exit
    strategy.close_all()
```

> Detail

https://www.fmz.com/strategy/429958

> Last Modified

2023-10-23 15:46:33
