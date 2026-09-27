
> Name

Multi-Indicator-Trend-Following-Momentum-Trading-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d949b61f63316134d5dd.png)
![IMG](https://www.fmz.com/upload/asset/2d83c82978b0a25698f04.png)




#### Overview
This strategy is a trend-following momentum trading system that combines multiple technical indicators. It primarily uses the 200-day Moving Average (MA200) to determine the main trend direction, utilizes the 50-day Exponential Moving Average (EMA50) to identify pullback opportunities, and combines the Relative Strength Index (RSI) and Moving Average Convergence Divergence (MACD) crossover signals to determine entry timing. The strategy also includes risk management mechanisms through setting risk-reward ratios and trailing stops to protect profits.

#### Strategy Principles
The core logic of the strategy is to improve trading accuracy through multiple filtering mechanisms. First, MA200 is used to determine the market's main trend, with prices above MA200 indicating a bullish trend and vice versa. After determining the trend direction, the strategy looks for pullback opportunities near EMA50, requiring the price to touch EMA50 within the last 5 periods. Meanwhile, RSI is used for momentum confirmation, requiring RSI above 50 in bullish trends and below 50 in bearish trends. Finally, MACD crossovers serve as specific entry signals. For exits, the strategy employs fixed stop-loss and take-profit levels based on risk-reward ratios, with an optional trailing stop feature.

#### Strategy Advantages
1. Multiple indicators provide collaborative verification, improving trading reliability
2. Combines trend and momentum factors to capture major market movements
3. Pullback entry mechanism reduces the risk of chasing highs
4. Flexible stop-loss mechanism protects capital while capturing significant trends
5. Strong parameter adjustability adapts to different market environments
6. Clear strategy logic, easy to understand and execute

#### Strategy Risks
1. Multiple indicator filtering may cause missed trading opportunities
2. May generate frequent false signals in ranging markets
3. Moving averages have inherent lag, potentially affecting entry timing
4. Fixed risk-reward ratios may perform differently across market environments
5. Parameter optimization may lead to overfitting risk

#### Strategy Optimization Directions
1. Introduce volatility indicators for dynamic risk-reward ratio adjustment
2. Add market environment filtering to identify trending and ranging markets
3. Optimize pullback detection logic to improve entry timing accuracy
4. Add volume confirmation mechanism to enhance signal reliability
5. Develop adaptive parameter system to improve strategy robustness

#### Summary
This strategy constructs a complete trend-following trading system through the comprehensive use of multiple technical indicators. Its strength lies in multiple signal confirmations improving trading reliability, while risk management mechanisms provide good protection. Although some inherent risks exist, the suggested optimization directions can further enhance strategy performance. Overall, this is a logically rigorous and practical quantitative trading strategy.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-21 00:00:00
end: 2024-08-10 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=6
strategy("Trend-Following Momentum Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=2)

// PARAMETERS
lengthMA200 = input(200, title="200-day MA Length")
lengthEMA50 = input(50, title="50-day EMA Length")
rsiLength = input(14, title="RSI Length")
macdFastLength = input(12, title="MACD Fast Length")
macdSlowLength = input(26, title="MACD Slow Length")
macdSignalLength = input(9, title="MACD Signal Length")
riskRewardRatio = input(1.5, title="Risk-Reward Ratio")
useTrailingStop = input(true, title="Use Trailing Stop?")
trailingPercent = input(1.0, title="Trailing Stop (%)") / 100

// INDICATORS
ma200 = ta.sma(close, lengthMA200) // 200-day MA
ema50 = ta.ema(close, lengthEMA50) // 50-day EMA
rsi = ta.rsi(close, rsiLength) // RSI
[macdLine, signalLine, _] = ta.macd(close, macdFastLength, macdSlowLength, macdSignalLength)

// TREND CONDITIONS
bullishTrend = close > ma200
bearishTrend = close < ma200

// PULLBACK CONDITION
recentPullbackLong = ta.barssince(close < ema50) < 5 // Price touched EMA50 in last 5 bars
recentPullbackShort = ta.barssince(close > ema50) < 5 // Price touched EMA50 in last 5 bars

// ENTRY CONDITIONS
longEntry = bullishTrend and ta.crossover(macdLine, signalLine) and rsi > 50 and recentPullbackLong
shortEntry = bearishTrend and ta.crossunder(macdLine, signalLine) and rsi < 50 and recentPullbackShort

// EXECUTE TRADES
if longEntry
    strategy.entry("Long", strategy.long)
    strategy.exit("Long Exit", from_entry="Long", limit=close * (1 + riskRewardRatio), stop=close * (1 - (1 / (1 + riskRewardRatio))), trail_price=useTrailingStop ? close * (1 - trailingPercent) : na)

if shortEntry
    strategy.entry("Short", strategy.short)
    strategy.exit("Short Exit", from_entry="Short", limit=close * (1 - riskRewardRatio), stop=close * (1 + (1 / (1 + riskRewardRatio))), trail_price=useTrailingStop ? close * (1 + trailingPercent) : na)

// PLOT INDICATORS
plot(ma200, title="200-day MA", color=color.blue, linewidth=2)
plot(ema50, title="50-day EMA", color=color.orange, linewidth=2)
```

> Detail

https://www.fmz.com/strategy/483029

> Last Modified

2025-02-21 10:06:35
