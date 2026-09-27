
> Name

Dual-EMA-RSI-Momentum-Trend-Following-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/d4aac3c0f62012a302.png)


#### Overview
This strategy is a trend-following trading system based on dual EMAs and RSI indicator. It combines EMA crossover signals, RSI overbought/oversold conditions, and price breakthrough confirmation to build a multi-filtered trading decision framework. The strategy uses 6-period and 82-period Exponential Moving Averages (EMA) to capture medium and short-term trends, while utilizing the Relative Strength Index (RSI) to filter market overheating and overcooling conditions, and finally confirms trading signals through price breakouts.

#### Strategy Principles
The core logic includes three dimensions of signal filtering:
1. Trend Determination: Uses crossovers between fast EMA (6-period) and slow EMA (82-period) to judge trend direction. Long signals are generated when the fast line crosses above the slow line, and short signals when the fast line crosses below.
2. Momentum Filtering: Uses 14-period RSI to filter excessive trend chasing. Market is considered overbought when RSI exceeds 70 (suppressing longs), and oversold when RSI falls below 22 (suppressing shorts).
3. Price Confirmation: Requires price breakthrough confirmation for entry. Long positions require closing price to make new highs, while short positions require new lows.

#### Strategy Advantages
1. Multiple Signal Filtering: Effectively reduces false signals through combination of technical indicators and price action.
2. Trend Following with Momentum Integration: Captures sustained trends while avoiding excessive trend chasing.
3. Strong Parameter Adaptability: Key parameters like EMA periods and RSI thresholds can be optimized for different market characteristics.
4. Comprehensive Risk Control: Built-in risk control mechanism through RSI overbought/oversold conditions.

#### Strategy Risks
1. Choppy Market Risk: EMA crossover signals may occur frequently in sideways markets, leading to overtrading.
2. Lag Risk: Both EMA and RSI have inherent lag, potentially causing delayed reactions to rapid market turns.
3. Parameter Sensitivity: Strategy performance is sensitive to parameter selection, different market environments may require different parameter combinations.
4. Signal Scarcity: Multiple filtering mechanisms may result in fewer valid signals, affecting profit opportunities.

#### Strategy Optimization Directions
1. Dynamic Parameter Adjustment: Introduce adaptive mechanisms to dynamically adjust EMA periods and RSI thresholds based on market volatility.
2. Stop Loss Implementation: Add trailing or fixed stop loss rules to enhance risk control capabilities.
3. Market Environment Classification: Add market state identification module to use different parameter combinations in different market conditions.
4. Signal Strength Grading: Design a grading system based on signal condition satisfaction levels to adjust position sizing.

#### Summary
The strategy constructs a logically rigorous trend-following system through clever combination of EMA system and RSI indicator. While the multiple filtering mechanisms effectively control risk, they may also miss some trading opportunities. Through continuous optimization and improvement, the strategy shows promise in maintaining stable performance across different market environments.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-17 00:00:00
end: 2025-02-15 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("EMA RSI Strategy", overlay=true)

// Input Parameters
emaShortLength = input.int(6, title="EMA Short Length")
emaLongLength = input.int(82, title="EMA Long Length")
rsiLength = input.int(14, title="RSI Length")
rsiOverbought = input.float(70, title="RSI Overbought Level")
rsiOversold = input.float(22, title="RSI Oversold Level")

// Calculations
emaShort = ta.ema(close, emaShortLength)
emaLong = ta.ema(close, emaLongLength)
rsi = ta.rsi(close, rsiLength)

// Conditions
emaBuyCondition = ta.crossover(emaShort, emaLong)
emaSellCondition = ta.crossunder(emaShort, emaLong)
higherHighCondition = close > ta.highest(close[1], 1)
lowerLowCondition = close < ta.lowest(close[1], 1)
rsiNotOverbought = rsi < rsiOverbought
rsiNotOversold = rsi > rsiOversold

// Entry Signals
buySignal = emaBuyCondition and rsiNotOverbought and higherHighCondition
sellSignal = emaSellCondition and rsiNotOversold and lowerLowCondition

// Execute Trades
if (buySignal)
    strategy.entry("Buy", strategy.long)

if (sellSignal)
    strategy.entry("Sell", strategy.short)

// Plotting
plot(emaShort, color=color.green, title="EMA Short")
plot(emaLong, color=color.red, title="EMA Long")
plot(rsi, title="RSI", color=color.blue, linewidth=1)
hline(rsiOverbought, title="RSI Overbought", color=color.red, linestyle=hline.style_dotted)
hline(rsiOversold, title="RSI Oversold", color=color.green, linestyle=hline.style_dotted)

```

> Detail

https://www.fmz.com/strategy/482241

> Last Modified

2025-02-17 10:51:53
