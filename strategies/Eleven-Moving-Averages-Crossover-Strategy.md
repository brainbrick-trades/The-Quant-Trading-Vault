
> Name

Eleven-Moving-Averages-Crossover-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1f7f2cebbb13c6663dd.png)


## Overview

This strategy uses a combination of 11 different types of moving average crossovers for long and short positions. The 11 moving averages used include: Simple Moving Average (SMA), Exponential Moving Average (EMA), Weighted Moving Average (WMA), Volume Weighted Moving Average (VWMA), Smoothed Moving Average (SMMA), Dual Exponential Moving Average (DEMA), Triple Exponential Moving Average (TEMA), Hull Moving Average (HMA), Zero Lag Exponential Moving Average (ZEMA), Triangular Moving Average (TMA), and Super Smoothing Filter(SSMA).

The strategy allows the configuration of two moving averages - a faster and a slower one, both chosen from 11 options. When the faster MA crosses over the slower MA, a long signal is generated. A short signal is generated when the faster MA crosses below the slower MA.

Additional features include ladder settings, take-profit, and stop-loss levels.

## Strategy Logic

Core strategy logic relies on crossovers between two moving averages to determine entry and exit.  

Entry condition is:  

long entry: fast MA > slow MAMA  
short entry: fast MA < slow MAMA

Exit is determined by one of the following three criteria:  

1. Take profit level reached  
2. Stop loss level reached   
3. Generates opposite signals (moving averages cross in opposite directions)

The strategy allows configuration of key parameters such as MA type and length, ladder settings, take profit and stop loss percentages. This provides flexibility to optimize strategies based on different market conditions and risk appetites.

## Advantage  

- Combine 11 different MA types to generate powerful signals  
- Main parameters are flexibly configurable    
- Take-profit and stop-loss features to protect profits and limit losses
- Trapezoid allows adding positions during strong trends  

## Risk  

- Like any technical indicator, MA crossovers may generate false signals  
- Over-optimizing for current market conditions may reduce future performance  
- Hard stop-loss exited correct trades with large volatility too early  

Risk management can be strengthened by using price confirmation for entry signals, using trailing stops instead of hard stops, and avoiding over-optimization.

## Optimize space  

This strategy can be improved in several ways:  

1. Add extra filters before entry, such as volume and price checks  
2. Systematically test the performance of different MA types and choose the best 1-2 types.    
3. Optimize MA length for specific trading instruments and timeframes   
4. Use trailing stop instead of hard stop     
5. Add phased take-profit as the trend extends    

## Summary  

The eleven moving average crossover strategy provides a systematic approach to trading crossovers. By combining signals across multiple MA indicators and allowing key parameters to be configured, it offers a powerful and flexible trading framework. Optimization and risk management will play a key role in enhancing performance. This strategy has strong potential in momentum trading but should be adjusted according to different market conditions.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|0|MA Type: : ZEMA|EMA|WMA|VWMA|SMMA|DEMA|TEMA|HullMA|SMA|TMA|SSMA|
|v_input_2|8|Fast MA Length|
|v_input_3_close|0|Fast MA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_4|21|Slow MA Length|
|v_input_5_close|0|Slow MA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_6|true|Pyramiding|
|v_input_7|false|Take Profit Long|
|v_input_8|false|Take Profit Short|
|v_input_9|3|Take Profit Long %|
|v_input_10|30|Take Profit Short %|
|v_input_11|false|Stop Loss Long|
|v_input_12|false|Stop Loss Short|
|v_input_13|3|Stop Loss %|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-15 00:00:00
end: 2024-01-14 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3

strategy(title = "[STRATEGY] MA Cross Eleven", overlay = true)

// MA - type, source, length

//  MA - type, source, length
//  SMA --> Simple
//  EMA --> Exponential
//  WMA --> Weighted
//  VWMA --> Volume Weighted
//  SMMA --> Smoothed
//  DEMA --> Double Exponential
//  TEMA --> Triple Exponential
//  HMA --> Hull
//  TMA --> Triangular
//  SSMA --> SuperSmoother filter
//  ZEMA --> Zero Lag Exponential

type = input(defval="ZEMA", title="MA Type: ", options=["SMA", "EMA", "WMA", "VWMA", "SMMA", "DEMA", "TEMA", "HullMA", "ZEMA", "TMA", "SSMA"])
len1 = input(defval=8, title="Fast MA Length", minval=1)
srcclose1 = input(close, "Fast MA Source")
len2 = input(defval=21, title="Slow MA Length", minval=1)
srcclose2 = input(close, "Slow MA Source")

// Returns MA input selection variant, default to SMA if blank or typo.

