
> Name

Multi-Timeframe-Trend-Following-Strategy-with-ATR-Based-Take-Profit-and-Stop-Loss

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/141a363bbd1c1f11f76.png)


#### Overview
This is a trend following trading strategy that combines UT Bot and 50-period Exponential Moving Average (EMA). The strategy operates primarily on a 1-minute timeframe while using a 5-minute timeframe trend line as a directional filter. It employs the ATR indicator for dynamic stop loss calculation and implements dual take profit targets to optimize returns.

#### Strategy Principles
The core logic is based on the following key components:
1. Using UT Bot to calculate dynamic support and resistance levels
2. Utilizing 50-period EMA on 5-minute timeframe for overall trend direction
3. Combining 21-period EMA and UT Bot signals for specific entry points
4. Setting dynamic trailing stops through ATR multipliers
5. Implementing two take profit targets at 0.5% and 1%, each closing 50% of the position

Trade signals are triggered when price breaks through UT Bot's support/resistance levels and 21-period EMA crosses with UT Bot, provided the price is in the correct direction relative to the 5-minute 50-period EMA.

#### Strategy Advantages
1. Multi-timeframe combination enhances trading reliability
2. Dynamic ATR stops adapt to market volatility
3. Dual take profit targets balance returns and win rate
4. Heikin Ashi candlesticks filter out some false breakouts
5. Flexible trade direction options (long only, short only, or both)

#### Strategy Risks
1. Short timeframe trading may face high spread and commission costs
2. May generate frequent false signals in ranging markets
3. Multiple conditions may cause missed trading opportunities
4. ATR parameters need optimization for different markets

#### Optimization Directions
1. Add volume indicators for additional confirmation
2. Consider incorporating more market sentiment indicators
3. Develop adaptive parameters for different market volatility characteristics
4. Add trading session filters
5. Develop more intelligent position sizing system

#### Summary
This strategy constructs a complete trading system through the combination of multiple technical indicators and timeframes. It includes not only clear entry and exit conditions but also comprehensive risk management mechanisms. While parameter optimization is still needed for specific market conditions in practical application, the overall framework demonstrates good practicality and extensibility.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-18 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
//Created by Nasser mahmoodsani' all rights reserved
// E-mail : e.man4858@gmail.com

strategy("UT Bot Strategy with T/P and S/L and Trend EMA", overlay=true)

// Inputs
along = input(1, title='Key Value (Sensitivity - Long)', group="LONG")
clong = input(10, title='ATR Period (Long)', group="LONG")
h = input(true, title='Signals from Heikin Ashi Candles')
ashort = input(7, title='Key Value (Sensitivity - Short)', group="SHORT")
cshort = input(2, title='ATR Period (Short)', group="SHORT")
tradeType = input.string("Both", title="Trade Type", options=["Buy Only", "Sell Only", "Both"])
tp1_percent = input.float(0.5, title="TP1 Percentage", step=0.1, group="TP Settings") // TP1 % input
tp2_percent = input.float(1.0, title="TP2 Percentage", step=0.1, group="TP Settings") // TP2 % input
sl_percent = input.float(1.0, title="Stop Loss Percentage", step=0.1, group="TP Settings") // SL % input
sl_in_percent = input(true, title="Use Stop Loss in Percentage", group="TP Settings")
tp1_qty = input.float(0.5, title="Take Profit 1 Quantity (as % of position size)", minval=0.0, maxval=1.0, step=0.1)
tp2_qty = input.float(0.5, title="Take Profit 2 Quantity (as % of position size)", minval=0.0, maxval=1.0, step=0.1)

// Check that total quantities for TPs do not exceed 100%
if tp1_qty + tp2_qty > 1
    runtime.error("The sum of Take Profit quantities must not exceed 100%.")

// Calculate 50 EMA from 5-Minute Timeframe
trendEmaPeriod = 50
trendEma_5min = request.security(syminfo.tickerid, "5", ta.ema(close, trendEmaPeriod))
plot(trendEma_5min, title="Trend EMA (5-Min)", color=color.blue, linewidth=2)

// Calculations 
xATRlong = ta.atr(clong)
xATRshort = ta.atr(cshort)
nLosslong = along * xATRlong
nLossshort = ashort * xATRshort

src = h ? request.security(ticker.heikinashi(syminfo.tickerid), timeframe.period, close) : close

// LONG
var float xATRTrailingStoplong = na
var float stopLossLong = na
var float takeProfit1 = na
var float takeProfit2 = na

iff_1long = src > nz(xATRTrailingStoplong[1], 0) ? src - nLosslong : src + nLosslong
iff_2long = src < nz(xATRTrailingStoplong[1], 0) and src[1] < nz(xATRTrailingStoplong[1], 0) ? math.min(nz(xATRTrailingStoplong[1]), src + nLosslong) : iff_1long
xATRTrailingStoplong := src > nz(xATRTrailingStoplong[1], 0) and src[1] > nz(xATRTrailingStoplong[1], 0) ? math.max(nz(xATRTrailingStoplong[1]), src - nLosslong) : iff_2long

