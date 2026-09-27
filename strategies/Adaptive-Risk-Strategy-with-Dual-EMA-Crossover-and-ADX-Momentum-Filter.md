
> Name

Adaptive-Risk-Strategy-with-Dual-EMA-Crossover-and-ADX-Momentum-Filter

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/146d660ebc6cba62f48.png)


#### Overview
This strategy is a trading system that combines dual EMA trend identification, ADX momentum filtering, and adaptive risk management. It uses 50 and 200-period Exponential Moving Averages (EMA) as the foundation for trend determination, confirms momentum through ADX and DMI indicators, and dynamically adjusts stop-loss and profit targets based on ATR.

#### Strategy Principles
The core logic consists of three parts:
1. Trend Identification: Uses the relative position of 50 and 200-period EMAs to determine the current trend direction, with EMA50 above EMA200 indicating an uptrend and vice versa.
2. Momentum Confirmation: Utilizes ADX and DMI indicators to confirm trend strength, requiring ADX above a set threshold (default 25) and DI+ greater than DI- to confirm uptrend, and vice versa for downtrend.
3. Entry Timing: After trend confirmation, price crossovers with EMA50 serve as specific entry signals, with upward crosses for long positions and downward crosses for short positions.

#### Strategy Advantages
1. Multiple Confirmation Mechanism: Effectively reduces false signals through multiple confirmations of trend and momentum.
2. Adaptive Risk Management: Uses ATR to dynamically adjust stop-loss positions, making risk management more aligned with market volatility.
3. Risk-Reward Optimization: Ensures reasonable return expectations for each trade through preset risk-reward ratios.
4. Visual Support: Provides comprehensive graphical display including trend lines, stop-loss/profit levels, and trade signal markers.

#### Strategy Risks
1. Trend Reversal Delay: May experience some delay in trend reversals due to the use of longer-period moving averages.
2. Unsuitable for Ranging Markets: May generate frequent false signals in sideways, ranging markets.
3. Parameter Sensitivity: Strategy effectiveness is sensitive to parameter settings, which may need adjustment in different market environments.

#### Strategy Optimization Directions
1. Market Environment Adaptation: Can add market environment assessment logic to dynamically adjust parameters in different volatility conditions.
2. Enhanced Signal Filtering: Can introduce volume or other technical indicators as auxiliary filtering conditions.
3. Stop-Loss Optimization: Can consider implementing trailing stops or composite stop-loss strategies to improve risk management flexibility.
4. Scaled Position Building: Can implement scaled entry and exit mechanisms to optimize money management.

#### Summary
This is a structurally complete and logically clear trend-following strategy that achieves reliable trade signal generation and risk control through the coordinated use of multiple technical indicators. The strategy offers strong extensibility with significant optimization potential. Through appropriate parameter adjustments and optimization measures, it can adapt to different market environments.




> Source (PineScript)

``` pinescript
/*backtest
start: 2025-02-10 00:00:00
end: 2025-02-17 00:00:00
period: 3m
basePeriod: 3m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("XAUUSD 15m Trend Strategy", overlay=true, margin_long=100, margin_short=100)

// Input parameters
emaFast = input.int(50, "Fast EMA Period", minval=1)
emaSlow = input.int(200, "Slow EMA Period", minval=1)
adxThreshold = input.int(25, "ADX Threshold", minval=1)
lookback = input.int(5, "Swing Lookback Period", minval=1)
riskReward = input.float(1.5, "Risk Reward Ratio", minval=1.0)

// Calculate indicators
ema50 = ta.ema(close, emaFast)
ema200 = ta.ema(close, emaSlow)
[diPlus, diMinus, adx] = ta.dmi(14, 14)
atr = ta.atr(14)

// Trend conditions
uptrend = ema50 > ema200 and adx >= adxThreshold and diPlus > diMinus
downtrend = ema50 < ema200 and adx >= adxThreshold and diMinus > diPlus

// Entry conditions
longCondition = uptrend and ta.crossover(close, ema50)
shortCondition = downtrend and ta.crossunder(close, ema50)

// Calculate risk levels
longStop = ta.lowest(low, lookback) - atr * 0.5
longProfit = close + (close - longStop) * riskReward
shortStop = ta.highest(high, lookback) + atr * 0.5
shortProfit = close - (shortStop - close) * riskReward

// Execute trades
if (longCondition)
    strategy.entry("Long", strategy.long)
    strategy.exit("Exit Long", "Long", stop=longStop, limit=longProfit)

if (shortCondition)
    strategy.entry("Short", strategy.short)
    strategy.exit("Exit Short", "Short", stop=shortStop, limit=shortProfit)

// Plotting
plot(ema50, "EMA 50", color=color.blue)
plot(ema200, "EMA 200", color=color.orange)
plot(strategy.position_size > 0 ? longStop : na, "Long Stop", color=color.red, style=plot.style_linebr)
plot(strategy.position_size > 0 ? longProfit : na, "Long Target", color=color.green, style=plot.style_linebr)
plot(strategy.position_size < 0 ? shortStop : na, "Short Stop", color=color.red, style=plot.style_linebr)
plot(strategy.position_size < 0 ? shortProfit : na, "Short Target", color=color.green, style=plot.style_linebr)

// Signal markers
plotshape(longCondition, "Buy Signal", shape.triangleup, location.belowbar, color=color.green, size=size.small)
plotshape(shortCondition, "Sell Signal", shape.triangledown, location.abovebar, color=color.red, size=size.small)
```

> Detail

https://www.fmz.com/strategy/482489

> Last Modified

2025-02-18 16:21:02
