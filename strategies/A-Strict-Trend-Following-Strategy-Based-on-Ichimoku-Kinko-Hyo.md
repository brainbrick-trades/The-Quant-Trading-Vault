
> Name

A-Strict-Trend-Following-Strategy-Based-on-Ichimoku-Kinko-Hyo

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/12cea905217ba13a11a.png)
 
## Overview

This is a trend following strategy designed based on the Ichimoku Kinko Hyo indicator. It sets very strict entry rules using multiple metrics from the Ichimoku system, while having simple exits to lock in trends. The strategy is intended for long-term trend trading.  

## Strategy Logic

The strategy uses the relationship between the conversion line, base line, leading span A, leading span B and price itself from the Ichimoku system to determine trend direction and strength. The specific rules are:

1. Current cloud expands and price above cloud;
2. Future cloud expands;
3. Base line above cloud; 
4. Conversion line above base line;
5. Price above conversion line;
6. Current and future leading span A, leading span B, base line and conversion line angles pointing up.

It triggers buy signal when all above conditions are met, and sell signal when all conditions are inverted.  

The strategy also sets leading span A as the stop loss line. It flattens positions when price crosses below stop loss.

## Advantage Analysis 

This is an extremely strict strategy, which effectively avoids false signals and locks in major trends. It also utilizes multiple indicators to determine the trend, preventing systemic failures of single metrics.

The strategy favors long holding periods, thus reducing trading frequency and cost from commissions and slippage. 

## Risk Analysis

The stop loss of this strategy is relatively wide, set at leading span A, which poses the risk of large losses per trade. Consider tightening stops or adding filters to control risks.

Also, there are fewer signals generated, which may miss some short-term opportunities. Traders seeking higher frequency may consider relaxing some entry rules.

## Improvement Opportunities

Fine tune entry rules to strike a balance between getting more signals vs filtering out noise.

Explore more advanced stop loss techniques like automated or remote stops to control single trade loss.

Test impact of different parameter sets to find optimum values. Incorporate other indicators to achieve more accurate position sizing.

## Conclusion

This is an exceptionally strict trend following strategy based on Ichimoku Kinko Hyo system. By using multiple Ichimoku metrics to gauge trend, it avoids false signals reliably. The wide stop loss allows it to ride long term trends. With parameter tuning and risk management enhancements, this strategy can evolve into a formidable system for quantitative trading.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|20|ATR Period|
|v_input_2|9|Conversion Line Period|
|v_input_3|26|Base Line Period|
|v_input_4|52|Span B Period|
|v_input_5|26|Displacement|
|v_input_6|true|Min Current Cloud ATR|
|v_input_7|false|Min Future Cloud ATR|
|v_input_8|true|Check Base Line above Cloud?|
|v_input_9|true|Check Conversion Line above Base Line?|
|v_input_10|true|Check Price above Conversion Line?|
|v_input_11|false|Check Current Span A is pointing Up?|
|v_input_12|false|Check Current Span B is pointing Up?|
|v_input_13|true|Check Future Span A is pointing Up?|
|v_input_14|true|Check Future Span B is pointing Up?|
|v_input_15|true|Check Base Line is Pointing Up?|
|v_input_16|true|Check Conversion Line is Pointing Up?|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-10 00:00:00
end: 2024-01-17 00:00:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy(title="BadaBing Ichimoku", shorttitle="BadaBing", overlay=true)

atr_period = input(title="ATR Period",  defval=20)
conversion_period = input(title="Conversion Line Period", defval=9, minval=1)
base_period = input(title="Base Line Period", defval=26, minval=1)
span_b_period = input(title="Span B Period", defval=52, minval=1)
displacement = input(title="Displacement", defval=26, minval=1)
min_current_cloud_atr = input(title="Min Current Cloud ATR", type=float, defval=1.0)
min_future_cloud_atr = input(title="Min Future Cloud ATR", type=float, defval=0)
check_base_line_above_cloud = input(title="Check Base Line above Cloud?", type=bool, defval=true)
check_conversion_line_above_base_line = input(title="Check Conversion Line above Base Line?", type=bool, defval=true)
check_price_above_conversion_line = input(title="Check Price above Conversion Line?", type=bool, defval=true)
check_span_a_point_up = input(title="Check Current Span A is pointing Up?", type=bool, defval=false)
check_span_b_point_up = input(title="Check Current Span B is pointing Up?", type=bool, defval=false)
check_future_span_a_point_up = input(title="Check Future Span A is pointing Up?", type=bool, defval=true)
check_future_span_b_point_up = input(title="Check Future Span B is pointing Up?", type=bool, defval=true)
check_base_line_point_up = input(title="Check Base Line is Pointing Up?", type=bool, defval=true)
check_conversion_line_point_up = input(title="Check Conversion Line is Pointing Up?", type=bool, defval=true)

bullish_color = #ccff99
bearish_color = #ff704d
span_a_color = #0000cc
span_b_color = #000066
conversion_color = #ff99ff
base_color = #4da6ff
bull_signal_color = #228b22
bear_signal_color = #990000

donchian(len) => avg(lowest(len), highest(len))
bchange(series) => series and not series[1]

conversion_line = donchian(conversion_period)
base_line = donchian(base_period)
future_span_a = avg(conversion_line, base_line)
future_span_b = donchian(span_b_period)
span_a = future_span_a[displacement]
span_b = future_span_b[displacement]
current_atr = atr(atr_period)

