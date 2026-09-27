
> Name

Moving-Average-Crossover-and-Candlestick-Pattern-Smart-Timing-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/179abc2f8e4f2a999a6.png)


#### Overview
This strategy is an intelligent trading system that combines classical technical analysis tools including moving average crossovers and candlestick pattern recognition. The strategy identifies potential market turning points by analyzing the relationship between candlestick shadows and bodies, while incorporating dual moving average crossover signals. The system not only focuses on price trends but also calculates average ranges to dynamically adjust trading parameters for improved adaptability.

#### Strategy Principles
The core logic consists of two main components:
1. The candlestick pattern recognition module identifies potential reversal signals by calculating the ratio between shadows and bodies. The system includes adjustable parameters for shadow multiplier (wickMultiplier) and body percentage (bodyPercentage) to optimize signal quality. When a candlestick displays qualifying long upper or lower shadows, the system generates corresponding long or short signals.

2. The dual moving average crossover system utilizes 14-period and 28-period Simple Moving Averages (SMA) as trend indicators. Long signals are generated when the short-term MA crosses above the long-term MA, while short signals occur when the short-term MA crosses below the long-term MA.

#### Strategy Advantages
1. Strict Signal Filtering: Effectively filters out low-quality signals through shadow multiplier and body percentage thresholds
2. Strong Parameter Adaptability: Provides flexible parameter adjustment interfaces for optimizing strategy performance across different market conditions
3. Combines Trend Following and Reversal Signals: Captures both trending markets and important reversal opportunities
4. Comprehensive Risk Control: Utilizes 50-period average range calculations to dynamically adjust trading parameters for enhanced stability

#### Strategy Risks
1. Parameter Sensitivity: Different parameter settings may lead to significant performance variations, requiring thorough optimization
2. Market Environment Dependency: May generate excessive false signals in ranging markets, increasing trading costs
3. Slippage Impact: Potential for significant slippage in markets with poor liquidity
4. Signal Delay: Moving average systems have inherent lag, possibly missing optimal entry points

#### Strategy Optimization Directions
1. Incorporate Volume Indicators: Analyze volume changes to confirm reversal signal validity
2. Enhance Dynamic Parameter Adjustment: Automatically adjust shadow multiplier and body percentage parameters based on market volatility
3. Add Trend Strength Filtering: Integrate RSI or ADX indicators to filter signals in weak market conditions
4. Improve Stop-Loss Mechanism: Design dynamic stop-loss positions based on ATR indicator for more precise risk control

#### Summary
This strategy constructs a relatively complete trading decision framework by combining candlestick pattern recognition with moving average crossover systems. Its strengths lie in strict signal filtering mechanisms and flexible parameter adjustment capabilities, while attention must be paid to parameter optimization and market environment adaptability. Through continuous optimization and refinement, the strategy shows potential for maintaining stable performance across various market conditions.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-10-28 00:00:00
end: 2024-11-27 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5 indicator("Wick Reversal Setup", overlay=true)

// Input parameters
wickMultiplier = input.float(3.5, title="Wick Multiplier", minval=0.5, maxval=20)
bodyPercentage = input.float(0.25, title="Body Percentage", minval=0.1, maxval=1.0)

// Calculate the average range over 50 periods
avgRange = ta.sma(high - low, 50)

// Define the lengths of wicks and bodies
bodyLength = math.abs(close - open)
upperWickLength = high - math.max(close, open)
lowerWickLength = math.min(close, open) - low
totalRange = high - low

// Long signal conditions
longSignal = (close > open and upperWickLength >= bodyLength * wickMultiplier and upperWickLength <= totalRange * bodyPercentage) or
             (close < open and lowerWickLength >= bodyLength * wickMultiplier and upperWickLength <= totalRange * bodyPercentage) or
             (close == open and close != high and upperWickLength >= bodyLength * wickMultiplier and upperWickLength <= totalRange * bodyPercentage) or
             (open == high and close == high and totalRange >= avgRange)

// Short signal conditions
shortSignal = (close < open and (high - open) >= bodyLength * wickMultiplier and lowerWickLength <= totalRange * bodyPercentage) or
              (close > open and (high - close) >= bodyLength * wickMultiplier and lowerWickLength <= totalRange * bodyPercentage) or
              (close == open and close != low and lowerWickLength >= bodyLength * wickMultiplier and lowerWickLength <= totalRange * bodyPercentage) or
              (open == low and close == low and totalRange >= avgRange)

// Plot signals
plotshape(series=longSignal, location=location.belowbar, color=color.green, style=shape.labelup, text="Long")
plotshape(series=shortSignal, location=location.abovebar, color=color.red, style=shape.labeldown, text="Short")
// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Sahaj_Beriwal

//@version=5
strategy("My strategy", overlay=true, margin_long=100, margin_short=100)

longCondition = ta.crossover(ta.sma(close, 14), ta.sma(close, 28))
if (longCondition)
    strategy.entry("L", strategy.long)

shortCondition = ta.crossunder(ta.sma(close, 14), ta.sma(close, 28))
if (shortCondition)
    strategy.entry("S", strategy.short)

```

> Detail

https://www.fmz.com/strategy/473269

> Last Modified

2024-11-28 17:18:29
