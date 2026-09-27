
> Name

Adaptive-Trend-Following-with-Dynamic-Risk-Control-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/13b8e75ecdf100dd585.png)


#### Overview
This strategy is a short-term trading system that combines multiple technical indicators, primarily based on the Parabolic SAR (PSAR) as the core signal generator, while incorporating moving averages and momentum indicators for trade filtering, along with a combination of dynamic stop-loss and fixed take-profit risk management methods. The strategy is designed to consider market trends and volatility, making it suitable for short-term trading in volatile market conditions.

#### Strategy Principles
The strategy uses the PSAR indicator as its primary trend determination tool, generating trading signals when price crosses the PSAR. To enhance signal reliability, the following filters are added:
1. 50-period Exponential Moving Average (EMA50) as a trend filter to ensure trade direction aligns with medium-term trends
2. Relative Strength Index (RSI) to filter out ranging markets, requiring RSI>40 for long positions and RSI<60 for short positions
3. Average True Range (ATR) for dynamic stop-loss calculation, providing more flexible risk control
4. Fixed 0.7% take-profit target to secure gains promptly
5. Position check mechanism to avoid duplicate entries

#### Strategy Advantages
1. Comprehensive signal system: Combines trend following and momentum indicators for more reliable trading signals
2. Flexible risk control: Dynamic stop-loss adapts to market volatility
3. False breakout prevention: Multiple filtering conditions effectively reduce the impact of false signals
4. Clear profit targets: Fixed take-profit ratio helps control holding time and improve capital efficiency
5. Clear trading logic: Well-defined component responsibilities facilitate subsequent optimization and adjustment

#### Strategy Risks
1. Over-filtering risk: Multiple conditions may cause missed trading opportunities
2. Fixed take-profit limitations: 0.7% fixed take-profit may exit strong trends too early
3. Parameter sensitivity: PSAR, EMA, RSI parameter settings significantly impact strategy performance
4. Market environment dependence: May underperform in low volatility or highly volatile markets
5. Slippage impact: Frequent trading may lead to higher transaction costs

#### Strategy Optimization Directions
1. Dynamic take-profit mechanism: Adjust profit targets based on market volatility
2. Position management optimization: Introduce volatility-based dynamic position sizing system
3. Market environment recognition: Add market state identification module to adjust strategy parameters accordingly
4. Indicator parameter optimization: Implement adaptive parameter adjustment mechanism
5. Transaction cost control: Optimize entry/exit frequency to reduce trading costs

#### Summary
The strategy builds a complete trading system by combining multiple technical indicators, with solid considerations in trend identification, risk control, and trade execution. Its core strengths lie in its flexible risk control mechanism and comprehensive signal system, while attention needs to be paid to parameter optimization and market adaptability. Through continuous optimization and improvement, the strategy has the potential to maintain stable performance across different market conditions.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-20 00:00:00
end: 2025-02-17 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("Nicole 100%", overlay=true)

// ? Settings Parabolic SAR Parameter
start = input.float(0.02, "Start AF")
increment = input.float(0.02, "Acceleration factor")
maximum = input.float(0.2, "Max. AF")

// ? Calculate Parabolic SAR
SAR = ta.sar(start, increment, maximum)

// ? ATR Calculate (for dynamic stop loss))
atrLength = input.int(14, "ATR Calculation cycle")
atrMultiplier = input.float(1.3, "ATR Coefficient")  // 2times ATR As Stop-Loss Range
ATR = ta.atr(atrLength)

// ? Fixed 0.5% Take profit calculation
takeProfitPercent = 0.007  // 0.7% Fixed take profit
takeProfitLong = close * (1 + takeProfitPercent)  // Take Profit on Buy
takeProfitShort = close * (1 - takeProfitPercent) // Take Profit on Sell

// ? **50 EMA Filter**
ema50 = ta.ema(close, 50)

// ? **RSI Filter (to prevent entering during oscillation))**
rsiLength = input.int(14, "RSI Cycle")
rsi = ta.rsi(close, rsiLength)
longFilter = rsi > 40  // Only go long when RSI > 31
shortFilter = rsi < 60 // Only go short when RSI < 69

// ? **Check if there is already a position**
isFlat = strategy.position_size == 0  // **Only when there is no position, a new order can be opened**

// ? **Bull Entry Conditions**
longCondition = ta.crossover(close, SAR) and close > ema50 and longFilter and isFlat  

// ? **Bear Entry Conditions**
shortCondition = ta.crossunder(close, SAR) and close < ema50 and shortFilter and isFlat  

// ? **Entry strategy**
if (longCondition)
    strategy.entry("B", strategy.long, comment="B")

if (shortCondition)
    strategy.entry("S", strategy.short, comment="S")

// ? **take profit & Stop loss**
stopLossLong = close - (ATR * atrMultiplier)  // Long position ATR stop loss
stopLossShort = close + (ATR * atrMultiplier) // Short position ATR stop loss

strategy.exit("Exit Long", from_entry="B", stop=stopLossLong, limit=takeProfitLong, comment="TP Long")
strategy.exit("Exit Short", from_entry="S", stop=stopLossShort, limit=takeProfitShort, comment="TP Short")

// ? **Mark Entry and Exit Points**
plotshape(series=longCondition, location=location.belowbar, style=shape.triangleup, size=size.small, title="B")
plotshape(series=shortCondition, location=location.abovebar, style=shape.triangledown, size=size.small, title="S")

// ? **Draw 50 EMA**
plot(ema50, color=color.blue, title="50 EMA")

```

> Detail

https://www.fmz.com/strategy/482600

> Last Modified

2025-02-19 11:26:56
