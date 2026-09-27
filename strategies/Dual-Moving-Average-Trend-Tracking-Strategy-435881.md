
> Name

Dual-Moving-Average-Trend-Tracking-Strategy-435881

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/10960ebad05e95e1f81.png)
 
## Overview  

The Dual Moving Average Trend Tracking Strategy is a quantitative trading strategy that uses two moving averages with different periods to determine the trend direction of the market. It uses the long/short status of fast and slow moving averages to identify the trend and make trades along the trend direction.

## Principles  

The strategy employs two moving averages, including a fast moving average (e.g. 10-period) and a slow moving average (e.g. 30-period). If both moving averages are pointing up, it indicates an uptrend. If both moving averages are pointing down, it indicates a downtrend.   

Specifically, the strategy first calculates the fast and slow moving averages. Then it compares the current fast moving average with previous period to see if the current one is larger than the previous one. If yes, assign value 1 indicating up trend. Otherwise assign -1 for down trend. Do the same for the slow moving average.

Finally, determine the trend by the values of the two moving averages. If both values are 1, final decision is 1, indicating uptrend. If both are -1, final decision is -1, indicating downtrend. If the values are different, maintain previous trend decision.  

Upon the identification of trend direction, the strategy will long at uptrend and short at downtrend.  

## Advantages

The strategy has the following edges:

1. The logic is simple and easy to understand and implement.  
2. The dual moving averages help filter market noise and identify the trend.
3. Parameters of moving averages can be adjusted for different products and timeframes.  
4. No need to set stop loss or take profit, which lowers trade frequency and helps follow the trend.  
5. Can flexibly go long only or short only based on preference.

## Risks  

There are also some risks of the strategy:  

1. Moving averages may lag during sharp price change, causing missing best entry timing.
2. Fake breakout and incorrect crossover may happen, resulting in wrong trading signals.
3. No stop loss is set, unable to effectively limit single trade loss. 
4. Full position by default brings larger risk, needs cautious operation.

To reduce the risks, parameters of moving averages can be set more reasonably, other indicators can be introduced, stop loss and take profit can be set, and position size can be adjusted accordingly.

## Optimization  

The strategy can be further optimized in the following aspects:

1. Add more types of moving averages like SMA and EMA to utilize more charting tools.  
2. Introduce other assisting indicators like MACD and BOLL to improve accuracy.
3. Add trend line and support/resistance analysis for more precise trading signals.   
4. Set stop loss and take profit to control single trade loss.
5. Optimize position sizing based on fund usage, profit ratio etc.  

## Conclusion    

The Dual Moving Average Trend Tracking Strategy has a clear logic of using dual moving averages to filter noise and identify trend, and trade along the trend direction. It's a typical trend following strategy. Traders can choose long only or short only based on preference. There are still some risks of the strategy. Additional indicators, stop loss/take profit should be added to control risks. By doing so, long term steady profit can be achieved.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Long|
|v_input_2|true|Short|
|v_input_3|10|MA Fast (red)|
|v_input_4|30|MA Slow (blue)|
|v_input_5|0|MA Type: SMA|EMA|
|v_input_6_ohlc4|0|MA Source: ohlc4|high|low|open|hl2|hlc3|hlcc4|close|
|v_input_7|true|Show MAs|
|v_input_8|false|Show Background|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-12-12 00:00:00
end: 2023-12-18 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © noro
// 2020

//@version=4
strategy(title = "Noro's TrendMA Strategy", shorttitle = "TrendMA str", overlay = true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, pyramiding = 0, commission_value = 0.1)

//Settings
needlong = input(true, title = "Long")
needshort = input(true, title = "Short")
fast = input(10, minval = 1, title = "MA Fast (red)")
slow = input(30, minval = 2, title = "MA Slow (blue)")
type = input(defval = "SMA", options = ["SMA", "EMA"], title = "MA Type")
src = input(ohlc4, title = "MA Source")
showma = input(true, title = "Show MAs")
showbg = input(false, title = "Show Background")

//MAs
fastma = type == "EMA" ? ema(src, fast) : sma(src, fast)
slowma = type == "EMA" ? ema(src, slow) : sma(src, slow)

//Lines
colorfast = showma ? color.red : na
colorslow = showma ? color.blue : na
plot(fastma, color = colorfast, title = "MA Fast")
plot(slowma, color = colorslow, title = "MA Slow")

//Trend
trend1 = fastma > fastma[1] ? 1 : -1
trend2 = slowma > slowma[1] ? 1 : -1
trend = 0
trend := trend1 == 1 and trend2 == 1 ? 1 : trend1 == -1 and trend2 == -1 ? -1 : trend[1]

//Backgrouns
colbg = showbg == false ? na : trend == 1 ? color.lime : trend == -1 ? color.red : na
bgcolor(colbg, transp = 80)

//Trading
if trend == 1
    if needlong
        strategy.entry("Long", strategy.long)
    if needlong == false
        strategy.close_all()

if trend == -1
    if needshort
        strategy.entry("Short", strategy.short)
    if needshort == false
        strategy.close_all()
    
```

> Detail

https://www.fmz.com/strategy/435881

> Last Modified

2023-12-19 14:49:52
