
> Name

Momentum-Divergence-Trend-Reversal-Quantitative-Strategy-Based-on-MACD-Histogram

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8aa33e5f54aad9436c1.png)
![IMG](https://www.fmz.com/upload/asset/2d8b8336d2e5fc49461cf.png)





#### Overview
This strategy is a trend reversal trading system based on MACD histogram momentum divergence. It captures market reversal signals by analyzing the relationship between candlestick pattern changes and MACD histogram momentum changes. The core idea is to take counter-trend positions when signs of momentum decay appear, thereby positioning ahead of potential trend reversals.

#### Strategy Principle
The trading logic is divided into short and long directions:
Short Entry: When a large bullish candle appears (close above open) with a body larger than the previous candle, and the MACD histogram shows a declining trend for three consecutive periods, indicating weakening upward momentum, the system generates a short signal.
Long Entry: When a large bearish candle appears (close below open) with a body larger than the previous candle, and the MACD histogram shows an ascending trend for three consecutive periods, indicating weakening downward momentum, the system generates a long signal.
Position management uses counter-signal exit mechanism, closing positions when opposite trading signals appear. The strategy doesn't set stop-loss or take-profit levels, relying entirely on signals for position management.

#### Strategy Advantages
1. Clear Signals: The strategy considers both candlestick patterns and technical indicators, providing more reliable trading signals.
2. Reversal Detection: By monitoring momentum changes, it can identify market turning points early.
3. Controlled Risk: Using counter-signal exits prevents holding unfavorable positions during trend changes.
4. Simple Operation: Trading rules are clear, easy to execute and backtest.
5. High Adaptability: The strategy can be applied to different markets and timeframes.

#### Strategy Risks
1. False Breakout Risk: Markets may exhibit false breakouts, leading to incorrect signals.
2. Choppy Market Risk: Frequent trend changes in range-bound markets may result in consecutive losses.
3. Slippage Risk: Large trades may face significant slippage in low liquidity conditions.
4. Overtrading Risk: Frequent signals may generate high transaction costs.
5. Market Environment Dependency: Strategy performs better in trending markets but may underperform in other conditions.

#### Strategy Optimization Directions
1. Implement Trend Filters: Add trend identification indicators, such as moving average systems, to filter false signals in choppy markets.
2. Optimize Stop-Loss Mechanism: Set reasonable stop-loss levels to control per-trade risk.
3. Improve Take-Profit Mechanism: Dynamically adjust profit-taking levels based on market volatility.
4. Add Trading Filters: Such as volume confirmation and volatility filters to improve signal quality.
5. Enhance Position Management: Introduce dynamic position sizing mechanisms to adjust exposure based on market conditions.

#### Summary
This strategy captures market reversal opportunities by combining candlestick patterns and MACD histogram momentum changes, featuring simple operation and clear signals. While certain risks exist, the strategy's stability and profitability can be significantly enhanced through appropriate optimization and risk management measures. It is particularly suitable for trending market environments and can serve as an important component of a trading system.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-11-10 00:00:00
end: 2025-02-19 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=5
strategy("MACD Momentum Reversal Strategy", overlay=true, initial_capital=100000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === MACD Calculation ===
fastLength   = input.int(12, "MACD Fast Length")
slowLength   = input.int(26, "MACD Slow Length")
signalLength = input.int(9, "MACD Signal Length")
[macdLine, signalLine, histLine] = ta.macd(close, fastLength, slowLength, signalLength)

// === Candle Properties ===
bodySize      = math.abs(close - open)
prevBodySize  = math.abs(close[1] - open[1])
candleBigger  = bodySize > prevBodySize

bullishCandle = close > open
bearishCandle = close < open

// === MACD Momentum Conditions ===
// For bullish candles: if the MACD histogram (normally positive) is decreasing over the last 3 bars,
// then the bullish momentum is fading – a potential short signal.
macdLossBullish = (histLine[2] > histLine[1]) and (histLine[1] > histLine[0])

// For bearish candles: if the MACD histogram (normally negative) is increasing (moving closer to zero)
// over the last 3 bars, then the bearish momentum is fading – a potential long signal.
macdLossBearish = (histLine[2] < histLine[1]) and (histLine[1] < histLine[0])

// === Entry Conditions ===
// Short entry: Occurs when the current candle is bullish and larger than the previous candle,
// while the MACD histogram shows fading bullish momentum.
enterShort = bullishCandle and candleBigger and macdLossBullish

// Long entry: Occurs when the current candle is bearish and larger than the previous candle,
// while the MACD histogram shows fading bearish momentum.
enterLong  = bearishCandle and candleBigger and macdLossBearish

// === Plot the MACD Histogram for Reference ===
plot(histLine, title="MACD Histogram", color=color.blue, style=plot.style_histogram)

// === Strategy Execution ===
// Enter positions based on conditions. There is no stop loss or take profit defined;
// positions remain open until an opposite signal occurs.
if (enterShort)
    strategy.entry("Short", strategy.short)

if (enterLong)
    strategy.entry("Long", strategy.long)

// Exit conditions: close an existing position when the opposite signal appears.
if (strategy.position_size > 0 and enterShort)
    strategy.close("Long")

if (strategy.position_size < 0 and enterLong)
    strategy.close("Short")

```

> Detail

https://www.fmz.com/strategy/483020

> Last Modified

2025-02-21 09:25:50
