
> Name

Dynamic-Volatility-Trading-Strategy-Based-on-Bollinger-Bands-and-Candlestick-Patterns

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/f6b3e0820b82acd61b.png)


#### Overview
This strategy is a trading system based on Bollinger Bands and candlestick pattern analysis, designed to capture market reversals by analyzing price volatility and candlestick characteristics on the daily timeframe. The core methodology combines Bollinger Bands' volatility channels with the ratio relationship between candlestick shadows and bodies, looking for potential reversal signals when price touches the Bollinger Band boundaries. The system supports multi-timeframe analysis, allowing traders to execute trades on smaller timeframes while maintaining daily-level analysis.

#### Strategy Principles
The strategy employs 20-period Bollinger Bands as the primary technical indicator with a standard deviation multiplier of 2.0. By calculating the ratio between candlestick shadows and bodies, the system generates trading signals when this ratio exceeds a set threshold (default 1.0) and price touches the Bollinger Band boundaries. Entry timing can be flexibly chosen at daily close, next day's open, daily high, or low. The strategy includes a risk management system based on account balance, controlling risk through dynamic position sizing. Stop-loss is set at recent swing highs or lows, with take-profit targets at the opposite Bollinger Band.

#### Strategy Advantages
1. Multi-dimensional Analysis: Combines technical indicators and price pattern analysis for improved signal reliability.
2. Flexible Entry Mechanism: Offers multiple entry timing options to suit different trading styles.
3. Comprehensive Risk Management: Controls risk through dynamic position sizing and automated stop-loss.
4. Multi-timeframe Compatibility: Enables trading on smaller timeframes while maintaining daily analysis.
5. High Automation Level: Automates everything from signal identification to position management.

#### Strategy Risks
1. Market Volatility Risk: May generate false signals in highly volatile markets.
2. Lag Risk: Daily data usage might result in delayed responses in fast-moving markets.
3. Parameter Sensitivity: Strategy performance significantly depends on Bollinger Band parameters and shadow ratio threshold choices.
4. Liquidity Risk: May face execution challenges in less liquid markets.

#### Strategy Optimization Directions
1. Incorporate Volume Analysis: Integrate volume data to validate price reversals.
2. Add Market Environment Filters: Include trend strength indicators to filter unfavorable market conditions.
3. Optimize Parameter Adaptation: Dynamically adjust Bollinger Band parameters and shadow ratio thresholds based on market volatility.
4. Enhance Risk Control: Add drawdown control and equity curve monitoring mechanisms.
5. Strengthen Signal Confirmation: Introduce additional technical indicators as confirmation tools.

#### Summary
This is a comprehensive trading system combining Bollinger Bands and candlestick analysis to capture market reversal opportunities. The strategy's strengths lie in its comprehensive analytical framework and robust risk management system, while attention must be paid to market conditions and parameter selection impacts. Through the suggested optimization directions, the strategy's stability and reliability can be further enhanced. For live trading implementation, thorough backtesting and parameter optimization are recommended, with adjustments made according to specific trading instrument characteristics.




> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-29 00:00:00
end: 2024-11-28 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Trade Entry Detector, based on Wick to Body Ratio when price tests Bollinger Bands", overlay=true, default_qty_type=strategy.fixed)

// Input for primary analysis time frame
timeFrame = "D"  // Daily time frame

// Bollinger Band settings
length = input.int(20, title="Bollinger Band Length", minval=1)
mult = input.float(2.0, title="Standard Deviation Multiplier", minval=0.1)
source = input(close, title="Source")

// Entry ratio settings
wickToBodyRatio = input.float(1.0, title="Minimum Wick-to-Body Ratio", minval=0)

// Order Fill Timing Option
fillOption = input.string("Daily Close", title="Order Fill Timing", options=["Daily Close", "Daily Open", "HOD", "LOD"])

// Account and risk settings
accountBalance = 100000  // Account balance in dollars
riskPercentage = 1.0     // Risk percentage per trade
riskAmount = (riskPercentage / 100) * accountBalance // Fixed 1% risk amount

// Request daily data for calculations
dailyHigh = request.security(syminfo.tickerid, timeFrame, high)
dailyLow = request.security(syminfo.tickerid, timeFrame, low)
dailyClose = request.security(syminfo.tickerid, timeFrame, close)
dailyOpen = request.security(syminfo.tickerid, timeFrame, open)