buy = src > xATRTrailingStoplong and ta.crossover(ta.ema(src, 21), xATRTrailingStoplong) and close > trendEma_5min

if buy and (tradeType == "Buy Only" or tradeType == "Both")
    takeProfit1 := close * (1 + tp1_percent / 100)
    takeProfit2 := close * (1 + tp2_percent / 100)

    // Calculate stop loss based on percentage or ATR
    if sl_in_percent
        stopLossLong := close * (1 - sl_percent / 100)
    else
        stopLossLong := close - nLosslong

    strategy.entry("Long", strategy.long)
    strategy.exit("Take Profit 1", from_entry="Long", limit=takeProfit1, qty=strategy.position_size * tp1_qty)
    strategy.exit("Take Profit 2", from_entry="Long", limit=takeProfit2, qty=strategy.position_size * tp2_qty)
    strategy.exit("Stop Loss", from_entry="Long", stop=stopLossLong, qty=strategy.position_size)

    // // Create Position Projectile for Long
    // var line tpLineLong1 = na
    // var line tpLineLong2 = na
    // var line slLineLong = na
    // var label entryLabelLong = na

    // // Update projectile on entry
    // line.delete(tpLineLong1)
    // line.delete(tpLineLong2)
    // line.delete(slLineLong)
    // label.delete(entryLabelLong)

    // tpLineLong1 := line.new(x1=bar_index, y1=takeProfit1, x2=bar_index + 1, y2=takeProfit1, color=color.green, width=2, style=line.style_solid)
    // tpLineLong2 := line.new(x1=bar_index, y1=takeProfit2, x2=bar_index + 1, y2=takeProfit2, color=color.green, width=2, style=line.style_dashed)
    // slLineLong := line.new(x1=bar_index, y1=stopLossLong, x2=bar_index + 1, y2=stopLossLong, color=color.red, width=2, style=line.style_solid)

// SHORT
var float xATRTrailingStopshort = na
var float stopLossShort = na
var float takeProfit1Short = na
var float takeProfit2Short = na

iff_1short = src > nz(xATRTrailingStopshort[1], 0) ? src - nLossshort : src + nLossshort
iff_2short = src < nz(xATRTrailingStopshort[1], 0) and src[1] < nz(xATRTrailingStopshort[1], 0) ? math.min(nz(xATRTrailingStopshort[1]), src + nLossshort) : iff_1short
xATRTrailingStopshort := src > nz(xATRTrailingStopshort[1], 0) and src[1] > nz(xATRTrailingStopshort[1], 0) ? math.max(nz(xATRTrailingStopshort[1]), src - nLossshort) : iff_2short

sell = src < xATRTrailingStopshort and ta.crossover(xATRTrailingStopshort, ta.ema(src, 21)) and close < trendEma_5min

if sell and (tradeType == "Sell Only" or tradeType == "Both")
    takeProfit1Short := close * (1 - tp1_percent / 100)
    takeProfit2Short := close * (1 - tp2_percent / 100)

    // Calculate stop loss based on percentage or ATR
    if sl_in_percent
        stopLossShort := close * (1 + sl_percent / 100)
    else
        stopLossShort := close + nLossshort

    strategy.entry("Short", strategy.short)
    strategy.exit("Take Profit 1 Short", from_entry="Short", limit=takeProfit1Short, qty=strategy.position_size * tp1_qty)
    strategy.exit("Take Profit 2 Short", from_entry="Short", limit=takeProfit2Short, qty=strategy.position_size * tp2_qty)
    strategy.exit("Stop Loss Short", from_entry="Short", stop=stopLossShort, qty=strategy.position_size)

    // Create Position Projectile for Short
    // var line tpLineShort1 = na
    // var line tpLineShort2 = na
    // var line slLineShort = na
    // var label entryLabelShort = na

    // // Update projectile on entry
    // line.delete(tpLineShort1)
    // line.delete(tpLineShort2)
    // line.delete(slLineShort)
    // label.delete(entryLabelShort)

    // tpLineShort1 := line.new(x1=bar_index, y1=takeProfit1Short, x2=bar_index + 1, y2=takeProfit1Short, color=color.green, width=2, style=line.style_solid)
    // tpLineShort2 := line.new(x1=bar_index, y1=takeProfit2Short, x2=bar_index + 1, y2=takeProfit2Short, color=color.green, width=2, style=line.style_dashed)
    // slLineShort := line.new(x1=bar_index, y1=stopLossShort, x2=bar_index + 1, y2=stopLossShort, color=color.red, width=2, style=line.style_solid)

// Updating Stop Loss after hitting Take Profit 1
if buy and close >= takeProfit1
    strategy.exit("Adjusted Stop Loss", from_entry="Long", stop=close)

// Updating Stop Loss after hitting Take Profit 1 for Short
if sell and close <= takeProfit1Short
    strategy.exit("Adjusted Stop Loss Short", from_entry="Short", stop=close)

```

> Detail

https://www.fmz.com/strategy/475592

> Last Modified

2024-12-20 14:14:32