min_cloud_width = min_current_cloud_atr * current_atr
current_cloud_long_flag = span_a > (span_b + min_cloud_width)
current_cloud_short_flag = span_a < (span_b - min_cloud_width)
future_cloud_long_flag = future_span_a > (future_span_b + min_cloud_width)
future_cloud_short_flag = future_span_a < (future_span_b - min_cloud_width)
base_line_long_flag = check_base_line_above_cloud ? (base_line > span_a) : true
base_line_short_flag = check_base_line_above_cloud ? (base_line < span_a) : true
conversion_line_long_flag = check_conversion_line_above_base_line ? (conversion_line > base_line) : true
conversion_line_short_flag = check_conversion_line_above_base_line ? (conversion_line < base_line) : true
price_long_flag = check_price_above_conversion_line ? (close > conversion_line) : true
price_short_flag = check_price_above_conversion_line ? (close < conversion_line) : true
span_a_point_long_flag = check_span_a_point_up ? (span_a > span_a[1]) : true
span_a_point_short_flag = check_span_a_point_up ? (span_a < span_a[1]) : true
span_b_point_long_flag = check_span_b_point_up ? (span_b > span_b[1]) : true
span_b_point_short_flag = check_span_b_point_up ? (span_b < span_b[1]) : true
future_span_a_point_long_flag = check_future_span_a_point_up ? (future_span_a > future_span_a[1]) : true
future_span_a_point_short_flag = check_future_span_a_point_up ? (future_span_a < future_span_a[1]) : true
future_span_b_point_long_flag = check_future_span_b_point_up ? (future_span_b > future_span_b[1]) : true
future_span_b_point_short_flag = check_future_span_b_point_up ? (future_span_b < future_span_b[1]) : true
base_line_point_long_flag = check_base_line_point_up ? (base_line > base_line[1]) : true
base_line_point_short_flag = check_base_line_point_up ? (base_line < base_line[1]) : true
conversion_line_point_long_flag = check_conversion_line_point_up ? (conversion_line > conversion_line[1]) : true
conversion_line_point_short_flag = check_conversion_line_point_up ? (conversion_line < conversion_line[1]) : true


bada_long = bchange(current_cloud_long_flag)
   or bchange(future_cloud_long_flag)
   or bchange(base_line_long_flag)
   or bchange(conversion_line_long_flag)
   or bchange(price_long_flag)
   or bchange(span_a_point_long_flag)
   or bchange(span_b_point_long_flag)
   or bchange(future_span_a_point_long_flag)
   or bchange(future_span_b_point_long_flag)
   or bchange(base_line_point_long_flag)
   or bchange(conversion_line_point_long_flag)
bada_short = bchange(current_cloud_short_flag)
   or bchange(future_cloud_short_flag)
   or bchange(base_line_short_flag)
   or bchange(conversion_line_short_flag)
   or bchange(price_short_flag)
   or bchange(span_a_point_short_flag)
   or bchange(span_b_point_short_flag)
   or bchange(future_span_a_point_short_flag)
   or bchange(future_span_b_point_short_flag)
   or bchange(base_line_point_short_flag)
   or bchange(conversion_line_point_short_flag)
bada_color = bada_long ? bull_signal_color : bear_signal_color
plotshape(bada_long or bada_short, title="bada",
  style=shape.circle,
  location=location.belowbar,
  color=bada_color,
  transp=50)
   
bing_long = current_cloud_long_flag
   and future_cloud_long_flag
   and base_line_long_flag
   and conversion_line_long_flag
   and price_long_flag
   and span_a_point_long_flag
   and span_b_point_long_flag
   and future_span_a_point_long_flag
   and future_span_b_point_long_flag
   and base_line_point_long_flag
   and conversion_line_point_long_flag
bing_short = current_cloud_short_flag
   and future_cloud_short_flag
   and base_line_short_flag
   and conversion_line_short_flag
   and price_short_flag
   and span_a_point_short_flag
   and span_b_point_short_flag
   and future_span_a_point_short_flag
   and future_span_b_point_short_flag
   and base_line_point_short_flag
   and conversion_line_point_short_flag
bing_color = bing_long ? bull_signal_color : bear_signal_color
plotshape(bchange(bing_long or bing_short), title="bing",
   style=shape.diamond,
   location=location.abovebar,
   color=bing_color,
   transp=0)

c = plot(conversion_line, color=conversion_color, title="Conversion Line", linewidth=2)
b = plot(base_line, color=base_color, title="Base Line", linewidth=2)
p1 = plot(future_span_a, offset = displacement, color=span_a_color, title="Span A", linewidth=3)
p2 = plot(future_span_b, offset = displacement, color=red, title="Span B", linewidth=3)
fill(p1, p2, color = future_span_a > future_span_b ? bullish_color : bearish_color, transp = 60)

strategy.entry("long", true, 1, when=bing_long)
strategy.exit("stop", "long", stop=span_a)
strategy.close("long", when=close < base_line)
strategy.entry("short", false, 1, when=bing_short)
strategy.exit("stop", "short", stop=span_a)
strategy.close("short", when=close > base_line)

```

> Detail

https://www.fmz.com/strategy/439226

> Last Modified

2024-01-18 15:03:28
