
> Name

Advanced-Quantitative-Trading-Strategy-Automated-Execution-System-Based-on-Intraday-Momentum-and-Risk-Management

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8ff934925c91b8951b6.png)
![IMG](https://www.fmz.com/upload/asset/2d81d377bb988faddc930.png)




#### Overview
This is a fully automated trading strategy based on intraday momentum, incorporating strict risk management and precise position sizing systems. The strategy operates primarily during London trading hours, seeking trading opportunities through momentum change identification and Doji pattern exclusion, while implementing daily take-profit rules for risk control. The strategy employs dynamic position management, automatically adjusting trading size based on account equity to optimize capital utilization.

#### Strategy Principles
The core logic is built on several key components. First, trading is restricted to London hours (excluding 0:00 and after 19:00) to ensure adequate market liquidity. Entry signals are based on price momentum breakouts, specifically requiring the current candle's high to break above the previous candle's high (for longs) or the low to break below the previous candle's low (for shorts), while maintaining directional consistency. To avoid false breakouts, the strategy explicitly excludes Doji candles. The strategy also implements a daily take-profit rule, ceasing new positions once the target profit is achieved.

#### Strategy Advantages
1. Comprehensive Risk Management: Includes fixed stop-loss/take-profit, daily profit targets, and dynamic position sizing
2. Strong Adaptability: Trading size automatically adjusts based on account equity, suitable for different capital scales
3. Liquidity Assurance: Strict trading execution during London hours to avoid low liquidity risks
4. False Signal Filtering: Reduces losses from false breakouts by excluding Doji patterns and consecutive signals
5. Clear Execution Logic: Well-defined entry and exit conditions for easy monitoring and optimization

#### Strategy Risks
1. Market Volatility Risk: Fixed stop-loss may lack flexibility during high volatility periods
2. Price Slippage Risk: May face significant slippage during rapid market movements
3. Trend Dependency: Strategy may generate false signals in ranging markets
4. Parameter Sensitivity: Strategy performance heavily influenced by stop-loss/take-profit settings
Solutions include: implementing dynamic stop-loss mechanisms, adding volatility filters, and incorporating trend confirmation indicators.

#### Strategy Optimization Directions
1. Introduce Adaptive Stop-Loss: Dynamically adjust stop-loss ranges based on ATR or volatility
2. Add Market Environment Filtering: Incorporate trend strength indicators to extend holding periods in clear trends
3. Optimize Signal Confirmation: Enhance signal reliability by integrating volume and other technical indicators
4. Improve Capital Management: Introduce compound risk management systems considering drawdown control
5. Enhance Market Microstructure Analysis: Integrate order flow data for more precise entries

#### Summary
The strategy builds a comprehensive trading framework by combining momentum breakouts, strict risk management, and automated execution systems. Its main strengths lie in its comprehensive risk control system and adaptive design, though improvements in market environment recognition and signal filtering are needed. Through continuous improvement and parameter optimization, the strategy shows potential for maintaining stable performance across different market conditions.




> Source (PineScript)

``` pinescript
/*backtest
start: 2025-01-21 00:00:00
end: 2025-02-08 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=6
strategy("Trading Strategy for XAUUSD (Gold) – Automated Execution Plan", overlay=true, initial_capital=10000, currency=currency.USD)

//────────────────────────────
// 1. RISK MANAGEMENT & POSITION SIZING
//────────────────────────────
// Configurable inputs for Stop Loss and Take Profit
sl = input.float(title="Stop Loss ($)", defval=5, step=0.1)
tp = input.float(title="Take Profit ($)", defval=15, step=0.1)

// Volume: 0.01 lots per $100 of equity → lotSize = equity / 10000
lotSize = strategy.equity / strategy.initial_capital

//────────────────────────────
// 2. TRADING HOURS (London Time)
//────────────────────────────
// Get the current bar's timestamp in London time.
londonTime   = time(timeframe.period, "", "Europe/London")
londonHour   = hour(londonTime)
tradingAllowed = (londonHour != 0) and (londonHour < 19)

//────────────────────────────
// 3. DOJI CANDLE DEFINITION
//────────────────────────────
// A candle is considered a doji if the sum of its upper and lower shadows is greater than its body.
upperShadow = high - math.max(open, close)
lowerShadow = math.min(open, close) - low
bodySize    = math.abs(close - open)
isDoji      = (upperShadow + lowerShadow) > bodySize

//────────────────────────────
// 4. ENTRY CONDITIONS
//────────────────────────────
// Buy Signal:
//   • Current candle's high > previous candle's high.
//   • Current candle's low is not below previous candle's low.
//   • Bullish candle (close > open) and not a doji.
//   • Skip if previous candle already qualified.
buyRaw    = (high > high[1]) and (low >= low[1]) and (close > open) and (not isDoji)
buySignal = buyRaw and not (buyRaw[1] ? true : false)

// Sell Signal:
//   • Current candle's low < previous candle's low.
//   • Current candle's high is not above previous candle's high.
//   • Bearish candle (close < open) and not a doji.
//   • Skip if previous candle already qualified.
sellRaw    = (low < low[1]) and (high <= high[1]) and (close < open) and (not isDoji)
sellSignal = sellRaw and not (sellRaw[1] ? true : false)

//────────────────────────────
// 5. DAILY TAKE PROFIT (TP) RULE
//────────────────────────────
// Create a day-string (year-month-day) using London time.
// This flag will block new trades for the rest of the day if a TP is hit.
var string lastDay = ""
currentDay = str.tostring(year(londonTime)) + "-" + str.tostring(month(londonTime)) + "-" + str.tostring(dayofmonth(londonTime))
var bool dailyTPHit = false
if lastDay != currentDay
    dailyTPHit := false
    lastDay := currentDay

//────────────────────────────
// 6. TRACK TRADE ENTRY & EXIT FOR TP DETECTION
//────────────────────────────
// We record the TP target when a new trade is entered.
// Then, when a trade closes, if the bar's high (for long) or low (for short) reached the TP target,
// we assume the TP was hit and block new trades for the day.
var float currentTP = na
var int currentTradeType = 0   // 1 for long, -1 for short

// Detect a new trade entry (transition from no position to a position).
tradeEntered = (strategy.position_size != 0 and strategy.position_size[1] == 0)
if tradeEntered
    if strategy.position_size > 0
        currentTP := strategy.position_avg_price + tp
        currentTradeType := 1
    else if strategy.position_size < 0
        currentTP := strategy.position_avg_price - tp
        currentTradeType := -1

// Detect trade closure (transition from position to flat).
tradeClosed = (strategy.position_size == 0 and strategy.position_size[1] != 0)
if tradeClosed and not na(currentTP)
    // For a long trade, if the bar's high reached the TP target;
    // for a short trade, if the bar's low reached the TP target,
    // mark the daily TP flag.
    if (currentTradeType == 1 and high >= currentTP) or (currentTradeType == -1 and low <= currentTP)
        dailyTPHit := true
    currentTP := na
    currentTradeType := 0

//────────────────────────────
// 7. ORDER EXECUTION
//────────────────────────────
// Only open a new position if no position is open, trading is allowed, and daily TP rule is not active.
if (strategy.position_size == 0) and tradingAllowed and (not dailyTPHit)
    if buySignal
        strategy.entry("Long", strategy.long, qty=lotSize)
    if sellSignal
        strategy.entry("Short", strategy.short, qty=lotSize)

//────────────────────────────
// 8. EXIT ORDERS (Risk Management)
//────────────────────────────
// For long positions: SL = entry price - Stop Loss, TP = entry price + Take Profit.
// For short positions: SL = entry price + Stop Loss, TP = entry price - Take Profit.
if strategy.position_size > 0
    longSL = strategy.position_avg_price - sl
    longTP = strategy.position_avg_price + tp
    strategy.exit("Exit Long", from_entry="Long", stop=longSL, limit=longTP)
if strategy.position_size < 0
    shortSL = strategy.position_avg_price + sl
    shortTP = strategy.position_avg_price - tp
    strategy.exit("Exit Short", from_entry="Short", stop=shortSL, limit=shortTP)

//────────────────────────────
// 9. VISUALIZATION
//────────────────────────────
plotshape(buySignal and tradingAllowed and (not dailyTPHit) and (strategy.position_size == 0), title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="Buy")
plotshape(sellSignal and tradingAllowed and (not dailyTPHit) and (strategy.position_size == 0), title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="Sell")

```

> Detail

https://www.fmz.com/strategy/483119

> Last Modified

2025-02-27 16:57:06
