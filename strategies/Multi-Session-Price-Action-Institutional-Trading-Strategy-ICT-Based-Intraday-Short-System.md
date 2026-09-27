
> Name

Multi-Session-Price-Action-Institutional-Trading-Strategy-ICT-Based-Intraday-Short-System

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d7e40632fbab41f7f128.png)
![IMG](https://www.fmz.com/upload/asset/2d87a352b683e654be68f.png)




#### Overview

The Multi-Session Price Action Institutional Trading Strategy is an intraday trading system based on ICT (Inner Circle Trader) concepts, specifically designed to capture market downtrends. The strategy tracks price action across three major trading sessions-London, New York, and Asia-to identify institutional money flow and seek high-probability shorting opportunities at key price levels. The core of the strategy lies in utilizing the interconnected relationships between different trading sessions and price structures, combined with institutional trading concepts such as the "Judas Swing," to execute precise entries in areas of concentrated liquidity.

#### Strategy Principles

The strategy operates based on price structure analysis across multiple trading sessions, comprising several key components:

1. **London Open Setup (2:00-8:20 NY time)**: The code uses the variable `sessionLondon` to set the London session start time and continuously updates the session high `londonHigh` and low `londonLow`. The London session typically establishes the initial direction for the day.

2. **New York Open Kill Zone (8:20-10:00 NY time)**: The code sets `sessionNYOpen` to capture the New York opening time. When price breaks above the London session high and then reverses during the NY session (known as the "Judas Swing"), meeting the condition `judasSwing = high >= londonHigh and time >= sessionNYOpen`, the system prepares for a short entry.

3. **London Close Buy Setup (10:30-13:00 NY time)**: The code's `londonCloseBuy` condition determines whether to trigger a long signal during the London closing session, requiring price to drop below the London session low, aiming to capture retracement bounces.

4. **Asia Open Sell Setup (19:00-2:00 NY time)**: The code identifies the start of the Asian session with `sessionAsia`, triggering a short entry when price breaks above the Asian session high (`close > asiaHigh`).

The core trading logic leverages the "Judas Swing" concept, where price temporarily breaks above the London high during the New York session before reversing, indicating that large institutions may be distributing at higher levels, making short positions highly probable. The strategy also incorporates a long reversal during the London closing session and a short strategy during the Asian session, forming a round-the-clock trading system.

#### Strategy Advantages

Through deep code analysis, this strategy demonstrates the following significant advantages:

1. **Multi-Session Collaborative Analysis**: The strategy integrates price data from three major trading sessions, comprehensively tracking different markets' price performance through variables like `londonHigh`, `nyHigh`, and `asiaHigh`, avoiding the limitations of single-session analysis.

2. **Institution-Based Entry Logic**: The strategy's core "Judas Swing" concept (the `judasSwing` condition) directly aligns with institutional trading behavior, effectively identifying manipulative actions and true intentions of large institutions.

3. **Precise Time Control**: Through the `timestamp` function, the strategy precisely sets the start and end times of each trading session, ensuring trades occur during the most active market periods, enhancing trading effectiveness.

4. **Clear Risk Management**: The code includes explicit stop-loss settings (`stopLoss = high + 10 * syminfo.mintick`) and profit targets (`profitTarget = low - 20 * syminfo.mintick`), making the risk controllable for each trade.

5. **Visualization Support**: The strategy uses the `plot` function to draw the highs and lows of each session, providing intuitive visual references for trading decisions, enhancing the strategy's practicality.

#### Strategy Risks

Despite its rational design, the strategy still faces several potential risks:

1. **False Breakout Risk**: In highly volatile markets, the "Judas Swing" signal may generate false breakouts, leading to incorrect short entries. A solution is to add filtering conditions, such as volume confirmation or waiting for more definitive price reversal patterns.

2. **Strong Time Dependency**: The strategy heavily relies on market behavior during specific time periods. If market characteristics change or major news is released at atypical times, the strategy's effectiveness may decrease. It's recommended to use it in conjunction with a market news calendar and pause trading before major data releases.

3. **Fixed Stop-Loss Setting**: The stop-loss in the code is set as a fixed number of points (`10 * syminfo.mintick`), not accounting for volatility differences across markets and sessions. This could be improved by implementing dynamic stops based on indicators like ATR.

4. **Lack of Filtering Mechanisms**: The strategy doesn't consider overall market trends and volatility environments, potentially generating frequent false short signals in strong upward markets. Adding trend filtering conditions, such as moving average direction or momentum indicators, is recommended.

5. **Backtest Bias Risk**: Since the strategy relies on price behavior during specific time periods, there may be forward-looking bias in low timeframe backtests. Traders should be aware of potential differences between strategy performance and backtest results in actual trading.

#### Strategy Optimization Directions

Based on code analysis, the strategy can be optimized in these directions:

1. **Dynamic Stop-Loss Mechanism**: Replace the fixed-point stop-loss (`stopLoss = high + 10 * syminfo.mintick`) with an ATR-based dynamic stop, such as `stopLoss = high + atr(14) * 1.5`, to better adapt to volatility characteristics in different market environments.

2. **Add Trend Filtering**: Incorporate trend determination conditions from higher timeframes, such as daily or 4-hour chart moving average directions, to trade only in the direction consistent with the larger trend, improving the strategy's win rate.

3. **Volume Confirmation**: Add volume analysis when the "Judas Swing" signal triggers, executing shorts only when price reversal is accompanied by increasing volume, reducing losses from false breakouts.

4. **Incorporate Market Sentiment Indicators**: Combine with VIX or other market volatility indicators to adjust or pause the strategy in extremely volatile environments, avoiding trading in unstable markets.

5. **Optimize Entry Timing**: The current short entry condition is simply `close < open`. This could be improved by waiting for price to retrace to key support levels (such as London session opening price or VWAP) before entering, increasing entry precision.

6. **Add Multi-Timeframe Confirmation**: Combine price structures from lower timeframes to find more precise entry points after meeting the main entry conditions, reducing slippage and unnecessary risk.

These optimization directions aim to enhance the strategy's stability and reliability, enabling it to maintain good performance across different market environments.

#### Summary

The Multi-Session Price Action Institutional Trading Strategy is a comprehensive intraday trading system integrating ICT trading concepts, capturing high-probability trading opportunities driven by institutional money flow by analyzing price structures across the London, New York, and Asian trading sessions. The strategy's most distinctive feature is trading in alignment with institutional money flow, particularly using the "Judas Swing" concept to capture shorting opportunities, while also incorporating reversal long trades and Asian session shorts to form a complete trading system.

Although the strategy is well-designed with clear entry conditions and risk management rules, it still has drawbacks such as false breakout risks and strong dependency on specific time periods. By incorporating dynamic stop-losses, trend filtering, volume confirmation, and other optimization measures, the strategy's stability and adaptability can be further enhanced.

For traders pursuing intraday opportunities, this strategy provides a structured approach to understanding and capitalizing on market characteristics across different trading sessions, particularly suitable for those who wish to master institutional trading concepts and profit from intraday short-term positions.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-03-26 00:00:00
end: 2025-03-25 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"ETH_USDT"}]
*/

