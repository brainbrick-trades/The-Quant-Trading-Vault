
> Name

Dynamic-Volatility-Adjusted-Trend-Following-Strategy-Based-on-DI-Indicators-with-ATR-Stop-Management

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/147db016b817dfdd444.png)


#### Overview
This strategy is a trend following system that combines the Directional Movement Index (DMI) with Average True Range (ATR). The core mechanism uses DI+ and DI- indicators to identify market trend direction and strength, while utilizing ATR for dynamic stop-loss and take-profit adjustments. The introduction of a trend filtering moving average further enhances signal reliability. The strategy design considers market volatility and demonstrates good adaptability.

#### Strategy Principle
The strategy operates based on the following core mechanisms:
1. Uses DI+ and DI- indicators to measure trend direction and strength. When DI+ exceeds DI- by the threshold value, an uptrend is confirmed; vice versa for downtrends.
2. Incorporates a trend filtering moving average (SMA) as a trend confirmation tool. Signals are only triggered when price and moving average positions mutually confirm.
3. Utilizes ATR indicator to dynamically calculate stop-loss and take-profit levels, ensuring risk management adapts to different market conditions.
4. Strictly follows time restrictions in trade execution to avoid excessive trading frequency.

#### Strategy Advantages
1. Strong Dynamic Adjustment - Achieves market volatility adaptation through ATR.
2. Comprehensive Risk Control - Implements volatility-based dynamic stop-loss and take-profit mechanisms.
3. High Signal Reliability - Reduces false signals through multiple indicator cross-validation.
4. Flexible Parameters - Strategy parameters can be optimized for different market characteristics.
5. Clear Execution Logic - Precise entry and exit conditions facilitate real-world implementation.

#### Strategy Risks
1. Oscillation Market Risk - May result in consecutive stops in range-bound markets.
Suggestion: Add oscillation indicators for filtering or adjust parameter thresholds.

2. Slippage Risk - May face significant slippage during high volatility periods.
Suggestion: Appropriately widen stop-loss positions to accommodate slippage.

3. False Breakout Risk - Potential misjudgments at trend turning points.
Suggestion: Incorporate volume indicators for signal confirmation.

4. Parameter Sensitivity - Performance varies significantly with different parameter combinations.
Suggestion: Find stable parameter ranges through backtesting.

#### Strategy Optimization Directions
1. Signal Optimization - Consider introducing ADX indicator for trend strength evaluation or adding volume confirmation mechanisms.

2. Position Management - Implement dynamic position sizing based on trend strength for more refined risk control.

3. Time Structure - Consider multi-timeframe analysis to enhance signal reliability.

4. Market Adaptability - Develop adaptive parameter adjustment mechanisms based on different instrument characteristics.

#### Summary
This strategy achieves dynamic trend following and risk control by combining directional and volatility indicators. The strategy design emphasizes practicality and operability, demonstrating strong market adaptability. Through parameter optimization and signal improvements, there is room for further enhancement. Investors are advised to thoroughly test and make specific adjustments based on market characteristics before implementation.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2025-01-04 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Use the DI+ and DI- strategy (finally fully corrected and includes chart stop-loss and take-profit lines).)", overlay=true)

// Input parameters
diLength = input.int(title="DI Length", defval=14)
adxSmoothing = input.int(title="ADX Smoothing", defval=14)
trendFilterLength = input.int(title="Trend filter moving average length", defval=20)
strengthThreshold = input.int(title="Trend strength threshold value", defval=20)
atrLength = input.int(title="ATR Length", defval=14)
atrMultiplierStop = input.float(title="ATR Stop loss multiple", defval=1.5)
atrMultiplierTakeProfit = input.float(title="ATR Take profit multiple", defval=2.5)

// Calculate DI+ and DI-
[diPlus, diMinus, _] = ta.dmi(diLength, adxSmoothing)

// Calculate trend filter moving average
trendFilterMA = ta.sma(close, trendFilterLength)

// Determine trend direction and strength
strongUpTrend = diPlus > diMinus + strengthThreshold and close > trendFilterMA
strongDownTrend = diMinus > diPlus + strengthThreshold and close < trendFilterMA

// Calculate ATR
atr = ta.atr(atrLength)

// Track stop loss and take profit prices (Use var Declaration, only update upon entry)
var float longStopPrice = na
var float longTakeProfitPrice = na
var float shortStopPrice = na
var float shortTakeProfitPrice = na

// Entry logic
longCondition = strongUpTrend
shortCondition = strongDownTrend

if (longCondition)
    strategy.entry("Long order", strategy.long)
    longStopPrice := close - atr * atrMultiplierStop // Calculate and update the stop loss price when entering the market
    longTakeProfitPrice := close + atr * atrMultiplierTakeProfit // Calculate and update the take profit price when entering the market

if (shortCondition)
    strategy.entry("Empty order", strategy.short)
    shortStopPrice := close + atr * atrMultiplierStop // Calculate and update the stop loss price when entering the market
    shortTakeProfitPrice := close - atr * atrMultiplierTakeProfit // Calculate and update the take profit price when entering the market


// Exit logic (Use time Limits and ATR)
inLongPosition = strategy.position_size > 0
inShortPosition = strategy.position_size < 0

lastEntryTime = strategy.opentrades.entry_bar_index(strategy.opentrades - 1)

if (inLongPosition and time > lastEntryTime)
    strategy.exit("Long position exit", "Long order", stop=longStopPrice, limit=longTakeProfitPrice)

if (inShortPosition and time > lastEntryTime)
    strategy.exit("Short position exit", "Empty order", stop=shortStopPrice, limit=shortTakeProfitPrice)

// Draw DI+,DI- And trend filter moving average
plot(diPlus, color=color.green, title="DI+")
plot(diMinus, color=color.red, title="DI-")
plot(trendFilterMA, color=color.blue, title="Trend filtering moving average")

// Draw stop loss and take profit lines (Use plot Function drawing)
plot(strategy.position_size > 0 ? longStopPrice : na, color=color.red, style=plot.style_linebr, linewidth=2, title="Long stop loss")
plot(strategy.position_size > 0 ? longTakeProfitPrice : na, color=color.green, style=plot.style_linebr, linewidth=2, title="Take Profit on Buy")
plot(strategy.position_size < 0 ? shortStopPrice : na, color=color.red, style=plot.style_linebr, linewidth=2, title="Short stop loss")
plot(strategy.position_size < 0 ? shortTakeProfitPrice : na, color=color.green, style=plot.style_linebr, linewidth=2, title="Take Profit on Sell")
```

> Detail

https://www.fmz.com/strategy/477595

> Last Modified

2025-01-06 16:18:01
