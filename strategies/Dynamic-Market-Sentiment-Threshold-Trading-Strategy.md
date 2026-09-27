
> Name

Dynamic-Market-Sentiment-Threshold-Trading-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d895bc5d1e39c19bb323.png)
![IMG](https://www.fmz.com/upload/asset/2d8312bddf249652b2050.png)



#### Overview
The Dynamic Market Sentiment Threshold Trading Strategy is an automated trading system that capitalizes on market fear and greed emotions to make trading decisions. The strategy utilizes dynamic changes in the Fear and Greed Index, entering positions during extreme fear and exiting during extreme greed, aiming to capture trading opportunities through market psychology.

#### Strategy Principles
The core mechanism monitors dynamic changes in the Fear and Greed Index to identify market sentiment turning points. Specifically:
1. Strategy sets two key thresholds: fear threshold (25) and greed threshold (75)
2. When the index transitions into the greed zone (>75), the system automatically generates a buy signal
3. When the index transitions into the fear zone (<25), the system automatically generates a sell signal
4. Trade volume is fixed at 100 units for risk control purposes
5. Strategy stores historical data in arrays and uses modulo operation to locate current period index values

#### Strategy Advantages
1. High Automation: Strategy executes trades automatically, reducing emotional interference
2. Psychological Quantification: Converts market sentiment into quantifiable trading indicators
3. Robust Risk Control: Manages risk through fixed trading volume and clear entry/exit mechanisms
4. Strong Visualization: Provides clear graphical interface and trade signal markers
5. High Adaptability: Applicable across multiple markets including stocks, cryptocurrencies, and forex

#### Strategy Risks
1. Lag Risk: Sentiment indicators may have inherent lag, affecting signal timeliness
2. False Breakout Risk: Short-term sentiment fluctuations may trigger false trading signals
3. Market Environment Dependency: May generate frequent trades in highly volatile markets
4. Parameter Sensitivity: Strategy performance heavily depends on threshold settings
5. Data Dependency: Strategy effectiveness relies on accuracy and timeliness of sentiment data

#### Strategy Optimization Directions
1. Implement Multiple Confirmation Mechanisms: Combine with other technical indicators like RSI or MACD
2. Dynamic Threshold Adjustment: Automatically adjust fear and greed thresholds based on market volatility
3. Enhanced Position Management: Introduce dynamic position sizing to replace fixed trading volume
4. Optimize Signal Filtering: Add signal filtering mechanisms to reduce false breakout trades
5. Improve Backtesting System: Add more backtesting metrics to evaluate strategy stability

#### Summary
This innovative trading strategy based on market psychology captures trading opportunities by quantifying market sentiment. While there are potential risks, continuous optimization and refinement suggest promising potential for stable performance in actual trading. Traders are advised to conduct thorough backtesting and parameter optimization before live implementation.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-22 00:00:00
end: 2025-02-19 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=6
strategy("Fear and Greed Trading Strategy", overlay=false)

// Manually input Fear and Greed Index data (example values for demo)
fear_and_greed = array.from(40, 35, 50, 60, 45, 80, 20, 10)  // Replace with your data points

// Get the current bar index within the array bounds
current_index = bar_index % array.size(fear_and_greed)

// Extract data for the current bar
fgi_value = array.get(fear_and_greed, current_index)

// Initialize variables for previous index and value
var float fgi_prev = na
if (current_index > 0)
    fgi_prev := array.get(fear_and_greed, current_index - 1)

// Set thresholds
fear_threshold = 25
greed_threshold = 75

// Determine current and previous states
state_prev = na(fgi_prev) ? "neutral" : fgi_prev < fear_threshold ? "fear" : fgi_prev > greed_threshold ? "greed" : "neutral"
state_curr = fgi_value < fear_threshold ? "fear" : fgi_value > greed_threshold ? "greed" : "neutral"

// Buy and sell conditions
buy_condition = state_prev != "greed" and state_curr == "greed"
sell_condition = state_prev != "fear" and state_curr == "fear"

// Execute trades
if (buy_condition)
    strategy.entry("Buy", strategy.long, qty=100)
if (sell_condition)
    strategy.close("Buy")

// Plotting for visualization
plot(fgi_value, color=color.new(color.white, 0), linewidth=2, title="Fear and Greed Index")
hline(fear_threshold, "Fear Threshold", color=color.red, linestyle=hline.style_dashed)
hline(greed_threshold, "Greed Threshold", color=color.green, linestyle=hline.style_dashed)

// Add labels for actions
if (buy_condition)
    label.new(bar_index, fgi_value, "Buy", style=label.style_label_down, color=color.green, textcolor=color.white)
if (sell_condition)
    label.new(bar_index, fgi_value, "Sell", style=label.style_label_up, color=color.red, textcolor=color.white)

```

> Detail

https://www.fmz.com/strategy/483022

> Last Modified

2025-02-21 09:30:29
