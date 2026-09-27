
> Name

Dynamic-Re-entry-Buy-only-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1e1ef50ca48841c4eca.png)
 
### Overview

This strategy is a buy-only trading system that generates buy signals based on moving average crossovers and the Weekly Commodity Channel Index (CCI) or Weekly Average Directional Index (ADX). It produces buy signals when the fast moving average crosses above the slow moving average and when the Weekly CCI and/or Weekly ADX meet specified conditions.  

The strategy also allows for dynamic re-entry, which means it can open new long positions if the price goes above the three moving averages after an exit. However, the strategy will exit the long position if the price closes below the third moving average.

### Strategy Principle  

The script defines the conditions for generating buy signals. It checks two conditions for a valid buy signal:

- The fast moving average crosses above the slow moving average
- The user can choose to filter trades using Weekly CCI or Weekly ADX

**Dynamic Re-entry:** If there is no active long position and the price is above all three moving averages, a new long position is opened.  

**Exit Condition:** If the closing price drops below the third moving average, the script closes the long position.

### Advantage Analysis

The advantages of this strategy include:

1. Using multiple technical indicators to filter signals reduces false signals
2. The dynamic re-entry mechanism maximizes the capture of trends  
3. Being long-only avoids the risks of shorting

### Risk Analysis  

The risks of this strategy include:  

1. There is some risk of whipsaws
2. Long holding times could be too long, requiring stops
3. Poor parameter settings may cause too frequent trading

Solutions:

1. Use better parameter combinations and indicator combinations to filter 
2. Set reasonable stop losses
3. Adjust parameters to ensure stability  

### Optimization Directions

This strategy can be optimized by:

1. Testing more technical indicator combinations to find better entry timing
2. Optimizing parameters to find the best parameter combinations  
3. Adding stop loss mechanisms to control single loss
4. Adding position sizing to increase/decrease positions based on market conditions  

### Summary

This dynamic re-entry buy-only strategy integrates multiple technical indicators to determine entry timing and adopts a dynamic re-entry design to track trends in real-time. Being long-only avoids shorting risks. Through parameter optimization, stop losses, and position sizing, this strategy can be implemented in live trading to control risk while capturing excess returns.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|20|Fast Moving Average Length|
|v_input_2|30|Slow Moving Average Length|
|v_input_3|100|Third Moving Average Length|
|v_input_4|14|CCI Period for Weekly CCI|
|v_input_5|true|Use CCI for Entry|
|v_input_6|true|Use ADX for Entry|
|v_input_7|14|ADX Length|
|v_input_8|25|ADX Threshold|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-12-12 00:00:00
end: 2023-12-18 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Buy Only Strategy with Dynamic Re-Entry and Exit", overlay=true)

// Input Parameters
fast_length = input(20, title="Fast Moving Average Length")
slow_length = input(30, title="Slow Moving Average Length")
third_ma_length = input(100, title="Third Moving Average Length")
cci_period = input(14, title="CCI Period for Weekly CCI")
use_cci = input(true, title="Use CCI for Entry")
use_adx = input(true, title="Use ADX for Entry")
adx_length = input(14, title="ADX Length")
adx_threshold = input(25, title="ADX Threshold")

// Calculate Moving Averages
fast_ma = ta.sma(close, fast_length)
slow_ma = ta.sma(close, slow_length)
third_ma = ta.sma(close, third_ma_length)

// Weekly Commodity Channel Index (CCI) with user-defined period
weekly_cci = request.security(syminfo.tickerid, "W", ta.cci(close,  cci_period))

// Weekly Average Directional Index (ADX)
dirmov = hlc3
plus = ta.change(dirmov) > 0 ? ta.change(dirmov) : 0
minus = ta.change(dirmov) < 0 ? -ta.change(dirmov) : 0
trur = ta.rma(ta.tr, adx_length)
plusDI = ta.rma(plus, adx_length) / trur * 100
minusDI = ta.rma(minus, adx_length) / trur * 100
sum = plusDI + minusDI
DX = sum == 0 ? 0 : math.abs(plusDI - minusDI) / sum * 100
ADX = ta.rma(DX, adx_length)

// Entry Conditions (Buy Only and Weekly CCI > 100 and/or Weekly ADX > 25)
cci_condition = use_cci ? (weekly_cci > 100) : false
adx_condition = use_adx ? (ADX > adx_threshold) : false
long_condition = ta.crossover(fast_ma, slow_ma) and (cci_condition or adx_condition)

// Exit Condition and Dynamic Re-Entry
exit_condition = close < third_ma
re_entry_condition = close > fast_ma and close > slow_ma and close > third_ma and weekly_cci > 100

// Entry and Exit Signals
strategy.entry("Long", strategy.long, when=long_condition)
strategy.close("Long", when=exit_condition)

// Dynamic Re-Entry and Exit
if strategy.position_size == 0 and re_entry_condition
    strategy.entry("Long", strategy.long)

if strategy.position_size > 0 and close < third_ma
    strategy.close("Long")

// Plot Weekly CCI and ADX for reference
plot(weekly_cci, title="Weekly CCI", color=color.orange)
plot(ADX, title="Weekly ADX", color=color.blue)

```

> Detail

https://www.fmz.com/strategy/435867

> Last Modified

2023-12-19 13:56:55
