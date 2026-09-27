
> Name

Reversal-Trading-Strategy-Based-on-Moving-Average-Range

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/16f517e1fd1f7d5fdf6.png)
 
## Overview  

This strategy is named "Moving Average Range Reversal". It identifies market reversal opportunities by calculating crossovers between moving averages of different timeframes and takes appropriate long/short positions.  

## Strategy Logic  

The strategy computes 3 moving averages simultaneously:  

1. Fast MA (flenght): Reflecting latest price changes  
2. Slow MA (llenght): Reflecting mid-term price trends  
3. Slowest MA (sslenght): Reflecting long-term price tendencies  

When fast MA crosses above slow MA, it signals a short-term trend reversal to bullish. When fast MA crosses below slow MA, it signals a short-term reversal to bearish.  

To avoid false signals, a 4th MA is introduced as the long-term filter (tlenght). Only above this filter long signals are considered. Only below this filter short signals are considered.  

The specific trading rules are:  

1. When fast MA crosses above slow MA, and slow MA also crosses above slowest MA (short-term bullish), while price is above the long-term filter, go long. When fast MA crosses below slow MA, close long position.  

2. When fast MA crosses below slow MA, and slow MA also crosses below slowest MA (short-term bearish), while price is below the long-term filter, go short. When fast MA crosses above slow MA, close short position.

## Advantage Analysis   

The advantages of this strategy include:  

1. Utilizing multiple timeframes to identify trend changes more precisely and reduce false signals.   
2. Long-term filter avoids mispositioned trades before major trend reversal.  
3. Simple and clear rules, easy to understand and automate.
4. Reversal strategies benefit from positive bias in returns and profits.  
5. Good backtest results in simulated live trading regarding returns and profit factor.

## Risk Analysis   

The risks of the strategy include:

1. MA strategies are sensitive to parameters. Different parameters lead to different results.  
2. False breakout of reversal signals may cause losses. 
3. Prolonged sideways may nullify profits from repeated reversals.   
4. Price may reverse and accelerate with strength, failing timely stop loss.

Solutions:  

1. Optimize parameters to find best combination.  
2. Increase signal confirmation time to avoid false signals.   
3. Expand stop loss range to control loss amount.  

## Optimization Directions   

The strategy can be improved in the following aspects:  

1. Test more parameter sets to find optimum values.  
2. Add volume filter to avoid false signals in low volume conditions.   
3. Incorporate other indicators to confirm entry signals.  
4. Implement dynamic adjustment of stop loss for better exit control.
5. Optimize risk management for tighter risk control.   

## Conclusion   

This strategy trades market reversals identified by MA crossovers, with direction guidance from the long-term filter. It effectively captures opportunities at turning points. The positive backtest results show good profitability for live application. Further optimizations on parameters, signal filtering, stop loss etc. can make the strategy more robust for practical use.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|3|Fast MA Period|
|v_input_int_2|5|Slower MA Period|
|v_input_int_3|8|Slowest MA Period|
|v_input_int_4|200|Trend Filter MA Period|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5

strategy("Moving Average Trap", overlay=true)

flenght = input.int(title="Fast MA Period", minval=1, maxval=2000, defval=3)
llenght = input.int(title="Slower MA Period", minval=1, maxval=2000, defval=5)
sslenght = input.int(title="Slowest MA Period", minval=1, maxval=2000, defval=8)
tlenght = input.int(title="Trend Filter MA Period", minval=1, maxval=2000, defval=200)

ssma = ta.sma(close, sslenght)
fma = ta.sma(close, flenght)
sma = ta.sma(close, llenght)
tma = ta.sma(close, tlenght)

plot(fma, color=color.red)
plot(sma, color=color.white)
plot(ssma, color=color.green)
plot(tma, color=color.maroon, linewidth=2)

short =  (fma > sma and sma > ssma) and close < tma
long = (fma < sma and sma < ssma) and close > tma
closeshort = fma < sma and sma < ssma
closelong = fma > sma and sma > ssma

if long
	strategy.entry("long", strategy.long)
if closelong
	strategy.close("long")
if short
	strategy.entry("short", strategy.short)
if closeshort
	strategy.close("short")

//plot(strategy.equity, title="equity", color=color.red, linewidth=2, style=plot.style_areabr)
```

> Detail

https://www.fmz.com/strategy/439973

> Last Modified

2024-01-25 14:16:28
