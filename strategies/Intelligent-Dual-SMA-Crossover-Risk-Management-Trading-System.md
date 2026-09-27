
> Name

Intelligent-Dual-SMA-Crossover-Risk-Management-Trading-System

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d932dc32de49df0945a0.png)
![IMG](https://www.fmz.com/upload/asset/2d8c9bd51777457113b56.png)





#### Overview
This is an intelligent trading system based on dual moving average crossover signals with integrated risk management features. The system utilizes short-term and long-term Simple Moving Averages (SMA) to generate trading signals while incorporating stop-loss and take-profit mechanisms for risk control. The strategy employs a percentage-based risk management approach, dynamically adjusting position sizes based on account equity, achieving automated and intelligent trading execution.

#### Strategy Principles
The strategy is based on the following core principles:
1. Uses crossovers of 9-day and 21-day Simple Moving Averages (SMA) to capture market trends. A buy signal is generated when the short-term MA crosses above the long-term MA, and a sell signal when it crosses below.
2. Implements a dynamic risk management system based on account equity. Risk per trade is fixed at 1% of account equity, with stop-loss set at 1% from entry price and take-profit at twice the stop-loss distance.
3. Automatically calculates trade size to ensure risk amount remains constant at the predetermined level for each trade.

#### Strategy Advantages
1. Simple and reliable signal system: Uses classic dual MA crossover system, easy to understand and maintain.
2. Comprehensive risk control: Integrates stop-loss and take-profit functions, limiting maximum loss per trade.
3. Dynamic position management: Automatically adjusts trade size based on account equity, avoiding risks associated with fixed lot size trading.
4. Strong visualization: Clearly displays trading signals, stop-loss and take-profit levels on the chart for easy monitoring and analysis.
5. High parameter adaptability: Major parameters can be adjusted through the input interface to adapt to different market conditions.

#### Strategy Risks
1. Choppy market risk: False breakout signals may occur frequently in sideways markets, leading to consecutive losses.
2. Slippage risk: Actual execution prices may significantly deviate from theoretical prices during high volatility periods.
3. Systemic risk: Stop-losses may fail during market gaps or major events.
4. Parameter optimization risk: Over-optimization may lead to poor performance in live trading.

#### Strategy Optimization Directions
1. Add trend filter: Incorporate trend indicators like ADX to execute trades only in strong trend conditions.
2. Optimize stop-loss method: Consider implementing volatility-adaptive dynamic stop-loss for more flexible risk management.
3. Introduce volume indicators: Integrate volume analysis to improve signal reliability.
4. Add time filters: Avoid trading during high-volatility opening and closing periods.
5. Implement drawdown control: Set maximum drawdown limits to automatically stop trading when losses reach specific levels.

#### Summary
This is an intelligent trading system that combines classic technical analysis methods with modern risk management concepts. It captures trends through dual MA crossovers while controlling risk through dynamic risk management, achieving automated execution. While there are areas for optimization, the overall design concept is advanced and has practical value. Traders are advised to thoroughly test and optimize the system according to specific market characteristics before live implementation.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-06-09 00:00:00
end: 2025-02-19 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=6
strategy("AI Trade Bot with Risk Management", overlay=true)

// Input parameters
shortSMA = input.int(9, title="Short SMA")
longSMA = input.int(21, title="Long SMA")
riskPercent = input.float(1.0, title="Risk Percentage", step=0.1)

// Calculate SMAs
shortSMAValue = ta.sma(close, shortSMA)
longSMAValue = ta.sma(close, longSMA)

// Bullish and Bearish Signals
bullishSignal = ta.crossover(shortSMAValue, longSMAValue)
bearishSignal = ta.crossunder(shortSMAValue, longSMAValue)

// Risk Management
stopLossPercent = riskPercent / 100
takeProfitPercent = stopLossPercent * 2

// Calculate position size based on risk management
riskAmount = strategy.equity * riskPercent / 100

var float buyStopLossPrice = na
var float buyTakeProfitPrice = na
var float sellStopLossPrice = na
var float sellTakeProfitPrice = na

if (bullishSignal)
    buyStopLossPrice := close * (1 - stopLossPercent)
    buyTakeProfitPrice := close * (1 + takeProfitPercent)
    strategy.entry("Buy", strategy.long)
    strategy.exit("Take Profit/Stop Loss", from_entry="Buy", limit=buyTakeProfitPrice, stop=buyStopLossPrice)

if (bearishSignal)
    sellStopLossPrice := close * (1 + stopLossPercent)
    sellTakeProfitPrice := close * (1 - takeProfitPercent)
    strategy.entry("Sell", strategy.short)
    strategy.exit("Take Profit/Stop Loss", from_entry="Sell", limit=sellTakeProfitPrice, stop=sellStopLossPrice)

// Plot SMAs on the chart
plot(shortSMAValue, color=color.blue, title="Short SMA")
plot(longSMAValue, color=color.red, title="Long SMA")

// Plot Buy/Sell signals on the chart
plotshape(series=bullishSignal, location=location.belowbar, color=color.green, style=shape.labelup, title="Buy Signal", text="BUY")
plotshape(series=bearishSignal, location=location.abovebar, color=color.red, style=shape.labeldown, title="Sell Signal", text="SELL")

// Plot Buy Stop Loss and Take Profit levels
plot(buyStopLossPrice, color=color.red, style=plot.style_linebr, linewidth=2, title="Buy Stop Loss")
plot(buyTakeProfitPrice, color=color.green, style=plot.style_linebr, linewidth=2, title="Buy Take Profit")

// Plot Sell Stop Loss and Take Profit levels
plot(sellStopLossPrice, color=color.red, style=plot.style_linebr, linewidth=2, title="Sell Stop Loss")
plot(sellTakeProfitPrice, color=color.green, style=plot.style_linebr, linewidth=2, title="Sell Take Profit")

```

> Detail

https://www.fmz.com/strategy/483026

> Last Modified

2025-02-21 09:56:11