// Calculate Bollinger Bands on the daily time frame
dailyBasis = request.security(syminfo.tickerid, timeFrame, ta.sma(source, length))
dailyDev = mult * request.security(syminfo.tickerid, timeFrame, ta.stdev(source, length))
dailyUpperBand = dailyBasis + dailyDev
dailyLowerBand = dailyBasis - dailyDev

// Calculate the body and wick sizes on the daily time frame
dailyBodySize = math.abs(dailyOpen - dailyClose)
dailyUpperWickSize = dailyHigh - math.max(dailyOpen, dailyClose)
dailyLowerWickSize = math.min(dailyOpen, dailyClose) - dailyLow

// Conditions for a candle with an upper wick or lower wick that touches the Bollinger Bands
upperWickCondition = (dailyUpperWickSize / dailyBodySize >= wickToBodyRatio) and (dailyHigh > dailyUpperBand)
lowerWickCondition = (dailyLowerWickSize / dailyBodySize >= wickToBodyRatio) and (dailyLow < dailyLowerBand)

// Define the swing high and swing low for stop loss placement
var float swingLow = na
var float swingHigh = na

if (ta.pivothigh(dailyHigh, 5, 5))
    swingHigh := dailyHigh[5]

if (ta.pivotlow(dailyLow, 5, 5))
    swingLow := dailyLow[5]

// Determine entry price based on chosen fill option
var float longEntryPrice = na
var float shortEntryPrice = na

if lowerWickCondition
    longEntryPrice := fillOption == "Daily Close" ? dailyClose :
                      fillOption == "Daily Open" ? dailyOpen :
                      fillOption == "HOD" ? dailyHigh : dailyLow

if upperWickCondition
    shortEntryPrice := fillOption == "Daily Close" ? dailyClose :
                       fillOption == "Daily Open" ? dailyOpen :
                       fillOption == "HOD" ? dailyHigh : dailyLow

// Execute the long and short entries with expiration
var int longOrderExpiry = na
var int shortOrderExpiry = na

if not na(longEntryPrice)
    longOrderExpiry := bar_index + 2  // Order expires after 2 days

if not na(shortEntryPrice)
    shortOrderExpiry := bar_index + 2  // Order expires after 2 days

// Check expiration and execute orders
if (longEntryPrice and bar_index <= longOrderExpiry and high >= longEntryPrice)
    longStopDistance = close - nz(swingLow, close)
    longPositionSize = longStopDistance > 0 ? riskAmount / longStopDistance : na
    if (not na(longPositionSize))
        strategy.entry("Long", strategy.long, qty=longPositionSize)
    longEntryPrice := na  // Reset after entry

if (shortEntryPrice and bar_index <= shortOrderExpiry and low <= shortEntryPrice)
    shortStopDistance = nz(swingHigh, close) - close
    shortPositionSize = shortStopDistance > 0 ? riskAmount / shortStopDistance : na
    if (not na(shortPositionSize))
        strategy.entry("Short", strategy.short, qty=shortPositionSize)
    shortEntryPrice := na  // Reset after entry

// Exit logic: hit the opposing Bollinger Band
if (strategy.position_size > 0) // Long position
    strategy.exit("Exit Long", "Long", limit=dailyUpperBand)
else if (strategy.position_size < 0) // Short position
    strategy.exit("Exit Short", "Short", limit=dailyLowerBand)

if (strategy.position_size > 0) // Long position
    strategy.exit("Stop Loss Long", "Long", stop=swingLow)
else if (strategy.position_size < 0) // Short position
    strategy.exit("Stop Loss Short", "Short", stop=swingHigh)

// Plot daily Bollinger Bands and levels on the chosen time frame
plot(dailyUpperBand, color=color.blue, linewidth=1, title="Daily Upper Bollinger Band")
plot(dailyLowerBand, color=color.blue, linewidth=1, title="Daily Lower Bollinger Band")
plot(dailyBasis, color=color.gray, linewidth=1, title="Daily Middle Bollinger Band")

```

> Detail

https://www.fmz.com/strategy/473394

> Last Modified

2024-11-29 16:29:01