variant(type, src, len) =>
    v1 = sma(src, len)                                                  // Simple
    v2 = ema(src, len)                                                  // Exponential
    v3 = wma(src, len)                                                  // Weighted
    v4 = vwma(src, len)                                                 // Volume Weighted
    v5 = 0.0
    v5 := na(v5[1]) ? sma(src, len) : (v5[1] * (len - 1) + src) / len    // Smoothed
    v6 = 2 * v2 - ema(v2, len)                                          // Double Exponential
    v7 = 3 * (v2 - ema(v2, len)) + ema(ema(v2, len), len)               // Triple Exponential
    v8 = wma(2 * wma(src, len / 2) - wma(src, len), round(sqrt(len)))   // Hull
    v11 = sma(sma(src,len),len)                                         // Triangular
    // SuperSmoother filter
    // © 2013  John F. Ehlers
    a1 = exp(-1.414*3.14159 / len)
    b1 = 2*a1*cos(1.414*3.14159 / len)
    c2 = b1
    c3 = (-a1)*a1
    c1 = 1 - c2 - c3
    v9 = 0.0
    v9 := c1*(src + nz(src[1])) / 2 + c2*nz(v9[1]) + c3*nz(v9[2])
    // Zero Lag Exponential
    e = ema(v2, len)
    v10 = v2+(v2-e)
    // return variant, defaults to SMA if input invalid.
    type=="EMA"?v2 : type=="WMA"?v3 : type=="VWMA"?v4 : type=="SMMA"?v5 : type=="DEMA"?v6 : type=="TEMA"?v7 : type=="HullMA"?v8 : type=="SSMA"?v9 : type=="ZEMA"?v10 : type=="TMA"? v11: v1

ma_1 = variant(type, srcclose1, len1)
ma_2 = variant(type, srcclose2, len2)

plot(ma_1, title="Fast MA", color = green, linewidth=2, transp=0)
plot(ma_2, title="Slow MA", color = red, linewidth=2, transp=0)

longCond = na
shortCond = na
longCond := crossover(ma_1, ma_2)
shortCond := crossunder(ma_1, ma_2)

// Count your long short conditions for more control with Pyramiding

sectionLongs = 0
sectionLongs := nz(sectionLongs[1])
sectionShorts = 0
sectionShorts := nz(sectionShorts[1])

if longCond
    sectionLongs := sectionLongs + 1
    sectionShorts := 0

if shortCond
    sectionLongs := 0
    sectionShorts := sectionShorts + 1
    
// Pyramiding Inputs

pyrl = input(1, "Pyramiding")

// These check to see your signal and cross references it against the pyramiding settings above

longCondition = longCond and sectionLongs <= pyrl 
shortCondition = shortCond and sectionShorts <= pyrl 

// Get the price of the last opened long or short

last_open_longCondition = na
last_open_shortCondition = na
last_open_longCondition := longCondition ? high[1] : nz(last_open_longCondition[1])
last_open_shortCondition := shortCondition ? low[1] : nz(last_open_shortCondition[1])

// Check if your last postion was a long or a short

last_longCondition = na
last_shortCondition = na
last_longCondition := longCondition ? time : nz(last_longCondition[1])
last_shortCondition := shortCondition ? time : nz(last_shortCondition[1])

in_longCondition = last_longCondition > last_shortCondition
in_shortCondition = last_shortCondition > last_longCondition

// Take profit

isTPl = input(false, "Take Profit Long")
isTPs = input(false, "Take Profit Short")
tpl = input(3, "Take Profit Long %", type=float)
tps = input(30, "Take Profit Short %", type=float)
long_tp = isTPl and crossover(high, (1+(tpl/100))*last_open_longCondition) and in_longCondition  == 1
short_tp = isTPs and crossunder(low, (1-(tps/100))*last_open_shortCondition) and in_shortCondition == 1 

// Stop Loss

isSLl = input(false, "Stop Loss Long")
isSLs = input(false, "Stop Loss Short")
sl= 0.0
sl := input(3, "Stop Loss %", type=float)
long_sl = isSLl and crossunder(low, (1-(sl/100))*last_open_longCondition) and longCondition == 0 and in_longCondition == 1
short_sl = isSLs and crossover(high, (1+(sl/100))*last_open_shortCondition) and shortCondition == 0 and in_shortCondition == 1

// Create a single close for all the different closing conditions.

long_close = long_tp or long_sl ? 1 : 0
short_close = short_tp or short_sl ? 1 : 0

// Get the time of the last close

last_long_close = na
last_short_close = na
last_long_close := long_close ? time : nz(last_long_close[1])
last_short_close := short_close ? time : nz(last_short_close[1])

// Strategy entries

strategy.entry("long", strategy.long, when=longCondition == true, stop = open[1])
strategy.entry("short", strategy.short, when=shortCondition == true)
strategy.close("long", when = long_sl or long_tp)
strategy.close("short", when = short_sl or short_tp)
```

> Detail

https://www.fmz.com/strategy/438791

> Last Modified

2024-01-15 13:57:53
