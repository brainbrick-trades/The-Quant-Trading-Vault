
> Name

Momentum-Enhanced-Simple-Moving-Average-and-RSI-Strategy-for-Trend-Following

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d7e723abaa25e8ec430e.png)
![IMG](https://www.fmz.com/upload/asset/2d9018845cc1c579be0c3.png)





#### Overview
This strategy is a trend-following trading system that combines Simple Moving Averages (SMA) with the Relative Strength Index (RSI). It identifies trend directions through crossovers of short-term and long-term moving averages, uses RSI for momentum confirmation, and seeks high-probability trading opportunities in the market. The strategy includes a comprehensive risk management module for effective control of trading risks.

#### Strategy Principles
The core logic is based on the combination of two technical indicators:
1. Dual MA System: Uses 8-period and 21-period simple moving averages to identify trend changes. Buy signals are generated when the short-term MA crosses above the long-term MA, and sell signals when it crosses below.
2. RSI Filter: Employs a 14-period RSI for momentum confirmation. Long positions are only executed when RSI is below 70, and short positions when RSI is above 30, avoiding trades in overextended areas.
3. Risk Control: Each trade includes a 1% stop loss and 2% take profit level to protect capital and secure profits.

#### Strategy Advantages
1. Indicator Synergy: Combines trend-following and momentum indicators for more accurate identification of market turning points.
2. Robust Risk Management: Built-in stop loss and take profit mechanisms effectively control risk.
3. Flexible Parameters: All key parameters can be optimized for different market conditions.
4. Wide Applicability: Can be applied across multiple markets and timeframes.
5. Clear Logic: Strategy rules are explicit, easy to understand and execute.

#### Strategy Risks
1. Choppy Market Risk: May generate frequent false signals in sideways markets.
2. Lag Risk: Moving averages have inherent lag, potentially missing some profit opportunities.
3. Parameter Sensitivity: May require parameter adjustments in different market environments.
4. Trend Dependency: Strategy performs best in strong trending markets but may underperform in other conditions.

#### Optimization Directions
1. Introduce market environment recognition mechanism for different parameter combinations.
2. Add volume indicators as confirmatory signals.
3. Optimize stop loss and take profit mechanisms, consider implementing dynamic stop loss.
4. Add trend strength filters to trade only in strong trending markets.
5. Develop adaptive parameter adjustment mechanisms to improve strategy adaptability.

#### Summary
This is a comprehensively structured trend-following strategy with clear logic. By combining SMA and RSI, it captures trends while avoiding trades in overextended areas. The built-in risk management ensures strategy stability. While there are some inherent limitations, the suggested optimization directions can further enhance strategy performance. This strategy is particularly suitable for traders seeking stable returns.




> Source (PineScript)

``` pinescript
/*backtest
start: 2025-02-16 00:00:00
end: 2025-02-23 00:00:00
period: 6m
basePeriod: 6m
exchanges: [{"eid":"Binance","currency":"SOL_USDT"}]
*/

//@version=6
strategy("WEN - SMA with RSI Strategy", overlay=true)

// Define input parameters
// SMA Inputs
shortLength = input(8, title="Short MA Length")
longLength = input(21, title="Long MA Length")

// RSI Inputs
rsiLength = input(14, title="RSI Length")
rsiOverbought = input(70, title="RSI Overbought")
rsiOversold = input(30, title="RSI Oversold")

// Calculate indicators
// Moving Averages
shortMA = ta.sma(close, shortLength)
longMA = ta.sma(close, longLength)

// RSI
rsi = ta.rsi(close, rsiLength)

// Plot indicators
plot(shortMA, title="Short MA", color=color.blue)
plot(longMA, title="Long MA", color=color.red)
// RSI is typically plotted in a separate panel in trading platforms

// Entry conditions with RSI confirmation
smaLongCondition = ta.crossover(shortMA, longMA)
smaShortCondition = ta.crossunder(shortMA, longMA)

rsiLongCondition = rsi < rsiOverbought  // Not overbought for long entry
rsiShortCondition = rsi > rsiOversold   // Not oversold for short entry

// Combined entry conditions
longCondition = smaLongCondition and rsiLongCondition
shortCondition = smaShortCondition and rsiShortCondition

// Execute trades
if (longCondition)
    strategy.entry("Long", strategy.long)
if (shortCondition)
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

// Set stop loss and take profit
stopLoss = input(1, title="Stop Loss (%)") / 100
takeProfit = input(2, title="Take Profit (%)") / 100

longStopLossPrice = strategy.position_avg_price * (1 - stopLoss)
longTakeProfitPrice = strategy.position_avg_price * (1 + takeProfit)
shortStopLossPrice = strategy.position_avg_price * (1 + stopLoss)
shortTakeProfitPrice = strategy.position_avg_price * (1 - takeProfit)

strategy.exit("Take Profit / Stop Loss", from_entry="Long", stop=longStopLossPrice, limit=longTakeProfitPrice)
strategy.exit("Take Profit / Stop Loss", from_entry="Short", stop=shortStopLossPrice, limit=shortTakeProfitPrice)
```

> Detail

https://www.fmz.com/strategy/483525

> Last Modified

2025-02-24 10:19:03
