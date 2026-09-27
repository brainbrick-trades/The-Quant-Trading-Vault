
> Name

Trend-Following-Gap-Breakout-Trading-System-with-SMA-Filter

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/c86875ce2045f72938.png)


#### Overview
This is a trend-following trading system based on price gaps and moving average filtering. The strategy captures trending opportunities by identifying statistically significant price gaps combined with SMA trend filters, executing trades when clear market trends emerge. The core concept is to capitalize on trend continuation opportunities created by supply-demand imbalances manifesting as price gaps.

#### Strategy Principles
The strategy operates on several key elements:
1. Gap Identification - The system identifies gaps by calculating the percentage difference between opening price and previous closing price, with a minimum gap threshold to filter out minor fluctuations.
2. Directional Selection - Offers multiple gap trading modes (long up gaps, short down gaps, etc.), allowing users to adapt to market conditions.
3. SMA Trend Filtering - Uses Simple Moving Average to determine overall trend, only entering positions when price aligns with trend direction.
4. Position Management - Employs preset holding periods for position management and risk control.

#### Strategy Advantages
1. Clear Signals - Gap signals are visually distinct and easy to identify and execute.
2. Controlled Risk - Minimum gap thresholds and fixed holding periods effectively manage risk.
3. High Flexibility - Different gap trading directions can be selected based on market conditions.
4. Trend Confirmation - SMA filter provides additional trend confirmation, improving success rate.
5. High Automation - Clear strategy logic facilitates automated trading implementation.

#### Strategy Risks
1. False Breakout Risk - Gaps may quickly fill, leading to false signals.
2. Slippage Risk - Opening gap trades may face significant slippage.
3. Trend Reversal Risk - Fixed holding periods might miss trend reversals.
4. Market Environment Dependency - Fewer effective signals in low-volatility markets.

#### Strategy Optimization Directions
1. Dynamic Holding Period - Adjust holding time based on market volatility.
2. Multiple Confirmations - Incorporate volume and volatility indicators for signal confirmation.
3. Stop Loss Optimization - Add trailing stops or volatility-based stops.
4. Signal Grading - Design tiered position sizing based on gap magnitude.
5. Market Selection - Develop market condition identification mechanisms for selective trading.

#### Summary
This strategy combines price gaps and moving average trend filtering to create a trading system with clear logic and controlled risk. Through appropriate parameter settings and continuous optimization, the strategy can achieve stable returns in trending markets. Traders are advised to conduct thorough historical testing before live implementation and optimize based on specific market characteristics.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-27 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Simplified Gap Strategy with SMA Filter", overlay=true)

// Input fields for user control
long_gap_threshold = input.float(0.1, title="Gap Threshold (%)", minval=0.01, step=0.01)  // Minimum percentage for gaps
hold_duration = input.int(10, title="Hold Duration (bars)", minval=1)  // Duration to hold the position
gap_trade_option = input.string("Long Up Gap", title="Select Trade Option", options=["Long Up Gap", "Short Down Gap", "Short Up Gap", "Long Down Gap"])  // Combined option
use_sma_filter = input.bool(false, title="Use SMA Filter")  // Checkbox to activate SMA filter
sma_length = input.int(200, title="SMA Length", minval=1)  // Length of the SMA

// RGB color definitions for background
color_up_gap = color.new(color.green, 50)    // Green background for up gaps
color_down_gap = color.new(color.red, 50)    // Red background for down gaps

// Gap size calculation in percentage terms
gap_size = (open - close[1]) / close[1] * 100  // Gap size in percentage

// Calculate gaps based on threshold input
up_gap = open > close[1] and gap_size >= long_gap_threshold  // Long gap condition
down_gap = open < close[1] and math.abs(gap_size) >= long_gap_threshold  // Short gap condition

// Calculate the SMA
sma_value = ta.sma(close, sma_length)

// Define the trading logic based on selected option and SMA filter
if (gap_trade_option == "Long Up Gap" and up_gap and (not use_sma_filter or close > sma_value))
    strategy.entry("Long", strategy.long)
if (gap_trade_option == "Short Down Gap" and down_gap and (not use_sma_filter or close < sma_value))
    strategy.entry("Short", strategy.short)
if (gap_trade_option == "Short Up Gap" and up_gap and (not use_sma_filter or close < sma_value))
    strategy.entry("Short", strategy.short)
if (gap_trade_option == "Long Down Gap" and down_gap and (not use_sma_filter or close > sma_value))
    strategy.entry("Long", strategy.long)

// Exit position after the hold duration
if (strategy.opentrades > 0)
    if (bar_index - strategy.opentrades.entry_bar_index(0) >= hold_duration)
        strategy.close("Long")
        strategy.close("Short")

// Background coloring to highlight gaps on the chart
bgcolor((gap_trade_option == "Long Up Gap" and up_gap) ? color_up_gap : na, title="Up Gap Background")
bgcolor((gap_trade_option == "Short Down Gap" and down_gap) ? color_down_gap : na, title="Down Gap Background")
bgcolor((gap_trade_option == "Short Up Gap" and up_gap) ? color_down_gap : na, title="Short Up Gap Background")
bgcolor((gap_trade_option == "Long Down Gap" and down_gap) ? color_up_gap : na, title="Long Down Gap Background")

// Plot the SMA for visualization
plot(use_sma_filter ? sma_value : na, color=color.white, title="SMA", linewidth=1)

```

> Detail

https://www.fmz.com/strategy/473356

> Last Modified

2024-11-29 15:07:43
