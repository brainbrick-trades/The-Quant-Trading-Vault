
> Name

RSI-Dynamic-Range-Reversal-Quantitative-Strategy-with-Volatility-Optimization-Model

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/e503c30545894d9cba.png)


#### Overview
This strategy is a dynamic range reversal trading system based on the RSI indicator, capturing market turning points through adjustable overbought/oversold zones combined with convergence/divergence sensitivity parameters. The strategy employs a fixed number of contracts for trading and operates within a specific backtesting timeframe. The core of this model lies in identifying market overbought and oversold conditions through dynamic RSI changes and executing reversal trades at appropriate timing.

#### Strategy Principles
The strategy utilizes a 14-period RSI as its core indicator, setting 80 and 30 as overbought and oversold benchmark levels. By introducing a convergence/divergence sensitivity parameter (set at 3.0), it adds dynamic adjustment capability to the traditional RSI strategy. Long positions are established when RSI breaks above the overbought level and closed when RSI falls below the oversold level. Similarly, long positions are established when RSI falls below the oversold level and closed when RSI breaks above the overbought level. Each trade uses a fixed 10 contracts to ensure stability in capital utilization.

#### Strategy Advantages
1. Dynamic Range Adjustment: Achieves dynamic adjustment of overbought/oversold zones through convergence/divergence parameters
2. Clear Risk Control: Uses fixed contract quantity for trading, facilitating capital management
3. Time Range Limitation: Avoids trading outside target periods through specific backtesting timeframe settings
4. Signal Clarity: Uses RSI crossover signals as trading triggers, reducing false signals
5. Visualization Support: Displays RSI trends and key levels through charts for monitoring and analysis

#### Strategy Risks
1. Choppy Market Risk: May result in frequent trading in sideways markets, increasing transaction costs
2. Trend Continuation Risk: Reversal signals might lead to premature position closure in strong trends
3. Fixed Contract Risk: Doesn't consider market volatility changes, potentially over-risking in high volatility periods
4. Parameter Sensitivity: Strategy performance heavily depends on RSI period and overbought/oversold level settings
5. Time Dependence: Strategy effectiveness may be limited to specific backtesting periods

#### Strategy Optimization Directions
1. Implement Volatility Adaptation: Suggest dynamically adjusting contract quantity based on market volatility
2. Add Trend Filters: Combine other technical indicators to judge market trends, avoiding reversals in strong trends
3. Optimize Signal Confirmation: Can add volume and other auxiliary indicators for signal confirmation
4. Dynamic Time Periods: Automatically adjust RSI calculation periods based on different market phases
5. Stop Loss Mechanism: Add dynamic stop losses to control single trade risk

#### Summary
This is a dynamic range reversal strategy based on the RSI indicator, achieving a relatively complete trading system through flexible parameter settings and clear trading rules. The strategy's main advantages lie in its dynamic adjustment capability and clear risk control, while attention needs to be paid to potential risks in choppy and trending markets. Through optimization measures such as volatility adjustment and trend filtering, the strategy has room for further improvement. Overall, this is a practical quantitative trading strategy framework suitable for in-depth research and practical verification.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-11 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("RSI Options Strategy", overlay=true)

// RSI settings
rsiLength = input(14, title="RSI Length")
rsiOverbought = input(80, title="Overbought Level")
rsiOversold = input(30, title="Oversold Level")
rsiSource = input(close, title="RSI Source")
rsi = ta.rsi(rsiSource, rsiLength)

// Convergence/Divergence Input
convergenceLevel = input(3.0, title="Convergence/Divergence Sensitivity")

// Order size (5 contracts)
contracts = 10

// Date Range for Backtesting
startDate = timestamp("2024-09-10 00:00")
endDate = timestamp("2024-11-09 23:59")

// Limit trades to the backtesting period
inDateRange = true

// RSI buy/sell conditions with convergence/divergence sensitivity
buySignalOverbought = ta.crossover(rsi, rsiOverbought - convergenceLevel)
sellSignalOversold = ta.crossunder(rsi, rsiOversold + convergenceLevel)
buySignalOversold = ta.crossunder(rsi, rsiOversold - convergenceLevel)
sellSignalOverbought = ta.crossover(rsi, rsiOverbought + convergenceLevel)

// Execute trades only within the specified date range
if (inDateRange)
    // Buy when RSI crosses above 80 (overbought)
    if (buySignalOverbought)
        strategy.entry("Buy Overbought", strategy.long, qty=contracts)
    
    // Sell when RSI crosses below 30 (oversold)
    if (sellSignalOversold)
        strategy.close("Buy Overbought")

    // Buy when RSI crosses below 30 (oversold)
    if (buySignalOversold)
        strategy.entry("Buy Oversold", strategy.long, qty=contracts)
    
    // Sell when RSI crosses above 80 (overbought)
    if (sellSignalOverbought)
        strategy.close("Buy Oversold")

// Plot the RSI for visualization
plot(rsi, color=color.blue, title="RSI")
hline(rsiOverbought, "Overbought", color=color.red)
hline(rsiOversold, "Oversold", color=color.green)

 




```

> Detail

https://www.fmz.com/strategy/471704

> Last Modified

2024-11-12 15:55:34
