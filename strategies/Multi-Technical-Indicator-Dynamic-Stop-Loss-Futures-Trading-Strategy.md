
> Name

Multi-Technical-Indicator-Dynamic-Stop-Loss-Futures-Trading-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d85e924a750a7599f716.png)
![IMG](https://www.fmz.com/upload/asset/2d913d89a425122404f85.png)




#### Strategy Overview
This strategy is an advanced futures trading system that combines multiple technical conditions and higher timeframe analysis to identify high-probability trading opportunities. The strategy employs a confluence-based approach, requiring multiple technical conditions to align before entering a trade. It integrates several sophisticated technical concepts including Fair Value Gaps (FVG), Order Blocks, Liquidity Sweeps, and Break of Structure (BOS) signals, while utilizing multi-timeframe indicators to confirm trend direction.

#### Strategy Principles
The core of this strategy is the combination of multiple technical analysis methods to ensure trades are only entered when several indicators align. Specifically, the strategy includes the following key components:

1. **Fair Value Gaps (FVG)** - Identified when there is a significant price gap between two candles, indicating potential unfilled space in the market.
2. **Order Blocks** - These are key areas where price formed a reversal, typically shown as strong rejection candles that later become support or resistance zones.
3. **Liquidity Sweeps** - Identifies instances where the market breaks previous highs or lows and then quickly reverses, typically indicating institutional collection of liquidity.
4. **Break of Structure (BOS)** - Occurs when price breaks a previous structure, forming higher highs or lower lows.
5. **Higher Timeframe Trend Confirmation** - Uses 15-minute and 60-minute timeframe EMAs (Exponential Moving Averages) to confirm the overall trend direction.

The strategy only generates entry signals when at least two basic conditions (one in debug mode) plus a Break of Structure signal are present, and these align with the higher timeframe trend.

For risk management, the strategy uses ATR (Average True Range) to set dynamic stop-loss positions, typically at 1.5 times the ATR value. This approach increases stop distance during high volatility and reduces it during low volatility, making the stops more intelligent.

For profit-taking, the strategy employs a partial profit approach, taking 50% of the position at a profit equal to the risk (1R), while moving the stop-loss for the remaining position to breakeven, creating a risk-free opportunity. Additionally, there's a time-based exit mechanism that automatically closes trades if they don't move favorably within a specified time (default 30 minutes).

Furthermore, the strategy includes account management features that automatically exit all positions when the account profit reaches a preset target ($3,000) or triggers a trailing stop (which begins tracking after the account exceeds $2,500 in profit).

#### Strategy Advantages
After deep analysis of the code, we can summarize the following clear advantages:

1. **Multiple Confirmation System** - Requiring several technical conditions to be met simultaneously reduces false signals and improves trade quality.
2. **Intelligent Risk Management** - Using ATR-based dynamic stops adapts better to market volatility changes than fixed point or percentage stops.
3. **Higher Timeframe Trend Filtering** - Utilizing higher timeframe trend direction avoids counter-trend trading by only trading in the direction of the trend.
4. **Partial Profit Strategy** - Through partial profit-taking and moving stops to breakeven, the strategy both secures partial profits and creates risk-free opportunities for remaining positions.
5. **Time-Based Exit Mechanism** - Automatically exits ineffective trades, preventing capital from being tied up in trades without momentum.
6. **Overall Account Management** - Protects overall account profits through profit targets and trailing stops, achieving robust capital management.
7. **High Adaptability** - Offers high flexibility through multiple parameters that can be adjusted according to different market conditions and trading styles.
8. **Professional Technical Indicator Integration** - Combines multiple advanced technical analysis concepts typically used only by professional traders.

#### Strategy Risks
Despite its sophisticated design, there are several potential risks, including:

1. **Parameter Optimization Risk** - The strategy relies on multiple parameter settings, which if over-optimized could lead to overfitting and poor performance in future market conditions. The solution is to use sufficiently long testing periods and conduct forward testing.
2. **Market Environment Dependency** - The strategy may perform excellently in trending markets but could generate more false signals in range-bound markets. The solution is to add market environment filters and adjust trading frequency or stop trading entirely when a ranging market is identified.
3. **Execution Slippage Risk** - During high volatility periods, entry and exit prices may differ significantly from expectations, affecting strategy performance. The solution is to simulate realistic slippage in backtesting and use limit orders instead of market orders in actual trading.
4. **Technical Failure Risk** - Automated trading systems may face technical failures or network interruptions. The solution is to establish backup systems and manual intervention mechanisms.
5. **Complexity Management** - The strategy's complexity may make it difficult to diagnose problems or understand why certain trades failed. The solution is to maintain detailed trading logs and regularly analyze strategy performance.
6. **Market Liquidity Risk** - Under specific market conditions, such as before and after important news releases, liquidity may rapidly decrease, leading to greater slippage or inability to exit positions. The solution is to avoid trading during major economic data releases or reduce position sizes during these periods.

#### Strategy Optimization Directions
Based on code analysis, here are several potential optimization directions:

1. **Enhanced Trend Identification** - The current strategy uses simple EMA crossovers to determine trends; consider adding other trend indicators like ADX (Average Directional Index) to confirm trend strength, as strong trending markets typically provide better trading opportunities.
2. **Market State Adaptation** - Add market state recognition mechanisms to automatically adjust strategy parameters in different market environments (trending, ranging, high volatility, low volatility). This would make the strategy more flexible and adaptive to different market conditions.
3. **Optimized Entry Timing** - Consider adding momentum indicators like RSI or stochastic oscillators to ensure that when entering in the trend direction, we also avoid entering in oversold or overbought conditions, thereby reducing reversal risk.
4. **Improved Profit Strategy** - The current fixed 1R profit target may be too conservative or too aggressive; consider dynamically adjusting profit targets based on volatility or support/resistance levels, setting farther targets during higher volatility.
5. **Refined Risk Management** - Introduce dynamic position sizing adjustment mechanisms that automatically adjust risk exposure based on recent strategy performance and market volatility, increasing risk when the strategy performs well and reducing it when performance declines.
6. **Add Intraday Time Filters** - Futures markets have different characteristics during different time periods; adding time filters can avoid periods with poor liquidity or directionless markets.
7. **Integrate Market Sentiment Indicators** - Add market sentiment indicators like VIX to adjust strategy parameters or pause trading during extreme sentiment situations.
8. **Optimize Code Efficiency** - Some loop operations in the current code may affect execution efficiency, especially on smaller timeframes. Optimizing these loops can improve strategy response speed.

#### Summary
This is a well-designed multi-indicator futures trading strategy that integrates various advanced technical analysis concepts and features comprehensive risk and capital management functions. It reduces false signals by requiring multiple conditions to align simultaneously and higher timeframe trend confirmation, while using ATR-based dynamic stops and partial profit strategies to optimize the risk-reward ratio.

The strategy's main advantages lie in its multi-layered confirmation system and intelligent risk management, allowing it to capture high-probability trading opportunities while maintaining relatively low risk. However, the complexity of the strategy also brings challenges in parameter optimization and market adaptability, requiring continuous monitoring and regular adjustments to maintain its effectiveness.

By implementing the suggested optimization measures, especially enhancing market state adaptability and improving risk management systems, the strategy has the potential to maintain stable performance across different market environments. Overall, this is an advanced strategy suitable for experienced traders, which can become a powerful tool in a trading system with appropriate monitoring and adjustment.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-04-02 00:00:00
end: 2025-04-01 00:00:00
period: 2d
basePeriod: 2d
exchanges: [{"eid":"Futures_Binance","currency":"ETH_USDT"}]
*/

// @version=5
strategy("NQ Futures Trading Strategy", overlay=true, initial_capital=50000, default_qty_type=strategy.cash, default_qty_value=5000)

// ==========================================
// Parameters
// ==========================================

// Account Parameters
accountSize = 50000
profitGoal = 3000
trailingThreshold = 2500
stopsTrailing = 52650

// Trading Parameters
atrLength = input.int(14, "ATR Period", minval=1)
atrMultiplier = input.float(1.5, "ATR Multiplier for SL", minval=0.5, maxval=3.0, step=0.1)
timeoutPeriod = input.int(30, "Exit after X minutes if trade doesn't move favorably", minval=5, maxval=120)

// FVG (Fair Value Gap) Parameters
fvgLength = input.int(5, "FVG Look-back Period", minval=2, maxval=20)
fvgThreshold = input.float(0.1, "FVG Size Threshold (%)", minval=0.05, maxval=1.0, step=0.05) * 0.01

// Order Block Parameters
obLength = input.int(5, "Order Block Look-back Period", minval=2, maxval=20)
obThreshold = input.float(0.1, "Order Block Size Threshold (%)", minval=0.05, maxval=1.0, step=0.05) * 0.01

// Liquidity Sweep Parameters
sweepLength = input.int(5, "Liquidity Sweep Look-back Period", minval=2, maxval=20)
sweepThreshold = input.float(0.05, "Sweep Size Threshold (%)", minval=0.01, maxval=0.5, step=0.01) * 0.01

// Break of Structure Parameters
bosLength = input.int(5, "BOS Look-back Period", minval=2, maxval=20)
bosThreshold = input.float(0.05, "BOS Size Threshold (%)", minval=0.01, maxval=0.5, step=0.01) * 0.01

// Debug Mode
debugMode = input.bool(false, "Debug Mode (more signals)")

// Higher Timeframe Trend Parameters
htfPeriod1 = input.timeframe("15", "First Higher Timeframe")
htfPeriod2 = input.timeframe("60", "Second Higher Timeframe")

// ==========================================
// Indicators & Calculations
// ==========================================

// ATR Calculation
atr = ta.atr(atrLength)

// Higher Timeframe EMAs for Trend Determination
htf1_ema20 = request.security(syminfo.tickerid, htfPeriod1, ta.ema(close, 20), barmerge.gaps_off, barmerge.lookahead_off)
htf1_ema50 = request.security(syminfo.tickerid, htfPeriod1, ta.ema(close, 50), barmerge.gaps_off, barmerge.lookahead_off)
htf2_ema20 = request.security(syminfo.tickerid, htfPeriod2, ta.ema(close, 20), barmerge.gaps_off, barmerge.lookahead_off)
htf2_ema50 = request.security(syminfo.tickerid, htfPeriod2, ta.ema(close, 50), barmerge.gaps_off, barmerge.lookahead_off)

// Higher Timeframe Trend
htf1_bullish = htf1_ema20 > htf1_ema50
htf1_bearish = htf1_ema20 < htf1_ema50
htf2_bullish = htf2_ema20 > htf2_ema50
htf2_bearish = htf2_ema20 < htf2_ema50

// ==========================================
// Entry Conditions
// ==========================================

// 1. Fair Value Gap (FVG)
bullishFVG = false
bearishFVG = false

for i = 1 to fvgLength
    if low[i] > high[i+2] and (low[i] - high[i+2]) / high[i+2] > fvgThreshold
        bullishFVG := true
    if high[i] < low[i+2] and (low[i+2] - high[i]) / high[i] > fvgThreshold
        bearishFVG := true

// 2. Inverse Fair Value Gap
inverseBullishFVG = false
inverseBearishFVG = false

for i = 1 to fvgLength
    if high[i+1] < low[i+2] and close[i] > open[i] and close[i] > high[i+1]
        inverseBullishFVG := true
    if low[i+1] > high[i+2] and close[i] < open[i] and close[i] < low[i+1]
        inverseBearishFVG := true

// 3. Order Block / Breaker Block
bullishOrderBlock = false
bearishOrderBlock = false

for i = 1 to obLength
    if close[i+1] < open[i+1] and (open[i+1] - close[i+1]) / close[i+1] > obThreshold and close[i] > open[i]
        bullishOrderBlock := true
    if close[i+1] > open[i+1] and (close[i+1] - open[i+1]) / open[i+1] > obThreshold and close[i] < open[i]
        bearishOrderBlock := true

// 4. Liquidity Sweep
bullishSweep = false
bearishSweep = false

lowestLow = ta.lowest(low, sweepLength+1)
highestHigh = ta.highest(high, sweepLength+1)

if low[1] < lowestLow[2] and close > open
    bullishSweep := true
if high[1] > highestHigh[2] and close < open
    bearishSweep := true

// 5. Break of Structure (BOS)
bullishBOS = false
bearishBOS = false

prevHigh = high[2]
prevLow = low[2]

if high > prevHigh and low[1] < low[2]
    bullishBOS := true
if low < prevLow and high[1] > high[2]
    bearishBOS := true

// Simpler version for debug mode
if debugMode
    bullishBOS := close > open and close > close[1]
    bearishBOS := close < open and close < close[1]

// ==========================================
// Signal Generation
// ==========================================

// Count valid entry conditions
bullishConditions = bullishFVG ? 1 : 0
bullishConditions := bullishConditions + (inverseBullishFVG ? 1 : 0)
bullishConditions := bullishConditions + (bullishOrderBlock ? 1 : 0)
bullishConditions := bullishConditions + (bullishSweep ? 1 : 0)

bearishConditions = bearishFVG ? 1 : 0
bearishConditions := bearishConditions + (inverseBearishFVG ? 1 : 0)
bearishConditions := bearishConditions + (bearishOrderBlock ? 1 : 0)
bearishConditions := bearishConditions + (bearishSweep ? 1 : 0)

// Entry signals (need at least 2 conditions + BOS confirmation)
// In debug mode, require only 1 condition
minConditions = debugMode ? 1 : 2
longSignal = bullishConditions >= minConditions and bullishBOS and (htf1_bullish or htf2_bullish)
shortSignal = bearishConditions >= minConditions and bearishBOS and (htf1_bearish or htf2_bearish)

// Debug mode override for testing
if debugMode
    longSignal := longSignal or (bullishBOS and htf1_bullish)
    shortSignal := shortSignal or (bearishBOS and htf1_bearish)

// ==========================================
// Risk Management
// ==========================================

// Calculate dynamic stop loss based on ATR
longStopDistance = atr * atrMultiplier
shortStopDistance = atr * atrMultiplier

// Default fixed values for testing
if debugMode
    longStopDistance := close * 0.01  // 1% stop
    shortStopDistance := close * 0.01  // 1% stop

// Calculate position size based on risk
nqPointValue = 20  // Each point is $20 for NQ
longPositionSize = math.floor(2000 / (longStopDistance * nqPointValue))
shortPositionSize = math.floor(2000 / (shortStopDistance * nqPointValue))

// Ensure at least 1 contract
longPositionSize := math.max(longPositionSize, 1)
shortPositionSize := math.max(shortPositionSize, 1)

// Variables to track entry time
var int entryTime = 0
var float equityCurve = accountSize

// ==========================================
// Strategy Execution
// ==========================================

// Make sure we don't get multiple signals on the same bar
var longEnteredThisBar = false
var shortEnteredThisBar = false

longEnteredThisBar := false
shortEnteredThisBar := false

// Entry conditions
if longSignal and not longEnteredThisBar and strategy.position_size <= 0
    strategy.close_all()
    strategy.entry("Long", strategy.long, qty=longPositionSize)
    longEnteredThisBar := true
    entryTime := time

if shortSignal and not shortEnteredThisBar and strategy.position_size >= 0
    strategy.close_all()
    strategy.entry("Short", strategy.short, qty=shortPositionSize)
    shortEnteredThisBar := true
    entryTime := time

// Take profit and stop loss orders
if strategy.position_size > 0
    stopPrice = strategy.position_avg_price - longStopDistance
    takeProfitPrice1 = strategy.position_avg_price + longStopDistance
    strategy.exit("Long TP1", "Long", qty_percent=50, limit=takeProfitPrice1, stop=stopPrice)
    
    // Move stop to breakeven after 1R move
    if high >= takeProfitPrice1
        strategy.exit("Long BE", "Long", stop=strategy.position_avg_price)

if strategy.position_size < 0
    stopPrice = strategy.position_avg_price + shortStopDistance
    takeProfitPrice1 = strategy.position_avg_price - shortStopDistance
    strategy.exit("Short TP1", "Short", qty_percent=50, limit=takeProfitPrice1, stop=stopPrice)
    
    // Move stop to breakeven after 1R move
    if low <= takeProfitPrice1
        strategy.exit("Short BE", "Short", stop=strategy.position_avg_price)

// Time-based exit
if strategy.position_size != 0
    currentTime = time
    if (currentTime - entryTime) >= timeoutPeriod * 60000  // Convert minutes to milliseconds
        strategy.close_all(comment="Time Exit")

// ==========================================
// Trailing Stop for Account Management
// ==========================================

// Update equity curve
equityCurve := strategy.equity

// Check if profit target is reached or trailing stop is hit
if strategy.equity >= accountSize + profitGoal
    strategy.close_all(comment="Profit Goal")

if strategy.equity >= accountSize + trailingThreshold
    trailingStop = math.max(accountSize, strategy.equity - trailingThreshold)
    if strategy.equity <= trailingStop
        strategy.close_all(comment="Trailing Stop")

// Stop trailing if account reaches the stop trailing threshold
if strategy.equity >= stopsTrailing
    strategy.close_all(comment="Stop Trailing")

// ==========================================
// Plotting
// ==========================================

// Plot entry conditions
plotshape(longSignal, title="Long Signal", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
plotshape(shortSignal, title="Short Signal", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)

// Plot current position
bgcolor(strategy.position_size > 0 ? color.new(color.green, 90) : strategy.position_size < 0 ? color.new(color.red, 90) : na)

// Alert conditions
alertcondition(longSignal, title="Long Entry Signal", message="NQ LONG ENTRY: {{ticker}}, Price: {{close}}")
alertcondition(shortSignal, title="Short Entry Signal", message="NQ SHORT ENTRY: {{ticker}}, Price: {{close}}")
alertcondition(strategy.position_size > 0 and high >= strategy.position_avg_price + longStopDistance, title="Long Take Profit", message="NQ LONG TP: {{ticker}}, Price: {{close}}")
alertcondition(strategy.position_size < 0 and low <= strategy.position_avg_price - shortStopDistance, title="Short Take Profit", message="NQ SHORT TP: {{ticker}}, Price: {{close}}")
alertcondition(strategy.position_size > 0 and low <= strategy.position_avg_price - longStopDistance, title="Long Stop Loss", message="NQ LONG SL: {{ticker}}, Price: {{close}}")
alertcondition(strategy.position_size < 0 and high >= strategy.position_avg_price + shortStopDistance, title="Short Stop Loss", message="NQ SHORT SL: {{ticker}}, Price: {{close}}")
```

> Detail

https://www.fmz.com/strategy/489135

> Last Modified

2025-04-02 09:41:48