//@version=5
strategy("ICT Bread and Butter Sell-Setup", overlay=true)

// Get current date values
t = time
currentYear = year(t)
currentMonth = month(t)
currentDay = dayofmonth(t)

// Time Settings
sessionNYOpen  = timestamp(currentYear, currentMonth, currentDay, 08, 20) // CME Open
sessionLondon  = timestamp(currentYear, currentMonth, currentDay, 02, 00) // London Open
sessionAsia    = timestamp(currentYear, currentMonth, currentDay, 19, 00) // Asia Open
sessionEnd     = timestamp(currentYear, currentMonth, currentDay, 16, 00) // Market Close

// Session Ranges (Initialize to the first bar values)
var float londonHigh = high
var float londonLow = low
var float nyHigh = high
var float nyLow = low
var float asiaHigh = high
var float asiaLow = low

// Update Highs & Lows for Each Session
if (time >= sessionLondon and time < sessionNYOpen)
    londonHigh := math.max(londonHigh, high)
    londonLow := math.min(londonLow, low)

if (time >= sessionNYOpen and time < sessionEnd)
    nyHigh := math.max(nyHigh, high)
    nyLow := math.min(nyLow, low)

if (time >= sessionAsia and time < sessionLondon)
    asiaHigh := math.max(asiaHigh, high)
    asiaLow := math.min(asiaLow, low)

// New York Judas Swing (Temporary Rally)
judasSwing = high >= londonHigh and time >= sessionNYOpen and time < sessionEnd

// Short Entry in NY Kill Zone
shortEntry = judasSwing and close < open
stopLoss = high + 10 * syminfo.mintick
profitTarget = low - 20 * syminfo.mintick

if shortEntry
    strategy.entry("Short", strategy.short)
    strategy.exit("Take Profit", from_entry="Short", limit=profitTarget, stop=stopLoss)

// London Close Buy Setup
londonCloseBuy = time >= timestamp(currentYear, currentMonth, currentDay, 10, 30) and time <= timestamp(currentYear, currentMonth, currentDay, 13, 00) and close < londonLow
if londonCloseBuy
    strategy.entry("Buy", strategy.long)
    strategy.exit("Take Profit Buy", from_entry="Buy", limit=close + 20 * syminfo.mintick, stop=low - 10 * syminfo.mintick)

// Asia Open Sell Setup
asiaSell = time >= sessionAsia and time < sessionLondon and close > asiaHigh
if asiaSell
    strategy.entry("Asia Short", strategy.short)
    strategy.exit("Asia Profit", from_entry="Asia Short", limit=close - 15 * syminfo.mintick, stop=high + 10 * syminfo.mintick)

// Plot High/Low of Sessions
plot(londonHigh, color=color.blue, title="London High")
plot(londonLow, color=color.blue, title="London Low")
plot(nyHigh, color=color.red, title="NY High")
plot(nyLow, color=color.red, title="NY Low")
plot(asiaHigh, color=color.orange, title="Asia High")
plot(asiaLow, color=color.orange, title="Asia Low")

```

> Detail

https://www.fmz.com/strategy/488283

> Last Modified

2025-03-26 15:40:23
