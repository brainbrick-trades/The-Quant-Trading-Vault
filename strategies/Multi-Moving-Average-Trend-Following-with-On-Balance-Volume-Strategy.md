
> Name

Multi-Moving-Average-Trend-Following-with-On-Balance-Volume-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8e95531a65bc8788fde.png)
![IMG](https://www.fmz.com/upload/asset/2d910f6a572f3464e0964.png)




#### Overview
This strategy is a trend following system that combines multiple moving averages with the On-Balance Volume (OBV) indicator. It utilizes the synergy of 9-day Exponential Moving Average (EMA), 20-day Weighted Moving Average (WMA), and 200-day WMA to determine market trends, while incorporating OBV to confirm volume support for more reliable trading signals.

#### Strategy Principle
The strategy operates based on two core conditions:
1. Trend Confirmation: Requires 9-day EMA, 20-day WMA, and 200-day WMA to be in upward trends (current value greater than previous). This multi-timeframe trend confirmation method effectively filters out false breakouts.
2. Volume Confirmation: Uses OBV and its 13-period EMA. When the 13-period EMA of OBV is above the OBV line, it indicates volume supports the current price movement.

Long positions are only taken when both conditions are simultaneously met. Positions are closed when conditions are no longer satisfied.

#### Strategy Advantages
1. Multiple Confirmation Mechanism: Combines price trend and volume trend confirmation, increasing signal reliability.
2. Strong Adaptability: Through the use of different period moving averages, the strategy can adapt to various market environments.
3. Comprehensive Risk Control: Implements percentage-based position management with reasonable commission consideration.
4. Clear Visualization: Includes a complete graphical display system for better market condition understanding.

#### Strategy Risks
1. Lag Risk: Moving averages are inherently lagging indicators, potentially responding slowly in volatile markets.
2. Sideways Market Risk: May generate frequent false signals in range-bound markets.
3. Money Management Risk: Fixed percentage position sizing might not be flexible enough under certain market conditions.

#### Strategy Optimization Directions
1. Implement Dynamic Stop-Loss: Can introduce ATR or volatility-based dynamic stop-loss levels.
2. Optimize Position Management: Introduce volatility-based dynamic position sizing system.
3. Add Market Environment Filters: Incorporate market regime identification mechanisms to adjust strategy parameters under different market conditions.
4. Optimize Entry Timing: Can add momentum indicators like RSI to optimize entry points.

#### Summary
The strategy constructs a relatively complete trend following trading system by combining multiple moving averages and volume analysis. Its core strength lies in its multiple confirmation mechanism, while attention needs to be paid to the inherent lag in moving averages. Through the suggested optimization directions, there is room for further strategy enhancement.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-21 00:00:00
end: 2025-02-18 08:00:00
period: 5d
basePeriod: 5d
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("Strategy: Daily MAs + OBV", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10, commission_type=strategy.commission.percent, commission_value=0.1)

//=== Daily Moving Averages Calculation =========================
// Get daily timeframe values using request.security.
dailyEMA9   = request.security(syminfo.tickerid, "D", ta.ema(close, 9))
dailyWMA20  = request.security(syminfo.tickerid, "D", ta.wma(close, 20))
dailyWMA200 = request.security(syminfo.tickerid, "D", ta.wma(close, 200))

// Check if each moving average is trending upward (current > previous).
ema9_up   = dailyEMA9   > nz(dailyEMA9[1])
wma20_up  = dailyWMA20  > nz(dailyWMA20[1])
wma200_up = dailyWMA200 > nz(dailyWMA200[1])

trend_condition = ema9_up and wma20_up and wma200_up

//=== OBV and its 13-period EMA Calculation ================================
// Calculate OBV manually using a cumulative sum.
obv_val = ta.cum(close > close[1] ? volume : (close < close[1] ? -volume : 0))
// 13-period EMA of the OBV.
ema13_obv = ta.ema(obv_val, 13)

// Condition: 13-period EMA of OBV must be above the OBV value.
obv_condition = ema13_obv > obv_val

//=== Entry Condition ===================================================
// Both trend and OBV conditions must be met.
buy_condition = trend_condition and obv_condition

//=== Entry and Exit Orders =============================================
// Enter a long position when the buy condition is met and no position is open.
if buy_condition and strategy.position_size <= 0
    strategy.entry("Long", strategy.long)

// Exit the position when the condition is no longer met.
if not buy_condition and strategy.position_size > 0
    strategy.close("Long")

//=== Explicit Entry and Exit Markers ====================================
// Determine the exact bar where entry and exit occur.
entry_signal = (strategy.position_size > 0 and (strategy.position_size[1] <= 0))
exit_signal  = (strategy.position_size == 0 and (strategy.position_size[1] > 0))

plotshape(entry_signal, title="Entry Signal", location=location.belowbar, style=shape.labelup, text="BUY", color=color.new(color.green, 0), size=size.normal)
plotshape(exit_signal, title="Exit Signal", location=location.abovebar, style=shape.labeldown, text="SELL", color=color.new(color.red, 0), size=size.normal)

//=== Plots for Visualization ===============================================
// Plot daily moving averages.
plot(dailyEMA9, color=color.blue, title="Daily EMA 9")
plot(dailyWMA20, color=color.orange, title="Daily WMA 20")
plot(dailyWMA200, color=color.red, title="Daily WMA 200")

// Plot OBV and its 13-period EMA using color.new() to specify transparency.
plot(obv_val, color=color.new(color.gray, 30), title="OBV")
plot(ema13_obv, color=color.new(color.green, 0), title="13-Period EMA OBV")
```

> Detail

https://www.fmz.com/strategy/482796

> Last Modified

2025-02-20 14:57:20
