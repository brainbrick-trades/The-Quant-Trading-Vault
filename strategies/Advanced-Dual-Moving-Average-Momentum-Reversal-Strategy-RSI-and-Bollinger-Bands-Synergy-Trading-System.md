
> Name

Advanced-Dual-Moving-Average-Momentum-Reversal-Strategy-RSI-and-Bollinger-Bands-Synergy-Trading-System

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d86c96aa078d628f4120.png)
![IMG](https://www.fmz.com/upload/asset/2d85b42120e639f4b7163.png)





#### Overview
This strategy is an advanced technical analysis trading system that combines the Relative Strength Index (RSI) and Bollinger Bands (BB). It seeks high-probability reversal trading opportunities in overbought and oversold market areas by synergistically using these two indicators. The strategy employs a 20-period moving average as the Bollinger Bands basis line, with 2 standard deviations for the upper and lower bands, while using a 14-period RSI for momentum analysis, generating trading signals when RSI breaks through 30/70 key levels and price touches the Bollinger Bands boundaries.

#### Strategy Principles
The core logic is built on the synergistic effect of two main technical indicators:
1. Bollinger Bands use a 20-period simple moving average as the middle band, with upper and lower bands at 2 standard deviations, identifying price volatility range.
2. RSI uses a 14-period setting, with 30 as oversold and 70 as overbought levels, determining market momentum status.
3. Long conditions require: RSI breaking above 30 and price touching or below the lower Bollinger Band.
4. Short conditions require: RSI breaking below 70 and price touching or above the upper Bollinger Band.
5. Exit conditions include: RSI breaking opposite extremes or price breaking the Bollinger Band middle line.

#### Strategy Advantages
1. Dual confirmation mechanism: Combining RSI and Bollinger Bands provides more reliable trading signals.
2. Strong adaptability: Bollinger Bands automatically adjust bandwidth based on market volatility.
3. Comprehensive risk control: Clear entry and exit conditions prevent overtrading.
4. Good visualization: Strategy provides clear visual indicators for market state understanding.
5. Parameter adjustability: Key parameters can be optimized for different market characteristics.

#### Strategy Risks
1. Choppy market risk: May generate frequent false breakout signals in sideways markets.
2. Trend market risk: Reversal signals might lead to premature exits in strong trends.
3. Parameter sensitivity: Different market environments may require different parameter settings.
4. Slippage risk: Actual execution prices may deviate from signal prices in less liquid markets.
5. Systematic risk: May face significant drawdowns during extreme market volatility.

#### Strategy Optimization Directions
1. Add trend filters: Introduce additional trend indicators to avoid counter-trend trades.
2. Optimize parameter adaptation: Develop dynamic parameter adjustment mechanisms.
3. Enhance risk management: Add dynamic stop-loss and profit target settings.
4. Incorporate volume analysis: Integrate volume indicators to improve signal reliability.
5. Develop market environment recognition: Build market state classification system for parameter adjustment.

#### Summary
This strategy builds a complete trading system through the synergy of RSI and Bollinger Bands. It provides clear entry and exit signals while maintaining good risk control mechanisms. Though inherent risks exist, continuous optimization and improvement enable the strategy to maintain stable performance across different market environments. The modular design also provides a solid foundation for future optimization and expansion.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-10-31 00:00:00
end: 2025-02-18 08:00:00
period: 30m
basePeriod: 30m
exchanges: [{"eid":"Binance","currency":"SOL_USDT"}]
*/

//@version=5
strategy("RSI + Bollinger Bands Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// Bollinger Bands Settings
bbLength = input.int(20, title="BB Length")
bbStdDev = input.float(2.0, title="BB Standard Deviation")
basis = ta.sma(close, bbLength)
dev = bbStdDev * ta.stdev(close, bbLength)
upperBB = basis + dev
lowerBB = basis - dev

// Plot Bollinger Bands
plot(basis, color=color.orange, title="BB Basis")
plot(upperBB, color=color.blue, title="Upper Bollinger Band")
plot(lowerBB, color=color.blue, title="Lower Bollinger Band")
fill(plot(upperBB), plot(lowerBB), color=color.blue, transp=90, title="BB Fill")

// RSI Settings
rsiLength = input.int(14, title="RSI Length")
rsiOverbought = input.int(70, title="RSI Overbought Level")
rsiOversold = input.int(30, title="RSI Oversold Level")
rsi = ta.rsi(close, rsiLength)

// Plot RSI on separate pane
hline(rsiOverbought, "Overbought", color=color.red)
hline(rsiOversold, "Oversold", color=color.green)
plot(rsi, color=color.purple, title="RSI", linewidth=2, display=display.none) // Hidden on main chart

// Long Condition: RSI crosses above oversold and price touches lower BB
longCondition = ta.crossover(rsi, rsiOversold) and close <= lowerBB
if (longCondition)
    strategy.entry("Long", strategy.long)

// Short Condition: RSI crosses below overbought and price touches upper BB
shortCondition = ta.crossunder(rsi, rsiOverbought) and close >= upperBB
if (shortCondition)
    strategy.entry("Short", strategy.short)

// Exit Long: RSI crosses above overbought or price crosses above basis
exitLong = ta.crossunder(rsi, rsiOverbought) or close >= basis
if (exitLong)
    strategy.close("Long")

// Exit Short: RSI crosses below oversold or price crosses below basis
exitShort = ta.crossover(rsi, rsiOversold) or close <= basis
if (exitShort)
    strategy.close("Short")

```

> Detail

https://www.fmz.com/strategy/482775

> Last Modified

2025-02-27 17:51:02
