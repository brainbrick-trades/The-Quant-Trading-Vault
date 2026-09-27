
> Name

Dynamic-Trend-Following-Dual-Moving-Average-Channel-Strategy-with-Risk-Management-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/17851fbc890c2887eff.png)


#### Overview
This strategy is a dynamic trend following system based on dual moving average channels, combined with risk management mechanisms. It utilizes two Simple Moving Averages (SMA) to construct a trading channel, with the upper band calculated using the high price and the lower band using the low price. The system generates entry signals when the closing price remains above the upper band for five consecutive bars, and exit signals when either the price falls below the lower band for five consecutive bars or retraces 25% from the highest point, achieving dynamic trend tracking and risk control.

#### Strategy Principles
The core principles involve capturing price trends through dual moving average channels and establishing strict entry and exit mechanisms:
1. Entry Mechanism: Requires price to maintain above the upper band for five consecutive days, ensuring trend continuity and validity
2. Exit Mechanism: Operates on two levels
   - Trend Deviation Exit: Triggered when price falls below the lower band for five consecutive days, indicating potential trend reversal
   - Stop-Loss Exit: Activated when price retraces 25% from the highest point, preventing excessive losses
3. Position Management: Uses a fixed percentage of account equity for position sizing, ensuring effective capital allocation

#### Strategy Advantages
1. Trend Following Stability: Filters out false breakouts by requiring five consecutive days of confirmation
2. Comprehensive Risk Control: Combines trend deviation and stop-loss mechanisms for dual protection
3. Flexible Parameters: Moving average periods and stop-loss percentage can be optimized for different market characteristics
4. Clear Execution Logic: Definitive entry and exit conditions reduce subjective judgment interference
5. Scientific Capital Management: Uses account proportion positioning rather than fixed lots for better risk control

#### Strategy Risks
1. Choppy Market Risk: Prone to false signals in sideways markets, leading to frequent trading
2. Slippage Risk: Stop-loss execution prices may significantly deviate from expectations in fast markets
3. Parameter Dependency: Optimal parameters may vary significantly across different market environments
4. Trend Lag: Moving averages introduce some delay at trend reversal points
5. Capital Efficiency: Strict holding conditions may miss some profit opportunities

#### Optimization Directions
1. Dynamic Parameter Optimization: Develop adaptive parameter systems that automatically adjust moving average periods based on market volatility
2. Market Environment Filtering: Add trend strength indicators to automatically reduce trading frequency in choppy markets
3. Multiple Timeframe Confirmation: Incorporate longer timeframe trend confirmation mechanisms to improve signal reliability
4. Stop-Loss Optimization: Introduce dynamic stop-loss mechanisms that automatically adjust based on volatility
5. Position Management Optimization: Dynamically adjust position sizing based on volatility and risk-reward ratios

#### Summary
This strategy constructs a complete trend following trading system through dual moving average channels, combining strict entry confirmation and dual exit mechanisms to achieve effective trend tracking and risk control. The strategy's strengths lie in its clear execution logic and comprehensive risk control, though it requires parameter optimization for different market environments and can be further improved through market environment filtering and multiple timeframe confirmation. Overall, it represents a structurally complete and logically rigorous quantitative trading strategy, suitable for application in markets with clear trends.




> Source (PineScript)

``` pinescript
/*backtest
start: 2025-01-02 00:00:00
end: 2025-01-09 00:00:00
period: 10m
basePeriod: 10m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT","balance":49999}]
*/

//@version=5
strategy("Moving Average Channel (MAC)", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

// Parameters for Moving Averages
upperMALength = input.int(10, title="Upper MA Length")
lowerMALength = input.int(8, title="Lower MA Length")
stopLossPercent = input.float(25.0, title="Stop Loss (%)", minval=0.1) / 100

// Calculate Moving Averages
upperMA = ta.sma(high, upperMALength)
lowerMA = ta.sma(low, lowerMALength)

// Plot Moving Averages
plot(upperMA, color=color.red, title="Upper Moving Average")
plot(lowerMA, color=color.green, title="Lower Moving Average")

// Initialize variables
var int upperCounter = 0
var int lowerCounter = 0
var float entryPrice = na
var float highestPrice = na

// Update counters based on conditions
if (low <= upperMA)
    upperCounter := 0
else
    upperCounter += 1

if (high >= lowerMA)
    lowerCounter := 0
else
    lowerCounter += 1

// Entry condition: 5 consecutive bars above the Upper MA
if (upperCounter == 5 and strategy.position_size == 0)
    strategy.entry("Long", strategy.long)
    highestPrice := high  // Initialize highest price

// Update the highest price after entry
if (strategy.position_size > 0)
    highestPrice := na(highestPrice) ? high : math.max(highestPrice, high)

// Exit condition: 5 consecutive bars below the Lower MA
if (lowerCounter == 5 and strategy.position_size > 0)
    strategy.close("Long", comment="Exit: 5 bars below Lower MA")

// Stop-loss condition: Exit if market closes below 25% of the highest price since entry
stopLossCondition = low < highestPrice * (1 - stopLossPercent)
if (stopLossCondition and strategy.position_size > 0)
    strategy.close("Long", comment="Exit: Stop Loss")

```

> Detail

https://www.fmz.com/strategy/477974

> Last Modified

2025-01-10 16:26:56
