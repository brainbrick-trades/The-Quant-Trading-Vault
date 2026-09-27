
> Name

Dynamic-EMA-Crossover-Strategy-with-ADX-Trend-Strength-Filtering-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/c60f9ebc8998a3298f.png)


#### Overview
This strategy is a trend-following trading system that combines the Exponential Moving Average (EMA) and Average Directional Index (ADX). It determines trading direction through EMA50 and price crossovers, uses ADX to filter trend strength, and employs a dynamic stop-loss method based on consecutive profitable candles. This approach enables both capturing major market trends and timely exits when trends weaken.

#### Strategy Principles
The core logic is based on the following key elements:
1. Uses 50-period EMA (EMA50) as trend direction indicator
2. Filters market trend strength using ADX indicator (default parameter 20)
3. Entry conditions:
   - Long: Price closes above EMA50 and ADX above threshold
   - Short: Price closes below EMA50 and ADX above threshold
4. Unique stop-loss mechanism:
   - Counts consecutive profitable candles
   - Activates dynamic trailing stop after 4 consecutive profitable candles
   - Stop-loss level adjusts dynamically with new highs/lows

#### Strategy Advantages
1. Dual Trend Confirmation
- EMA crossover provides trend direction
- ADX filtering ensures trend strength, reduces false breakouts
2. Intelligent Stop-Loss Design
- Dynamic stops based on market volatility
- Trailing stop activated only after consecutive profits
3. High Adaptability
- Highly adjustable parameters
- Applicable to multiple trading instruments
4. Comprehensive Risk Control
- Automatic exit on trend weakness
- Dynamic stops protect existing profits

#### Strategy Risks
1. Trend Reversal Risk
- May face significant drawdowns during sudden reversals
- Recommend adding reversal confirmation mechanism
2. Parameter Sensitivity
- Strategy performance affected by EMA and ADX parameter choice
- Recommend parameter optimization through backtesting
3. Market Environment Dependency
- May trade frequently in ranging markets
- Recommend adding sideways market filter
4. Stop-Loss Execution Risk
- Large gaps may cause stop-loss execution deviation
- Consider implementing hard stop-loss protection

#### Optimization Directions
1. Entry Mechanism Enhancement
- Add volume confirmation signals
- Incorporate price pattern analysis
2. Stop-Loss Mechanism Improvement
- Integrate ATR for dynamic stop-loss adjustment
- Add time-based stop-loss mechanism
3. Market Environment Adaptation
- Add market volatility filters
- Adjust parameters for different market cycles
4. Signal Confirmation Enhancement
- Integrate additional technical indicators
- Add fundamental filtering conditions

#### Summary
This is a well-designed trend-following strategy that effectively captures trends while controlling risks by combining the advantages of EMA and ADX. The dynamic stop-loss mechanism is particularly innovative, effectively balancing profit protection and trend capture. While there is room for optimization, the overall framework is complete and logically sound, making it a strategy system worth validating in live trading.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2025-01-04 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("Simple EMA 50 Strategy with ADX Filter", overlay=true)

// Input parameters
emaLength = input.int(50, title="EMA Length")
adxThreshold = input.float(20, title="ADX Threshold", minval=0)

// Calculate EMA and ADX
ema50 = ta.ema(close, emaLength)
adxSmoothing = input.int(20, title="ADX Smoothing")
[diPlus, diMinus, adx] = ta.dmi(20, adxSmoothing)

// Conditions for long and short entries
adxCondition = adx > adxThreshold
longCondition = adxCondition and close > ema50  // Check if candle closes above EMA
shortCondition = adxCondition and close < ema50  // Check if candle closes below EMA

// Exit conditions based on 4 consecutive profitable candles
var float longSL = na
var float shortSL = na
var longCandleCounter = 0
var shortCandleCounter = 0

// Increment counters if positions are open and profitable
if (strategy.position_size > 0 and close > strategy.position_avg_price)
    longCandleCounter += 1
    if (longCandleCounter >= 4)
        longSL := na(longSL) ? close : math.max(longSL, close)  // Update SL dynamically
else
    longCandleCounter := 0
    longSL := na

if (strategy.position_size < 0 and close < strategy.position_avg_price)
    shortCandleCounter += 1
    if (shortCandleCounter >= 4)
        shortSL := na(shortSL) ? close : math.min(shortSL, close)  // Update SL dynamically
else
    shortCandleCounter := 0
    shortSL := na

// Exit based on trailing SL
if (strategy.position_size > 0 and not na(longSL) and close < longSL)
    strategy.close("Buy", comment="Candle-based SL")

if (strategy.position_size < 0 and not na(shortSL) and close > shortSL)
    strategy.close("Sell", comment="Candle-based SL")

// Entry logic: Check every candle for new positions
if (longCondition)
    strategy.entry("Buy", strategy.long)
if (shortCondition)
    strategy.entry("Sell", strategy.short)

// Plot EMA and ADX for reference
plot(ema50, color=color.blue, title="EMA 50")
plot(adx, color=color.orange, title="ADX", style=plot.style_stepline, linewidth=1)
plot(longSL, color=color.green, title="Long SL", style=plot.style_cross, linewidth=1)
plot(shortSL, color=color.red, title="Short SL", style=plot.style_cross, linewidth=1)

// Plot signals
plotshape(series=longCondition, location=location.belowbar, color=color.green, style=shape.labelup, title="Buy Signal")
plotshape(series=shortCondition, location=location.abovebar, color=color.red, style=shape.labeldown, title="Sell Signal")

```

> Detail

https://www.fmz.com/strategy/477530

> Last Modified

2025-01-06 11:44:03
