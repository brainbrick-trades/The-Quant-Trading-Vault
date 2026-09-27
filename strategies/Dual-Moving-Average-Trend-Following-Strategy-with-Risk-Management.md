
> Name

Dual-Moving-Average-Trend-Following-Strategy-with-Risk-Management

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1bfc9d0f1ab2bac93ce.png)


#### Overview
This strategy is a trend-following trading system based on the crossover of 110-day and 200-day Exponential Moving Averages (EMA). It identifies market trends through the intersection of short-term and long-term EMAs, incorporating stop-loss and take-profit mechanisms for risk control. The system automatically executes long and short positions upon trend confirmation while continuously monitoring position risk.

#### Strategy Principle
The core logic relies on the continuity of price trends, using EMA110 and EMA200 crossovers to capture trend reversal signals. When the shorter-term moving average (EMA110) crosses above the longer-term moving average (EMA200), it signals an uptrend formation, triggering a long position. Conversely, when the shorter-term moving average crosses below the longer-term moving average, it signals a downtrend formation, triggering a short position. For risk management, the strategy sets a 1% stop-loss and 0.5% take-profit level for each position to protect profits and limit potential losses.

#### Strategy Advantages
1. Strong trend capture capability: Effectively filters short-term market noise through dual moving average crossovers
2. Comprehensive risk control: Integrated stop-loss and take-profit mechanisms effectively control single-trade risk
3. Rigorous execution logic: Automatically closes reverse positions before opening new ones, avoiding position overlap
4. Clear signal indication: Trade signals are clearly displayed in the top-right corner table
5. Reasonable parameter settings: 110-day and 200-day periods balance sensitivity and stability

#### Strategy Risks
1. Sideways market risk: Frequent trading in range-bound markets may lead to losses
2. Slippage risk: Significant slippage may occur during high market volatility
3. Trend reversal risk: Stop-losses may not trigger quickly enough during sudden trend reversals
4. Parameter optimization risk: Over-optimization may lead to strategy overfitting
5. Systemic risk: Exposure to systemic risks during extreme market conditions

#### Strategy Optimization Directions
1. Incorporate volume indicators: Confirm trend validity through volume analysis
2. Optimize stop-loss mechanism: Consider implementing trailing stops or ATR-based dynamic stops
3. Add trend filters: Integrate trend strength indicators to filter weak signals
4. Improve position management: Dynamically adjust position sizes based on trend strength
5. Implement drawdown control: Set maximum drawdown limits to pause trading when thresholds are reached

#### Summary
The strategy captures trends through moving average crossovers while managing risk through stop-loss and take-profit mechanisms, demonstrating sound design and logical rigor. Although it may underperform in ranging markets, the suggested optimizations can further enhance strategy stability and profitability. The strategy is suitable for medium to long-term investors seeking steady returns.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-18 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("EMA110/200 Cross with Stop-Loss and Take-Profit", overlay=true)

// DefinitionEMA110andEMA200
ema110 = ta.ema(close, 110)
ema200 = ta.ema(close, 250)

// DrawEMA
plot(ema110, color=color.blue, title="EMA110")
plot(ema200, color=color.red, title="EMA200")

// Calculate crossover signals
longCondition = ta.crossover(ema110, ema200)  // EMA110Break aboveEMA200,go long
shortCondition = ta.crossunder(ema110, ema200)  // EMA110Break belowEMA200,go short

// Set stop loss and take profit
stopLoss = 0.01  // stop loss1%
takeProfit = 0.005  // take profit0.5%

// Determine whether there is already a position
isLong = strategy.position_size > 0  // Is it currently a long position?
isShort = strategy.position_size < 0  // Is it currently a short position?

// Execution strategy: close short when going long, close long when going short
if (longCondition and not isLong)  // If the long conditions are met and there are currently no long positions
    if (isShort)  // If you are currently in a short position, close the position first
        strategy.close("Short")
    strategy.entry("Long", strategy.long)  // Execute Buy
    strategy.exit("Take Profit/Stop Loss", "Long", stop=close * (1 - stopLoss), limit=close * (1 + takeProfit))

if (shortCondition and not isShort)  // If the short selling conditions are met and there is currently no short position
    if (isLong)  // If you are currently in a long position, close the position first
        strategy.close("Long")
    strategy.entry("Short", strategy.short)  // Execute Sell
    strategy.exit("Take Profit/Stop Loss", "Short", stop=close * (1 + stopLoss), limit=close * (1 - takeProfit))

// Display signals in the table
var table myTable = table.new(position.top_right, 1, 1)
if (longCondition and not isLong)
    table.cell(myTable, 0, 0, "Buy Signal", text_color=color.green)
if (shortCondition and not isShort)
    table.cell(myTable, 0, 0, "Sell Signal", text_color=color.red)

```

> Detail

https://www.fmz.com/strategy/475597

> Last Modified

2024-12-20 14:30:29
