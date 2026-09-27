
> Name

Pivot-Reversal-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/185a11cb484a9f73dbc.png)
 
### Overview

This article will analyze in detail a reversal trading strategy based on pivot points. The strategy calculates potential support and resistance pivot levels over a period, and identifies trend reversals when price breaks through these pivot levels, allowing reversal trades.

### Strategy Logic

The strategy mainly relies on two indicators: Pivot High and Pivot Low. Pivot highs and lows are the highest and lowest prices within a period, and can be obtained using the `pivothigh()` and `pivotlow()` functions. When computing pivot points, the periods to the left and right need to be set; this strategy uses 4 periods to the left and 2 periods to the right.  

When the highest price of the latest period is lower than the previous period's pivot high, it signals a reversal opportunity. If previous positions were short, long positions should now be considered to capitalize on the reversal. Similarly, when the latest period's lowest price is higher than the previous pivot low, existing long positions should consider reversing to short.

Specifically, the main logic is:

1. Compute pivot high/low levels 
2. Identify breakthroughs
   1. Long when price breaks above pivot low
   2. Short when price breaks below pivot high
3. Set stop loss levels

### Advantage Analysis

The biggest advantage of this strategy is identifying potential trend reversal points, which is crucial for reversal traders. Compared to other indicators, pivot points can more clearly identify key support/resistance levels without frequent false signals.

Moreover, the strategy has conditions for both long and short entries, covering different market situations to avoid missing opportunities. The use of stop loss controls risk and ensures a good risk/reward ratio.

In summary, this is a very practical reversal strategy.  

### Risk Analysis

Despite efforts to reduce false signals, any breakout-based strategy inevitably faces issues like premature or lagging signals. This could result in planning a long entry but the market has already reversed, or planning a short but a bull run suddenly erupts. Such inability to perfectly predict reversals is an inherent limitation of technical analysis.

Additionally, pivot points cannot guarantee perfect support/resistance levels either. Bad luck could result in stop loss hitting just before the real support level. Such uncertainty around key zones cannot be fully avoided.

### Enhancement Opportunities

1. Period optimization. The current left/right periods are set at 4 and 2. These can serve as initial values and be further optimized for each market.

2. Add filters with other indicators. For example, combine with volume to only consider breakouts as valid when accompanied by increasing volume. This helps avoid false breakouts.  

3. Dynamic stop loss. Currently stops are set with a buffer of one minimum tick above/below pivot levels. The buffer zone can be dynamically adjusted based on market volatility.

4. Operate only in trend direction. Currently long/short conditions are in parallel. An optimization is to only long in uptrends and short in downtrends based on a trend filter.

### Conclusion 

In summary, this is a simple yet practical reversal strategy. Identifying pivot points over a period and monitoring price breakthroughs forms the core idea for detecting potential trend reversals. The parallel long/short conditions maximize opportunities while stop losses manage risk.

The strategy logic is straightforward and easy to implement. The parameters are also intuitive for beginners. Further optimizations can improve performance for adoption. Overall this is a recommended strategy.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|4|leftBars|
|v_input_2|2|rightBars|
|v_input_3|true|From Day|
|v_input_4|3|From Month|
|v_input_5|2018|From Year|
|v_input_6|true|To Day|
|v_input_7|true|To Month|
|v_input_8|2100|To Year|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-12-11 00:00:00
end: 2023-12-17 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("Pivot Reversal Strategy", overlay=true)

leftBars  = input(4)
rightBars = input(2)

// backtesting date range
from_day   = input(defval = 1,    title = "From Day",   minval = 1)
from_month = input(defval = 3,    title = "From Month", minval = 1)
from_year  = input(defval = 2018, title = "From Year",  minval = 1970)

to_day     = input(defval = 1,    title = "To Day",     minval = 1)
to_month   = input(defval = 1,    title = "To Month",   minval = 1)
to_year    = input(defval = 2100, title = "To Year",    minval = 1970)

time_cond = (time > timestamp(from_year, from_month, from_day, 00, 00)) and (time < timestamp(to_year, to_month, to_day, 23, 59))

swh = pivothigh(leftBars, rightBars)
swl = pivotlow(leftBars, rightBars)

swh_cond = not na(swh)

hprice = 0.0
hprice := swh_cond ? swh : hprice[1]

le = false
le := swh_cond ? true : (le[1] and high > hprice ? false : le[1])

if (le and time_cond)
    strategy.entry("PivRevLE", strategy.long, comment="PivRevLE", stop=hprice + syminfo.mintick)

swl_cond = not na(swl)

lprice = 0.0
lprice := swl_cond ? swl : lprice[1]


se = false
se := swl_cond ? true : (se[1] and low < lprice ? false : se[1])

if (se and time_cond)
    strategy.entry("PivRevSE", strategy.short, comment="PivRevSE", stop=lprice - syminfo.mintick)

//plot(strategy.equity, title="equity", color=red, linewidth=2, style=areabr)
```

> Detail

https://www.fmz.com/strategy/435761

> Last Modified

2023-12-18 16:59:59
