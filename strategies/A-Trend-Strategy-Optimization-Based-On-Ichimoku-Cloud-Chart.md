
> Name

A-Trend-Strategy-Optimization-Based-On-Ichimoku-Cloud-Chart

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/f286c755db8ffda144.png)
 
## Overview  

This strategy combines Ichimoku cloud chart with various auxiliary indicators to track the trends. It mainly uses Ichimoku cloud to determine the trend direction and MACD, CMF, TSI and other indicators for filtering to improve the signal quality. This is a strong trend strategy based on comprehensive judgments of multiple factors.

## Principles  

This strategy mainly utilizes the transformation of Ichimoku cloud to judge the trend direction. It goes long when the Tenkan-sen crosses above the cloud and goes short when the Tenkan-sen crosses below. Meanwhile, it uses Chikou Span, MACD histogram, CMF and TSI for multi-layer filtering to ensure the signal quality.   

Specifically, the long signal is triggered when:

1. Tenkan-sen crosses above the cloud  
2. The cloud is wide and Tenkan-sen is above Kijun-sen
3. Chikou Span is above the 0-line  
4. The closing price is above the cloud
5. MACD histogram is above 0
6. CMF is greater than 0.1  
7. TSI is above 0

The short signal is triggered when the above conditions are reversed. By such comprehensive criteria, most of the false signals can be filtered out and the major trends in the market are captured.   

## Advantages

The biggest advantage of this strategy is filtering out false signals and catching strong trends by combining multiple indicators. Specifically:  

1. Ichimoku cloud determines the major trend direction  
2. Auxiliary indicators further filter out signals and reduce risks
3. Comprehensively considers multiple timeframes for more reliable signals  
4. Strict rules to trade only high quality setups and avoid choppy markets   
5. Trend following mechanism to maximize trend profits  

Through such judgments, the strategy can effectively identify the mid-long term hot sectors and profit from trend trading.

## Risks  

The main risks of this strategy include:  

1. False breakout risk causing wrong signals 
2. Trend reversal risk leading to the loss of all profits
3. Relatively low trading frequency missing opportunities  

Solutions:

1. Relax filtering criteria properly to increase trade frequency 
2. Add stop loss condition to limit loss size
3. Optimize parameters to improve signal accuracy

## Enhancement  

The main optimization directions:  

1. Parameter optimization through more backtests to find better parameter combination

2. Add stop loss mechanism to control risks 

3. Add trailing stop loss to lock in profits  

4. Test more indicators to find better filter combination  

5. Add rules to distinguish real breakout 

## Conclusion  

This strategy effectively combines Ichimoku cloud and multiple auxiliary indicators. Further improvements on parameter optimization, stop loss mechanism, indicator selection can enhance the stability and signal quality for higher steady returns. The strategy has strong practical value.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|10|Tenkan-Sen Bars|
|v_input_2|30|Kijun-Sen Bars|
|v_input_3|52|Senkou-Span B Bars|
|v_input_4|26|Chikou-Span Offset|
|v_input_5|26|Senkou-Span Offset|
|v_input_6|true|Long Entry|
|v_input_7|true|Short Entry|
|v_input_8|17|Fast Length|
|v_input_9|28|Slow Length|
|v_input_10_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_11|5|Signal Smoothing|
|v_input_12|true|Simple MA(Oscillator)|
|v_input_13|true|Simple MA(Signal Line)|
|v_input_14|8|CMF Length|
|v_input_15|8|Long Length|
|v_input_16|8|Short Length|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-11 00:00:00
end: 2024-01-13 14:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © exlux99

//@version=4
strategy("Ichimoku with MACD/ CMF/ TSI", overlay=true, margin_long=0, margin_short=0)



//Inputs
ts_bars = input(10, minval=1, title="Tenkan-Sen Bars")
ks_bars = input(30, minval=1, title="Kijun-Sen Bars")
ssb_bars = input(52, minval=1, title="Senkou-Span B Bars")
cs_offset = input(26, minval=1, title="Chikou-Span Offset")
ss_offset = input(26, minval=1, title="Senkou-Span Offset")
long_entry = input(true, title="Long Entry")
short_entry = input(true, title="Short Entry")

middle(len) => avg(lowest(len), highest(len))

// Ichimoku Components
tenkan = middle(ts_bars)
kijun = middle(ks_bars)
senkouA = avg(tenkan, kijun)
senkouB = middle(ssb_bars)


ss_high = max(senkouA[ss_offset-1], senkouB[ss_offset-1])
ss_low = min(senkouA[ss_offset-1], senkouB[ss_offset-1])

// Entry/Exit Signals
fast_length = input(title="Fast Length", type=input.integer, defval=17)
slow_length = input(title="Slow Length", type=input.integer, defval=28)
src = input(title="Source", type=input.source, defval=close)
signal_length = input(title="Signal Smoothing", type=input.integer, minval = 1, maxval = 50, defval = 5)
sma_source = input(title="Simple MA(Oscillator)", type=input.bool, defval=true)
sma_signal = input(title="Simple MA(Signal Line)", type=input.bool, defval=true)

// Calculating
fast_ma = sma_source ? sma(src, fast_length) : ema(src, fast_length)
slow_ma = sma_source ? sma(src, slow_length) : ema(src, slow_length)
macd = fast_ma - slow_ma
signal = sma_signal ? sma(macd, signal_length) : ema(macd, signal_length)
hist = macd - signal


tk_cross_bull = tenkan > kijun
tk_cross_bear = tenkan < kijun
cs_cross_bull = mom(close, cs_offset-1) > 0
cs_cross_bear = mom(close, cs_offset-1) < 0
price_above_kumo = close > ss_high
price_below_kumo = close < ss_low


//CMF
lengthA = input(8, minval=1, title="CMF Length")
ad = close==high and close==low or high==low ? 0 : ((2*close-low-high)/(high-low))*volume
mf = sum(ad, lengthA) / sum(volume, lengthA)


//TSI
long = input(title="Long Length", type=input.integer, defval=8)
short = input(title="Short Length", type=input.integer, defval=8)
price = close
double_smooth(src, long, short) =>
	fist_smooth = ema(src, long)
	ema(fist_smooth, short)
pc = change(price)
double_smoothed_pc = double_smooth(pc, long, short)
double_smoothed_abs_pc = double_smooth(abs(pc), long, short)
tsi_value = 100 * (double_smoothed_pc / double_smoothed_abs_pc)



bullish = tk_cross_bull and cs_cross_bull and price_above_kumo and hist > 0 and mf > 0.1 and tsi_value > 0
bearish = tk_cross_bear and cs_cross_bear and price_below_kumo and hist < 0  and mf < -0.1 and tsi_value < 0



strategy.entry("Long", strategy.long, when=bullish and long_entry)
strategy.entry("Short", strategy.short, when=bearish and short_entry)

strategy.close("Long", when=bearish and not short_entry)
strategy.close("Short", when=bullish and not long_entry)
```

> Detail

https://www.fmz.com/strategy/439352

> Last Modified

2024-01-19 14:45:21
