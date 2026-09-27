
> Name

Multi-Moving-Average-Trend-Reversal-Quantitative-Strategy-Combined-EMA-and-SMA-Signal-System

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d90097b8034e3cc13bb3.png)
![IMG](https://www.fmz.com/upload/asset/2d84729cce9dce505fd68.png)



#### Overview
This strategy is a trend reversal trading system based on multiple moving average combinations, incorporating 9-period, 21-period, 50-period, and 200-period moving averages to identify market trend turning points through crossover signals. The strategy integrates the advantages of both short-term and long-term moving averages, enabling timely capture of market momentum changes while effectively filtering false signals.

#### Strategy Principles
The core logic is built on a multiple timeframe moving average crossover system. Specifically:
1. Uses 50-period and 200-period Simple Moving Averages (SMA) as primary trend indicators
2. Employs 9-period and 21-period Exponential Moving Averages (EMA) for short-term signal confirmation
3. Optimizes signal quality through lookback period and threshold parameters
4. Incorporates support and resistance level identification using pivot point algorithms
The system generates buy signals when shorter-term averages cross above longer-term ones, and sell signals when the opposite occurs.

#### Strategy Advantages
1. Signal Reliability: Multiple moving average confirmations significantly reduce false signal risks
2. Timely Trend Capture: Short-term averages enable quick response to market changes
3. Comprehensive Risk Control: Support and resistance identification aids in stop-loss and take-profit placement
4. Parameter Flexibility: Adjustable lookback and threshold parameters for different market conditions
5. Intuitive Visualization: Clear graphical interface facilitates trading decisions

#### Strategy Risks
1. Choppy Market Risk: May generate frequent false signals during consolidation phases
2. Lag Risk: Moving averages are inherently lagging indicators, potentially missing optimal entry points
3. Parameter Sensitivity: Different parameter combinations may lead to varying strategy performance
4. Market Environment Dependency: Strategy performs better in trending markets, may underperform during high volatility periods

#### Strategy Optimization Directions
1. Volume Integration: Consider incorporating volume as a signal confirmation indicator
2. Signal Filtering Enhancement: Design stricter signal confirmation mechanisms, such as requiring signal persistence
3. Dynamic Parameter Adjustment: Develop adaptive parameter systems that automatically adjust based on market conditions
4. Risk Control Improvement: Add dynamic stop-loss mechanisms to protect profits
5. Market Context Integration: Incorporate volatility indicators to adapt parameters to different market environments

#### Summary
The strategy effectively identifies market trend turning points through the synergy of multiple moving average systems. The design emphasizes practicality and operability, with flexible parameter adjustment capabilities for different market conditions. While certain limitations exist, continuous optimization and refinement show promising potential for overall strategy performance.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-11-11 00:00:00
end: 2025-02-18 08:00:00
period: 6h
basePeriod: 6h
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=6
//indicator("9/21 EMA Support & Resistance By DSW", overlay=true)
//indicator("Thick and Colorful Line", overlay=true)


// Define the price data
price = close

//@version=6
strategy("9/21/50/200 By DSW Trend Reversal for Options", overlay=true)

// Define the moving averages
short_term_sma = ta.sma(close, 50)  // 50-period SMA
long_term_sma = ta.sma(close, 200)  // 200-period SMA

// Plot the moving averages
plot(short_term_sma, color=color.blue, linewidth=2, title="50-period SMA")
plot(long_term_sma, color=color.red, linewidth=2, title="200-period SMA")

// Detect crossovers
bullish_reversal = ta.crossover(short_term_sma, long_term_sma)  // Short-term SMA crosses above long-term SMA
bearish_reversal = ta.crossunder(short_term_sma, long_term_sma)  // Short-term SMA crosses below long-term SMA

// Plot signals on the chart
plotshape(bullish_reversal, title="Bullish Reversal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
plotshape(bearish_reversal, title="Bearish Reversal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

// Strategy to buy or sell based on the crossovers
if bullish_reversal
    strategy.entry("Buy Option", strategy.long)  // Buy Call for a bullish reversal

if bearish_reversal
    strategy.entry("Sell Option", strategy.short)  // Buy Put for a bearish reversal


// Define the color and line thickness
line_color = color.new(color.blue, 0)  // You can change this to any color you like
line_width = 3  // This controls the thickness of the line

// Plot the line
plot(price, color=line_color, linewidth=line_width)

// Input parameters
lookback = input.int(10, "Lookback Period")
threshold = input.float(0.5, "Threshold", minval=0, maxval=100, step=0.1)

// Calculate EMAs
ema9 = ta.ema(close, 9)
ema21 = ta.ema(close, 21)

// Plot EMAs
plot(ema9, color=color.blue, title="9 EMA")
plot(ema21, color=color.red, title="21 EMA")

// Function to find pivot highs and lows
pivotHigh = ta.pivothigh(high, lookback, lookback)
pivotLow = ta.pivotlow(low, lookback, lookback)

// EMA Crossover
crossover = ta.crossover(ema9, ema21)
crossunder = ta.crossunder(ema9, ema21)

// Plot crossover signals
plotshape(crossover, title="Bullish Crossover", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
// Plot bearish crossover signals
plotshape(crossunder, title="Bearish Crossover", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)


// Alert conditions
if crossover
    alert("Bullish EMA Crossover", alert.freq_once_per_bar)

if crossunder
    alert("Bearish EMA Crossover", alert.freq_once_per_bar)





```

> Detail

https://www.fmz.com/strategy/482788

> Last Modified

2025-02-27 17:49:01
