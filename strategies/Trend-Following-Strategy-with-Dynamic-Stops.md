
> Name

Trend-Following-Strategy-with-Dynamic-Stops

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/8c4c6a5acbe70ebb18.png)


## Overview

This strategy generates trading signals when price crosses EMA and uses ATR as a dynamic stop loss to manage risks. 

## How It Works

The key logic is:

1. Calculate ATR as the stop loss line, ATR value determines stop distance nLoss

2. Price source is close price by default, use Heikin Ashi close if Heikin Ashi option h is enabled  

3. xATRTrailingStop tracks dynamic stop loss line based on price comparison with previous stop 

4. Position pos is 1 for long when price crosses above stop loss line, -1 for short when crosses below, else 0

5. EMA crossover signals, above EMA is buy signal, below is sell signal

6. Enter trades on buy/sell signals, exit on opposite signals

7. Color bars based on position, mark signals and stop loss lines

This strategy follows trends with dynamic stops based on ATR. It can identify trends and manage risks effectively.

## Advantages

The advantages are:

1. ATR-based dynamic stop adapts to market volatility  

2. EMA filter reduces false signals from noise  

3. Optional Heikin Ashi filters noise and identifies trend   

4. Clear long/short position avoids whipsaws from trailing stopOrder translation result:

5. Visual aids like lines, labels and coloring  

6. Simple and easy to understand logic for modifying

7. Customizable ATR period and multiplier for different markets

In summary, by combining trend following and dynamic stops, this strategy can catch trends and manage risks well for swing trading.

## Risks

There are some risks to consider:

1. EMA signals may lag missing short-term moves

2. Frequent stop loss triggers possible in choppy markets

3. No consideration of costs like commissions 

4. Lack of position sizing control 

5. Performance depends on parameter tuning

6. Risk of whipsaws in ranging markets

7. Requires monitoring and intervention

Risks can be reduced by optimizing parameters, adding filters, sizing positions properly, monitoring performance, and intervening when necessary.

## Optimization

Some ways to improve the strategy:

1. Adjust ATR parameters for different markets

2. Test other moving averages to filter signals

3. Add trend filter indicators for higher probability

4. Implement position sizing limits 

5. Add entry conditions like volume, distance from MA

6. Incorporate costs like commissions into stops

7. Optimize entry and exit timing with more signals

8. Introduce profit taking or trailing stops

9. Automated parameter optimization

By combining more techniques for entries, exits, filters, and parameter tuning, the strategy can be further robustified.

## Conclusion

This strategy combines dynamic stops and trend following nicely. With effective stops, smooth trend tracking, ease of use, and customizability, it is suitable for swing trading trends. But proper risk management, monitoring, and parameter tuning is required. When applied well on trending markets, good results can be achieved. Overall it provides a simple and practical approach to combining trend trading and risk management.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Key Vaule. 'This changes the sensitivity'|
|v_input_2|10|ATR Period|
|v_input_3|false|Signals from Heikin Ashi Candles|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-10-25 00:00:00
end: 2023-10-31 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy(title="UT Bot Strategy", overlay = true)
//CREDITS to HPotter for the orginal code. The guy trying to sell this as his own is a scammer lol. 

// Inputs
a = input(1,     title = "Key Vaule. 'This changes the sensitivity'")
c = input(10,    title = "ATR Period")
h = input(false, title = "Signals from Heikin Ashi Candles")

xATR  = atr(c)
nLoss = a * xATR

src = h ? security(heikinashi(syminfo.tickerid), timeframe.period, close, lookahead = false) : close

xATRTrailingStop = 0.0
xATRTrailingStop := iff(src > nz(xATRTrailingStop[1], 0) and src[1] > nz(xATRTrailingStop[1], 0), max(nz(xATRTrailingStop[1]), src - nLoss),
   iff(src < nz(xATRTrailingStop[1], 0) and src[1] < nz(xATRTrailingStop[1], 0), min(nz(xATRTrailingStop[1]), src + nLoss), 
   iff(src > nz(xATRTrailingStop[1], 0), src - nLoss, src + nLoss)))
 
pos = 0   
pos :=	iff(src[1] < nz(xATRTrailingStop[1], 0) and src > nz(xATRTrailingStop[1], 0), 1,
   iff(src[1] > nz(xATRTrailingStop[1], 0) and src < nz(xATRTrailingStop[1], 0), -1, nz(pos[1], 0))) 
   
xcolor = pos == -1 ? color.red: pos == 1 ? color.green : color.blue 

ema   = ema(src,1)
above = crossover(ema, xATRTrailingStop)
below = crossover(xATRTrailingStop, ema)

buy  = src > xATRTrailingStop and above 
sell = src < xATRTrailingStop and below

barbuy  = src > xATRTrailingStop 
barsell = src < xATRTrailingStop 

plotshape(buy,  title = "Buy",  text = 'Buy',  style = shape.labelup,   location = location.belowbar, color= color.green, textcolor = color.white, transp = 0, size = size.tiny)
plotshape(sell, title = "Sell", text = 'Sell', style = shape.labeldown, location = location.abovebar, color= color.red,   textcolor = color.white, transp = 0, size = size.tiny)

barcolor(barbuy  ? color.green : na)
barcolor(barsell ? color.red   : na)

strategy.entry("long",   true, when = buy)
strategy.entry("short", false, when = sell)
```

> Detail

https://www.fmz.com/strategy/430748

> Last Modified

2023-11-01 13:46:28
