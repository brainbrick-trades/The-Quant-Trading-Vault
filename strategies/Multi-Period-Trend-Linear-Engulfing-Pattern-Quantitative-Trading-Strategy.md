
> Name

Multi-Period-Trend-Linear-Engulfing-Pattern-Quantitative-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/13bc18b6fea0cb54852.png)


#### Overview
This is a quantitative trading strategy based on the engulfing pattern, which identifies and trades on multi-period trend linear engulfing patterns in the market. The core of the strategy is to capture price reversal signals, combined with holding periods and risk control to achieve stable trading results. The strategy is applicable to all markets and time periods, demonstrating strong universality.

#### Strategy Principle
The strategy trades based on the engulfing pattern in candlestick formations. A buy signal is generated in a downtrend when a bullish engulfing pattern appears (a smaller bearish candle followed by a larger bullish candle that completely engulfs the previous one). A sell signal is generated in an uptrend when a bearish engulfing pattern appears (a smaller bullish candle followed by a larger bearish candle that completely engulfs the previous one). The strategy uses parameterized holding periods, automatically closing positions after the specified period to avoid risks associated with excessive holding.

#### Strategy Advantages
1. Clear Signals: Engulfing patterns have distinct visual characteristics, leading to high accuracy in signal identification
2. Wide Applicability: Can be applied to all markets and timeframes, offering broad practical value
3. Controlled Risk: Effectively manages holding risk through fixed holding periods
4. Flexible Parameters: Trading direction and holding periods can be adjusted according to different market characteristics
5. Strong Visualization: Pattern occurrences are marked with background colors, facilitating analysis and backtesting

#### Strategy Risks
1. False Breakout Risk: Engulfing patterns may produce false breakouts, requiring confirmation from other indicators
2. Market Environment Dependency: Performance varies in different market environments, requiring timely parameter adjustments
3. Fixed Holding Period: Fixed holding periods may miss larger profits or incur larger losses
4. Signal Latency: Signals can only be confirmed after candle closing, potentially missing optimal entry points

#### Strategy Optimization Directions
1. Trend Filtering: Incorporate trend indicators like moving averages to filter counter-trend signals
2. Dynamic Holding Periods: Adjust holding periods based on market volatility
3. Volume Confirmation: Add volume indicators to verify pattern validity
4. Improved Stop Loss: Introduce dynamic stop-loss mechanisms to enhance risk control
5. Multiple Timeframe Resonance: Combine signals from multiple timeframes to improve trading success rate

#### Summary
The strategy captures engulfing pattern opportunities through a systematic approach, achieving risk-controlled trading through parameterized position management. While the strategy demonstrates strong practicality and adaptability, traders still need to optimize and adjust according to specific market characteristics. It is recommended to combine other technical indicators and risk control measures to improve strategy stability and reliability.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-12-06 00:00:00
end: 2025-01-04 08:00:00
period: 2h
basePeriod: 2h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("Engulfing Candlestick Strategy", overlay=true)

// Input parameters
bull_color = input.color(color.new(color.green, 0), title="Bullish Engulfing Highlight")
bear_color = input.color(color.new(color.red, 0), title="Bearish Engulfing Highlight")
hold_periods = input.int(17, title="Hold Periods", minval=1)  // How many bars to hold the position

// Input for selecting the pattern (Bullish or Bearish Engulfing)
pattern_type = input.string("Bullish Engulfing", title="Engulfing Pattern", options=["Bullish Engulfing", "Bearish Engulfing"])

// Input for selecting the trade type (Long or Short)
trade_type = input.string("Long", title="Trade Type", options=["Long", "Short"])

// Conditions for Bullish Engulfing
bullish_engulfing = close > open and open < close[1] and close > open[1] and open[1] > close[1]

// Conditions for Bearish Engulfing
bearish_engulfing = close < open and open > close[1] and close < open[1] and open[1] < close[1]

// Declare the entry condition variable
var bool entry_condition = false  // Set initial value to 'false'

// Entry logic based on selected pattern and trade type
if pattern_type == "Bullish Engulfing"
    entry_condition := bullish_engulfing
else
    entry_condition := bearish_engulfing

// Execute the entry based on the selected trade type
if entry_condition
    if trade_type == "Long"
        strategy.entry("Long", strategy.long)
    else
        strategy.entry("Short", strategy.short)

// Close position after specified number of bars
if strategy.position_size != 0 and bar_index - strategy.opentrades.entry_bar_index(0) >= hold_periods
    strategy.close("Long")
    strategy.close("Short")

// Highlight Bullish Engulfing Candles (Background Color)
bgcolor(bullish_engulfing and pattern_type == "Bullish Engulfing" ? color.new(bull_color, 80) : na, title="Bullish Engulfing Background")
// Highlight Bearish Engulfing Candles (Background Color)
bgcolor(bearish_engulfing and pattern_type == "Bearish Engulfing" ? color.new(bear_color, 80) : na, title="Bearish Engulfing Background")

```

> Detail

https://www.fmz.com/strategy/477529

> Last Modified

2025-01-06 11:42:37
