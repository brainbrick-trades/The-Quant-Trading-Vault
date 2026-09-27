
> Name

Multi-Temporal-Trend-Identification-Adaptive-Position-Management-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d971ec77a4a9f73f63cf.png)
![IMG](https://www.fmz.com/upload/asset/2d85b6927ffe4f8634c3c.png)




#### Overview
This strategy is a trend-following trading system based on Supertrend and Double Exponential Moving Average (DEMA). It combines Supertrend's trend direction identification capability with DEMA's trend confirmation function to build a reliable trading decision framework. The system supports bilateral trading and features a dynamic position adjustment mechanism that can flexibly switch between long and short positions according to market conditions.

#### Strategy Principles
The core logic of the strategy is based on the following key components:
1. Supertrend indicator: Uses ATR period of 10 and factor value of 3.0 to capture price trend turning points.
2. DEMA indicator: Employs a 100-period double exponential moving average to filter market noise and confirm trend reliability.
3. Trading signal generation mechanism:
   - Long signal: Triggered when price crosses above Supertrend and closing price is above DEMA
   - Short signal: Triggered when price crosses below Supertrend and closing price is below DEMA
4. Position management: System supports flexible position adjustment, including direct opening, reversal, and closing operations.

#### Strategy Advantages
1. Multiple confirmation mechanism: Combining Supertrend and DEMA indicators significantly improves trading signal reliability.
2. Flexible position management: Supports bilateral trading and can dynamically adjust position direction based on market conditions.
3. Comprehensive risk control: Features rapid response mechanism at trend turning points, enabling timely stop-loss and capture of new trend opportunities.
4. Strong parameter adaptability: Key parameters such as ATR period, Supertrend factor, and DEMA period can be optimized according to different market characteristics.

#### Strategy Risks
1. Poor performance in sideways markets: May generate frequent false breakout signals in markets without clear trends.
2. Lag risk: Using DEMA as a filter may cause slight delays in entry timing, affecting some profit potential.
3. Parameter sensitivity: Strategy effectiveness is sensitive to parameter settings, different market environments may require different parameter combinations.

#### Strategy Optimization Directions
1. Introduce volatility adaptive mechanism:
   - Dynamically adjust Supertrend factor values based on market volatility
   - Increase filtering threshold during high volatility periods and appropriately relax conditions during low volatility periods
2. Add market environment recognition module:
   - Add trend strength indicators to reduce trading frequency in sideways markets
   - Introduce volume indicators to assist in confirming breakout validity
3. Improve stop-loss mechanism:
   - Implement ATR-based dynamic stop-loss
   - Add trailing stop-loss function to protect profits

#### Summary
The strategy builds a robust trend-following system by cleverly combining Supertrend and DEMA indicators. Its advantages lie in high signal reliability and comprehensive risk control, but traders still need to optimize parameters based on specific market characteristics. Through the proposed optimization directions, the strategy's adaptability and stability can be further enhanced.




> Source (PineScript)

``` pinescript
/*backtest
start: 2025-02-16 00:00:00
end: 2025-02-23 00:00:00
period: 5m
basePeriod: 5m
exchanges: [{"eid":"Binance","currency":"SOL_USDT"}]
*/

//@version=6
strategy("Supertrend with DEMA Strategy (Reversal Enabled)", overlay=true)

// ===== Parameters for Supertrend =====
atrPeriod = input.int(10, "ATR Length", minval=1)
factor    = input.float(3.0, "Factor", minval=0.01, step=0.01)

// ===== Parameters for Allowing Trade Directions =====
allowLong  = input.bool(true,  "Allow LONG")
allowShort = input.bool(true,  "Allow SHORT")

// Supertrend Calculation
[supertrend, direction] = ta.supertrend(factor, atrPeriod)
// Set the value to na for the first bar to avoid false signals
supertrend := barstate.isfirst ? na : supertrend

// Plot Supertrend Lines
plot(direction < 0 ? supertrend : na, "Up Trend",   color=color.green, style=plot.style_linebr)
plot(direction < 0 ? na : supertrend, "Down Trend", color=color.red,   style=plot.style_linebr)

// ===== Parameters and Calculation for DEMA =====
demaLength = input.int(100, "DEMA Length", minval=1)
e1 = ta.ema(close, demaLength)
e2 = ta.ema(e1, demaLength)
dema = 2 * e1 - e2

// Plot DEMA
plot(dema, "DEMA", color=#43A047)

// ===== Signal Definitions =====
// Basic Supertrend Trend Change Signals
trendUp   = ta.crossover(close, supertrend)
trendDown = ta.crossunder(close, supertrend)

// Entry Signals considering DEMA
longSignal  = trendUp and (close > dema)
shortSignal = trendDown and (close < dema)

// ===== Entry/Exit Logic =====

// LONG Signal
if (longSignal)
    // If there is an open SHORT position – reverse it to LONG if allowed
    if (strategy.position_size < 0)
        if (allowLong)
            strategy.close("Short")
            strategy.entry("Long", strategy.long)
        else
            // If reversal to LONG is not allowed – just close SHORT
            strategy.close("Short")
    // If there is no position – open LONG if allowed
    else if (strategy.position_size == 0)
        if (allowLong)
            strategy.entry("Long", strategy.long)

// SHORT Signal
if (shortSignal)
    // If there is an open LONG position – reverse it to SHORT if allowed
    if (strategy.position_size > 0)
        if (allowShort)
            strategy.close("Long")
            strategy.entry("Short", strategy.short)
        else
            // If reversal to SHORT is not allowed – just close LONG
            strategy.close("Long")
    // If there is no position – open SHORT if allowed
    else if (strategy.position_size == 0)
        if (allowShort)
            strategy.entry("Short", strategy.short)

// ===== Additional Position Closure on Trend Change without Entry =====
// If Supertrend crosses (trend change) but DEMA conditions are not met,
// close the opposite position if open.
if (trendUp and not longSignal and strategy.position_size < 0)
    strategy.close("Short")

if (trendDown and not shortSignal and strategy.position_size > 0)
    strategy.close("Long")


```

> Detail

https://www.fmz.com/strategy/483510

> Last Modified

2025-02-27 16:49:07
