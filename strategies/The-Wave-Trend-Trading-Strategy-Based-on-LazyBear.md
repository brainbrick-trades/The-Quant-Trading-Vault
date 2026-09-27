
> Name

The-Wave-Trend-Trading-Strategy-Based-on-LazyBear

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/b00fb69eb9c85ed879.png)
 
## Overview

This is a trading strategy based on LazyBear's Wave Trend indicator. The strategy identifies market sentiment through computing the wave trend of price fluctuations, and makes long and short decisions accordingly.  

## Strategy Logic

The core of this strategy is LazyBear's Wave Trend indicator. It first calculates the average price (AP), then the exponential moving average of AP (ESA) and the absolute price movement (D). Based on ESA and D the strategy calculates the Volatility Index (CI), which then feeds into an exponential moving average to generate the Wave Trend line (WT). WT is further processed into WT1 and WT2 using simple moving averages. When WT1 crosses over WT2, it triggers the golden cross and goes long. When WT1 crosses below WT2, it triggers the death cross and goes short.

## Advantage Analysis  

This is a very simple but practical trend following strategy. The main advantages are:

1. It identifies price trend and market sentiment clearly based on the Wave Trend indicator  
2. Simple trading logic of going long/short based on golden/death crosses of WT lines
3. Customizable parameters to adjust sensitivity of WT for different cycles  
4. Flexibility to add further filters such as trading time window

## Risk Analysis   

There are some risks to this strategy:

1. As a trend following strategy, it can generate many false signals during range-bound markets
2. The lagging nature of WT may cause missed turns   
3. Default parameters may not suit all products and cycles
4. No stop loss mechanism, holding period can be very long

The main solutions are:

1. Optimize parameters to tune sensitivity of WT
2. Add other indicators for confirmation to avoid false signals
3. Employ stop loss and take profit  
4. Limit daily trades or positions 

## Optimization Directions

There is room for further optimization:

1. Optimize WT parameters for better sensitivity or stability
2. Use different parameter sets based on cycles
3. Add indicators like volume, volatility for confirmation   
4. Add stop loss and take profit
5. Enrich trading logic like pyramiding, grid trading
6. Explore better features and rules using machine learning

## Summary

In summary, this is a very simple and practical wave trend following strategy. By modeling the wave trend of price fluctuations, it identifies overbought and oversold market conditions to generate trade signals using WT's golden crosses and death crosses. The strategy is easy to implement but may require further optimization for sensitivity and stability. As a trend following strategy, it also needs additional filters and logic to avoid false signals. Overall this serves as a useful strategy template with lots of room for improvements.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|From Month|
|v_input_2|true|From Day|
|v_input_3|2021|From Year|
|v_input_4|true|Thru Month|
|v_input_5|true|Thru Day|
|v_input_6|2112|Thru Year|
|v_input_7|true|Show Date Range|
|v_input_8|10|Channel Length|
|v_input_9|21|Average Length|
|v_input_10|60|Over Bought Level 1|
|v_input_11|53|Over Bought Level 2|
|v_input_12|-60|Over Sold Level 1|
|v_input_13|-53|Over Sold Level 2|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-18 00:00:00
end: 2023-12-18 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//
// @author LazyBear
//
// If you use this code in its original/modified form, do drop me a note. 
//
//@version=4
     
// === INPUT BACKTEST RANGE ===
fromMonth = input(defval = 1,    title = "From Month",      type = input.integer, minval = 1, maxval = 12)
fromDay   = input(defval = 1,    title = "From Day",        type = input.integer, minval = 1, maxval = 31)
fromYear  = input(defval = 2021, title = "From Year",       type = input.integer, minval = 1970)
thruMonth = input(defval = 1,    title = "Thru Month",      type = input.integer, minval = 1, maxval = 12)
thruDay   = input(defval = 1,    title = "Thru Day",        type = input.integer, minval = 1, maxval = 31)
thruYear  = input(defval = 2112, title = "Thru Year",       type = input.integer, minval = 1970)

// === INPUT SHOW PLOT ===
showDate  = input(defval = true, title = "Show Date Range", type = input.bool)

// === FUNCTION EXAMPLE ===
start     = timestamp(fromYear, fromMonth, fromDay, 00, 00)        // backtest start window
finish    = timestamp(thruYear, thruMonth, thruDay, 23, 59)        // backtest finish window
window()  => true       // create function "within window of time"

n1 = input(10, "Channel Length")
n2 = input(21, "Average Length")
obLevel1 = input(60, "Over Bought Level 1")
obLevel2 = input(53, "Over Bought Level 2")
osLevel1 = input(-60, "Over Sold Level 1")
osLevel2 = input(-53, "Over Sold Level 2")
 
ap = hlc3 
esa = ema(ap, n1)
d = ema(abs(ap - esa), n1)
ci = (ap - esa) / (0.015 * d)
tci = ema(ci, n2)
 
wt1 = tci
wt2 = sma(wt1,4)

plot(0, color=color.gray)
plot(obLevel1, color=color.red)
plot(osLevel1, color=color.green)
plot(obLevel2, color=color.red, style=3)
plot(osLevel2, color=color.green, style=3)

plot(wt1, color=color.white)
plot(wt2, color=color.fuchsia)
plot(wt1-wt2, color=color.new(color.blue, 80), style=plot.style_area)

//Strategy
strategy(title="T!M - Wave Trend Strategy", overlay = false, precision = 8, max_bars_back = 200, pyramiding = 0, initial_capital = 1000, currency = currency.NONE, default_qty_type = strategy.cash, default_qty_value = 1000, commission_type = "percent", commission_value = 0.1, calc_on_every_tick=false, process_orders_on_close=true)
    
longCondition  = crossover(wt1, wt2)
shortCondition = crossunder(wt1, wt2)

strategy.entry(id="Long Entry", comment="buy", long=true, when=longCondition and window())
strategy.close("Long Entry", comment="sell", when=shortCondition and window())      

//strategy.entry(id="Short Entry", long=false, when=shortCondition)
```

> Detail

https://www.fmz.com/strategy/435853

> Last Modified

2023-12-19 12:07:14
