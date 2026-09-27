
> Name

Dynamic-Trend-Following-Multi-Indicator-Staged-Take-Profit-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/fed10a05a71b3d8d05.png)


#### Overview
This is a quantitative trading strategy that combines trend following and technical analysis. The strategy uses multiple technical indicators to confirm trading signals, employs a staged take-profit mechanism and dynamic position management system, aiming to capture major market trends while controlling risks. The strategy integrates multiple technical indicators including EMA, MACD, and RSI, identifying potential trading opportunities through indicator crossovers and divergences.

#### Strategy Principles
The core trading logic is based on the following key elements:
1. Entry signals use multiple technical indicator filters: EMA crossovers, MACD golden/death crosses, and RSI overbought/oversold indicators. Long entry requires fast EMA crossing above slow EMA, MACD golden cross, and RSI below 70; short entry requires fast EMA crossing below slow EMA, MACD death cross, and RSI above 30.
2. Risk control employs fixed percentage stop-loss at 5% from entry price.
3. Staged take-profit mechanism: first target at 8%, second target at 12%, with dynamic adjustment of the second target to adapt to market volatility.
4. Position management is dynamically calculated based on ATR, with maximum risk per trade at 5% and maximum position size not exceeding 40% of account equity.

#### Strategy Advantages
1. Multiple technical indicators cross-validation effectively filters false signals and improves trade quality.
2. Staged take-profit mechanism both locks in partial profits and maintains exposure to continued trends.
3. Dynamic position management system automatically adjusts trade size based on market volatility for effective risk control.
4. Comprehensive risk management system including fixed stop-loss, dynamic positioning, and maximum position limits ensures long-term strategy stability.
5. Clear strategy logic with adjustable parameters facilitates optimization for different market conditions.

#### Strategy Risks
1. May face frequent stop-losses in highly volatile markets, requiring parameter adjustment or trading suspension during high volatility periods.
2. Consecutive stop-losses possible in ranging markets, suggesting the need for range-bound market detection.
3. Multiple indicator filtering may miss some opportunities, potentially underperforming single-indicator strategies in strong trends.
4. Staged take-profit mechanism may not exit positions quickly enough in rapid reversals, requiring additional reversal signal detection.

#### Strategy Optimization Directions
1. Consider introducing volatility filtering mechanism to reduce position size or suspend trading during high volatility periods.
2. Add trend strength evaluation to adjust take-profit levels during strong trends for capturing more trend profits.
3. Optimize position management system by incorporating dynamic position adjustment based on risk-reward ratios.
4. Implement market state detection mechanism to use different parameter sets in different market conditions.
5. Consider adding volume indicators to improve trading signal reliability.

#### Summary
This strategy constructs a relatively complete trading system through the combination of multiple technical indicators, staged take-profit mechanisms, and dynamic position management. Its strengths lie in comprehensive risk control and high signal reliability, though it may miss some opportunities. Through continuous optimization and parameter adjustment, the strategy has the potential to maintain stable performance across different market conditions.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-10 00:00:00
end: 2025-02-08 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("Hang Strategy Aggressive", overlay=true, initial_capital=1000, currency=currency.USDT, default_qty_type=strategy.cash, default_qty_value=100)

// === Parameter Settings ===
fastLength = input.int(5, "FastEMALength")
slowLength = input.int(15, "SlowEMALength")
rsiLength = input.int(7, "RSILength")
atrPeriod = input.int(10, "ATRtimeframe")
leverageMultiple = input.float(3.0, "Leverage multiple", minval=1.0, step=0.5)

// === Take profit and stop loss parameters ===
stopLossPercent = input.float(5.0, "Stop Loss Percentage", minval=1.0, step=0.5)
firstTakeProfitPercent = input.float(8.0, "First take profit percentage", minval=1.0, step=0.5)
secondTakeProfitPercent = input.float(12.0, "Second take profit percentage", minval=1.0, step=0.5)
firstTakeProfitQtyPercent = input.float(50.0, "First take profit position percentage", minval=1.0, maxval=100.0, step=5.0)

// === Technical indicators ===
fastEMA = ta.ema(close, fastLength)
slowEMA = ta.ema(close, slowLength)
superFastEMA = ta.ema(close, 3)
rsi = ta.rsi(close, rsiLength)
atr = ta.atr(atrPeriod)

// === Trend judgment ===
[macdLine, signalLine, histLine] = ta.macd(close, 12, 26, 9)
macdCross = (macdLine > signalLine) and (macdLine[1] < signalLine[1])
macdCrossDown = (macdLine < signalLine) and (macdLine[1] > signalLine[1])

