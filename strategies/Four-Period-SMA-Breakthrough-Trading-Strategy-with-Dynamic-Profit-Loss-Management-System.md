
> Name

Four-Period-SMA-Breakthrough-Trading-Strategy-with-Dynamic-Profit-Loss-Management-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/199a69c7a17b732cecb.png)


#### Overview
This is a trading strategy system based on a four-period simple moving average, integrated with dynamic stop-loss and take-profit management mechanisms. The strategy captures market trend turning points by monitoring price crossovers with short-term moving averages and implements percentage-based stop-loss and take-profit levels for risk management. The core strength lies in utilizing the quick response characteristics of short-period moving averages, combined with strict money management rules to achieve stable trading results.

#### Strategy Principles
The strategy operates on the following core logic: First, it calculates a 4-period Simple Moving Average (SMA) as the primary indicator. When price crosses above the SMA, the system recognizes it as a bullish signal and enters a long position; when price crosses below the SMA, it identifies a bearish signal and enters a short position. Each trade is set with dynamic take-profit and stop-loss points based on the entry price, with default values of 2% for take-profit and 1% for stop-loss. This setup ensures a 2:1 reward-to-risk ratio, adhering to professional money management principles.

#### Strategy Advantages
1. Quick Response: Using a 4-period short-term moving average enables rapid capture of market movements, suitable for short-term trading.
2. Strict Risk Control: Integrated dynamic stop-loss and take-profit mechanisms provide clear exit points for each trade.
3. Simple Logic: Uses classic moving average crossover method, easy to understand and execute.
4. Adjustable Parameters: Profit and loss percentages can be flexibly adjusted for different market characteristics.
5. Bilateral Trading: Supports both long and short operations, maximizing market opportunities.

#### Strategy Risks
1. Consolidation Market Risk: Prone to false signals in sideways markets, leading to frequent trading.
2. Slippage Risk: Due to short-period moving average usage, high trading frequency may result in significant slippage losses.
3. Systemic Risk: Stop-losses may not execute timely during extreme market volatility.
4. Parameter Sensitivity: Strategy performance is highly sensitive to parameter settings, requiring continuous optimization.

#### Strategy Optimization Directions
1. Add Trend Filter: Incorporate longer-period moving averages as trend filters to reduce false signals in consolidating markets.
2. Optimize Stop Levels: Dynamically adjust profit and loss ratios based on market volatility.
3. Include Volume Indicators: Integrate volume as a supplementary indicator to improve entry signal reliability.
4. Implement Time Filters: Add trading session filters to avoid operations during unsuitable trading periods.

#### Summary
This is a well-structured quantitative trading strategy with clear logic. It captures market momentum through short-term moving averages, supplemented by strict risk control mechanisms, suitable for traders seeking stable returns. While there is room for optimization, the strategy's basic framework offers good scalability, and through continuous improvement and adjustment, it has the potential to achieve better trading results.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-28 00:00:00
period: 2d
basePeriod: 2d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("4SMA Strategy with Targets and Stop Loss", overlay=true)

// Input parameters for SMA
smaLength = input.int(4, title="SMA Length", minval=1)

// Input parameters for stop loss and take profit
takeProfitPercent = input.float(2.0, title="Take Profit (%)", step=0.1)  // Default: 2%
stopLossPercent = input.float(1.0, title="Stop Loss (%)", step=0.1)  // Default: 1%

// Calculate 4-period SMA
sma = ta.sma(close, smaLength)

// Plot SMA
plot(sma, color=color.blue, title="4SMA Line")

// Entry Conditions
longCondition = ta.crossover(close, sma)  // Price crosses above SMA (bullish signal)
shortCondition = ta.crossunder(close, sma)  // Price crosses below SMA (bearish signal)

// Strategy Logic
if (longCondition)
    strategy.entry("Long", strategy.long)  // Enter long position

if (shortCondition)
    strategy.entry("Short", strategy.short)  // Enter short position

// Calculate Take Profit and Stop Loss
longTakeProfit = strategy.position_avg_price * (1 + takeProfitPercent / 100)  // TP for long
longStopLoss = strategy.position_avg_price * (1 - stopLossPercent / 100)      // SL for long

shortTakeProfit = strategy.position_avg_price * (1 - takeProfitPercent / 100) // TP for short
shortStopLoss = strategy.position_avg_price * (1 + stopLossPercent / 100)     // SL for short

// Exit for Long
if (strategy.position_size > 0)  // If in a long position
    strategy.exit("Long TP/SL", from_entry="Long", limit=longTakeProfit, stop=longStopLoss)

// Exit for Short
if (strategy.position_size < 0)  // If in a short position
    strategy.exit("Short TP/SL", from_entry="Short", limit=shortTakeProfit, stop=shortStopLoss)

```

> Detail

https://www.fmz.com/strategy/473401

> Last Modified

2024-11-29 16:44:42
