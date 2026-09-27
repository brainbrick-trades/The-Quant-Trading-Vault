
> Name

Automated-Quantitative-Trading-System-with-Dual-EMA-Crossover-and-Risk-Management

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/cd6f787cb75ceefc36.png)


#### Overview
This strategy is an automated trading system based on dual moving average crossover theory with integrated risk management functionality. The core strategy utilizes 21-period and 50-period Exponential Moving Averages (EMA) as signal indicators, automatically executing trades based on crossover points while incorporating Stop Loss and Take Profit mechanisms for risk control.

#### Strategy Principles
The core logic is based on the classic moving average crossover theory in technical analysis. The system generates a bullish signal and enters a long position when the short-term (21-period) EMA crosses above the long-term (50-period) EMA, and conversely, generates a bearish signal and enters a short position when the short-term EMA crosses below the long-term EMA. Each trade signal automatically sets stop loss and take profit levels, with default settings of 40 ticks for stop loss and 80 ticks for take profit. This design ensures a 1:2 risk-reward ratio, adhering to professional trading management principles.

#### Strategy Advantages
1. High Automation: The system operates fully automatically, from signal detection to trade execution and risk management
2. Comprehensive Risk Management: Each trade has clear stop loss and take profit levels for effective risk control
3. Adjustable Parameters: Stop loss and take profit levels can be flexibly adjusted for different market conditions
4. Clear Visual Feedback: The system marks buy/sell signals with arrows and displays stop loss/take profit levels with dotted lines
5. Simple Strategy Logic: Uses classic technical indicators, easy to understand and maintain

#### Strategy Risks
1. Choppy Market Risk: May generate frequent false signals in range-bound markets
2. Slippage Risk: Actual execution prices may deviate from signal prices during high volatility
3. Trend Reversal Risk: Fixed stop loss levels may be inadequate during sudden market reversals
4. Parameter Optimization Risk: Over-optimization may lead to overfitting, affecting real-world performance

#### Strategy Optimization Directions
1. Add Trend Filters: Incorporate additional trend identification indicators like ADX or trend strength index to filter false signals
2. Dynamic Stop Loss Mechanism: Automatically adjust stop loss and take profit levels based on market volatility
3. Add Time Filters: Avoid trading during high-volatility periods like major news releases
4. Implement Position Sizing: Automatically adjust position sizes based on market volatility and account risk
5. Enhance Signal Confirmation: Add volume and other auxiliary indicators to improve signal reliability

#### Summary
This is a well-designed automated trading strategy with clear logic. By combining moving average crossover signals with strict risk management, the strategy provides a reliable technical framework for capturing market trends while ensuring trading safety. While there is room for optimization, the strategy's foundation is complete and suitable as a base module for further development and refinement in quantitative trading systems.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-10-01 00:00:00
end: 2024-10-31 23:59:59
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("EMA Crossover Strategy with SL & TP", overlay=true, default_qty_type=strategy.percent_of_equity)

// Input settings for SL and TP (ticks)
slTicks = input.int(40, title="Stop Loss (ticks)", minval=1)
tpTicks = input.int(80, title="Take Profit (ticks)", minval=1)

// Define EMA periods
ema21 = ta.ema(close, 21)
ema50 = ta.ema(close, 50)

// Detect crossovers
bullishCross = ta.crossover(ema21, ema50)
bearishCross = ta.crossunder(ema21, ema50)

// Plot the EMAs
plot(ema21, color=color.green, linewidth=2, title="EMA 21")
plot(ema50, color=color.red, linewidth=2, title="EMA 50")

// Calculate tick size in points
var float tickSize = syminfo.mintick

// Calculate stop loss and take profit prices for long and short positions
longSL = close - slTicks * tickSize
longTP = close + tpTicks * tickSize

shortSL = close + slTicks * tickSize
shortTP = close - tpTicks * tickSize

// Execute trades on crossover signals
if (bullishCross)
    strategy.entry("Long", strategy.long)
    strategy.exit("Exit Long", "Long", stop=longSL, limit=longTP)

if (bearishCross)
    strategy.entry("Short", strategy.short)
    strategy.exit("Exit Short", "Short", stop=shortSL, limit=shortTP)

// Plot arrows on crossovers
plotshape(series=bullishCross, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY", size=size.small)
plotshape(series=bearishCross, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL", size=size.small)

// Optional: Background coloring
bgcolor(bullishCross ? color.new(color.green, 90) : na, title="Bullish Background")
bgcolor(bearishCross ? color.new(color.red, 90) : na, title="Bearish Background")

```

> Detail

https://www.fmz.com/strategy/473324

> Last Modified

2024-11-29 11:20:40