// === Trading signals ===
longCondition = (fastEMA > slowEMA) and macdCross and (rsi < 70)
shortCondition = (fastEMA < slowEMA) and macdCrossDown and (rsi > 30)

// === Close signal ===
exitLong = shortCondition or (fastEMA < slowEMA)
exitShort = longCondition or (fastEMA > slowEMA)

// === position management ===
maxRiskPerTrade = 0.05
basePosition = strategy.equity * maxRiskPerTrade
atrAmount = atr * close
riskPosition = basePosition / atrAmount * leverageMultiple
positionSize = math.min(riskPosition, strategy.equity * 0.4 / close)

// === Trading status variables ===
var isLong = false
var isShort = false
var partialTpTriggered = false
var float stopPrice = na
var float firstTpPrice = na
var float secondTpPrice = na
var float firstTpQty = na

// === Transaction Execution ===
// Long Entry
if (longCondition and not isLong and not isShort)
    strategy.entry("Many", strategy.long, qty=positionSize)
    isLong := true
    partialTpTriggered := false

// Short Entry
if (shortCondition and not isShort and not isLong)
    strategy.entry("Empty", strategy.short, qty=positionSize)
    isShort := true
    partialTpTriggered := false

// === Take profit and stop loss logic ===
if (strategy.position_size > 0)  // Long position
    stopPrice := strategy.position_avg_price * (1 - stopLossPercent/100)
    firstTpPrice := strategy.position_avg_price * (1 + firstTakeProfitPercent/100)
    // Only calculate the second take-profit price when the first take-profit is not triggered
    if not partialTpTriggered
        secondTpPrice := strategy.position_avg_price * (1 + secondTakeProfitPercent/100)
    
    if (close[1] <= stopPrice or low <= stopPrice)
        strategy.close_all("Long stop loss")
        isLong := false
        partialTpTriggered := false
    
    if (not partialTpTriggered and (close[1] >= firstTpPrice or high >= firstTpPrice))
        strategy.order("First long take profit", strategy.short, qty=firstTpQty)
        partialTpTriggered := true
        // Recalculate the second take-profit price here
        secondTpPrice := high * (1 + 0.04)  // Based on the current highest price, rise again4%
    
    if (close[1] >= secondTpPrice or high >= secondTpPrice)
        strategy.close_all("Second long take profit")
        isLong := false
        partialTpTriggered := false

if (strategy.position_size < 0)  // Short position
    stopPrice := strategy.position_avg_price * (1 + stopLossPercent/100)
    firstTpPrice := strategy.position_avg_price * (1 - firstTakeProfitPercent/100)
    // Only calculate the second take-profit price when the first take-profit is not triggered
    if not partialTpTriggered
        secondTpPrice := strategy.position_avg_price * (1 - secondTakeProfitPercent/100)
    
    if (close[1] >= stopPrice or high >= stopPrice)
        strategy.close_all("Short stop loss")
        isShort := false
        partialTpTriggered := false
    
    if (not partialTpTriggered and (close[1] <= firstTpPrice or low <= firstTpPrice))
        strategy.order("First short take profit", strategy.long, qty=firstTpQty)
        partialTpTriggered := true
        // Recalculate the second take-profit price here
        secondTpPrice := low * (1 - 0.04)  // Based on the current lowest price, fall again4%
    
    if (close[1] <= secondTpPrice or low <= secondTpPrice)
        strategy.close_all("Second short take profit")
        isShort := false
        partialTpTriggered := false

// === Other closing conditions ===
if (exitLong and isLong)
    strategy.close_all("Close long")
    isLong := false
    partialTpTriggered := false

if (exitShort and isShort)
    strategy.close_all("Close short")
    isShort := false
    partialTpTriggered := false

// === Drawing ===
plot(fastEMA, "FastEMA", color=color.blue)
plot(slowEMA, "SlowEMA", color=color.red)
plot(superFastEMA, "Super fastEMA", color=color.green)

// Draw Take Profit and Stop Loss Lines
plot(strategy.position_size != 0 ? strategy.position_avg_price : na, "Opening price", color=color.yellow)
plot(strategy.position_size != 0 ? stopPrice : na, "Stop loss line", color=color.red)
plot(strategy.position_size != 0 ? firstTpPrice : na, "First take profit line", color=color.green)
plot(strategy.position_size != 0 ? secondTpPrice : na, "Second take profit line", color=color.blue)
```

> Detail

https://www.fmz.com/strategy/481356

> Last Modified

2025-02-10 14:49:11
