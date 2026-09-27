
> Name

Double-Seven-Strategy-Trend-Following-and-Mean-Reversion-Dual-Optimization-Trading-SystemDouble-Seven-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/17bacb16f999e2937a7.png)


#### Overview
This strategy is a quantitative trading system that combines trend following and mean reversion. It uses the 200-day moving average (MA200) to determine the major trend direction while utilizing 7-day price fluctuations to identify short-term oversold opportunities, achieving optimal entry timing in uptrends. This method ensures both directional accuracy and timely intervention during price adjustments, fully leveraging technical analysis in trading.

#### Strategy Principles
The core logic includes two dimensions: First, using MA200 to judge long-term trends, only considering positions when price is above MA200; Second, observing price performance over the last 7 trading days, entering long positions when a 7-day low occurs while still above MA200, and closing positions when price reaches a 7-day high. This design ensures both trend following and low-point entry, creating a systematic strategy that combines trend following and mean reversion concepts.

#### Strategy Advantages
1. Trend Confirmation Reliability: Using MA200 as a trend filter effectively avoids opening positions in downtrends.
2. Entry Timing Precision: Identifies oversold correction opportunities through 7-day lows, improving entry value.
3. High Systematization: Clear strategy rules without subjective judgment factors, easy to implement programmatically.
4. Comprehensive Risk Control: Reduces false signal probability through dual mechanisms of trend filtering and oversold judgment.
5. Wide Applicability: Simple and universal strategy logic applicable across multiple markets and instruments.

#### Strategy Risks
1. Trend Judgment Lag: MA200 as a long-term moving average has inherent lag, potentially causing misjudgments at trend turning points.
2. False Breakout Risk: Price breaking above 7-day highs may result in false breakouts, leading to premature exits.
3. Unsuitable for Ranging Markets: Frequent short-term highs and lows in sideways markets may generate excessive trading signals.
4. Market Environment Dependency: Strategy effectiveness heavily influenced by market trend characteristics, showing significant performance differences across market environments.

#### Strategy Optimization Directions
1. Dynamic Period Optimization: Adjust MA period and short-term observation period based on different market characteristics.
2. Multiple Confirmation Mechanisms: Add auxiliary indicators like volume and volatility to improve signal reliability.
3. Position Management Optimization: Introduce dynamic position management mechanisms to adjust holding ratios based on market volatility.
4. Stop Loss Enhancement: Design more flexible stop loss solutions, such as trailing stops or volatility-based stops.
5. Pattern Optimization: Design differentiated parameter combinations for different market environments.

#### Summary
The Double Seven Strategy is a quantitative trading system that organically combines trend following with mean reversion. Through the coordinated use of MA200 and 7-day price fluctuations, it ensures both directional accuracy and optimal entry timing. While certain limitations exist, the strategy holds practical value and expansion potential through reasonable optimization and risk control. Traders are advised to optimize the strategy based on market characteristics and personal needs in practical applications to enhance stability and profitability.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-27 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © EdgeTools

//@version=5
strategy("Larry Connors' Double Seven Strategy", overlay=true)

// 200-day moving average
ma200 = ta.sma(close, 200)

// Conditions for Double Seven Strategy
priceAboveMa200 = close > ma200

// Find the lowest close over the last 7 days
lowestClose7Days = ta.lowest(close, 7)

// Find the highest close over the last 7 days
highestClose7Days = ta.highest(close, 7)

// Entry and exit rules
longCondition = priceAboveMa200 and close <= lowestClose7Days
exitCondition = close >= highestClose7Days

// Enter long position
if (longCondition)
    strategy.entry("Long", strategy.long)

// Exit long position
if (exitCondition)
    strategy.close("Long")
    
// Plot moving averages
plot(ma200, "200-day MA", color=color.blue)

```

> Detail

https://www.fmz.com/strategy/473246

> Last Modified

2024-11-28 15:41:34
