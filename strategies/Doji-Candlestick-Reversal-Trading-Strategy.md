
> Name

Doji-Candlestick-Reversal-Trading-Strategy

> Author

ChaoZhang

> Strategy Description



## Overview

This strategy forms a hammy lamp chandelier pattern by identifying the candlestick, and performs reversal transactions based on the SMA moving average judgment. When the Hami Chandelier pattern appears, if the opening and closing prices are outside the moving average, a trading signal is generated. The long signal is the hanging man, and the short signal is the hanging man.

## Principle

This strategy is mainly based on the following principles:

1. Identify the pattern of Hami lamp chandelier by calculating the opening and closing price range and the overall rise and fall.

2. Determine if the previous candlestick's closing price is higher or lower than the current candlestick's high and low to avoid false signals.

3. Determine the relationship between the opening and closing prices and the SMA moving average to form a reversal signal

4. When the shape of the Hami lamp chandelier is recognized and the conditions are met, a long or short signal is generated.

Main Steps of the Code Are as Follows:

1. Calculate SMA moving average

2. Loop to determine whether the shape of Hami lamp chandelier is formed

3. Determine the relationship between the closing price of the previous candlestick and the highest and lowest price of the current candlestick

4. Determine the relationship between opening/closing prices and moving averages to confirm reversal signals

5. Draw signal markers and output long and short signals

## Advantage Analysis

This strategy has the following advantages:

1. Hami lamp chandelier has a clear shape and is easy to identify and implement.

2. Combining with moving average filters can reduce false signals.

3. Clear long and short signals, operations are clear.

4. Reversal trading Capture short-term trend.

5. Parameters can be flexibly adjusted to adapt to different market conditions.

6. Easy to understand and implement, novice-friendly.

## Risk Analysis

This strategy also carries some risks:

1. Reliance on a single pattern, easy to be affected by false market breakouts.

2. Without a stop-loss mechanism, losses cannot be effectively controlled.

3. Improper parameter settings may lead to too frequent transactions.

4. Needs to be combined with trend judgment, performs poorly in trending markets. 

5. Effect depends on parameter optimization and requires continuous testing.

Corresponding solution:

1. Combine with other indicators to filter signals.

2. Add stop-loss mechanism, strictly control risk.

3. Optimize parameters to control trading frequency.

4. Only use in consolidation areas, avoid counter-trend.

5. Continuously backtest and optimize, examine effect regularly.

## Optimization Direction

This strategy can continue to be optimized in the following ways:

1. Add volume filter, avoid false breakouts.

2. Add stop-loss mechanisms, such as trailing stop-loss, death cross stop-loss, etc.

3. Optimize parameters based on market structure, such as distinguishing between trending and consolidating market parameters.

4. Confirm the signal in conjunction with other indicators. Such as MACD, KDJ, etc. 

5. Add trend judgment, avoid counter-trend trades.

6. Optimize cycle period parameters and balance FREQ and signal quality.

## Summary

This strategy uses the chandelier line shape combined with SMA moving average judgment to achieve efficient reversal trading. It has the advantages of simple signal and easy operation. At the same time, there are also some risks and room for optimization. Through continuous optimization and testing, this strategy can become an efficient and stable short-term trading strategy.



||


## Overview

This strategy identifies doji candlestick patterns and combines SMA to determine reversals for trading. It generates trading signals when doji patterns form and the open/close prices are outside the SMA lines. Bullish signals are generated on hanging man lines and bearish signals on shooting star lines.

## Principles 

The main principles of this strategy are:

1. Identifying doji patterns by calculating the range of open/close prices vs the overall price movement.

2. Checking if previous close is above/below current high/low to avoid false signals. 

3. Judging open/close prices in relation to SMA lines to generate reversal signals.

4. Generating long/short signals when qualified doji patterns are identified.

The main steps in the code are:

1. Calculating SMA lines

2. Looping through candles to identify doji patterns

3. Checking previous close vs current high/low relationship 

4. Confirming reversal signals based on open/close and SMA relationship

5. Plotting signal markers and outputting long/short signals

## Advantages

The advantages of this strategy include:

1. Doji patterns are clear and easy to identify/implement.

2. SMA filters help reduce false signals. 

3. Clear long/short signals make trading operations straightforward. 

4. Reversal trading captures short-term trends.

5. Flexible parameters can adapt to different market conditions.

6. Easy to understand and implement, beginner friendly.

## Risks

Some potential risks:

1. Reliance on single pattern, prone to false breakouts. 

2. No stop loss mechanism to control losses.

3. Bad parameter tuning can lead to over-trading. 

4. Trend-reliant, underperforms in trending markets.

5. Performance relies on parameter optimization.

Solutions:

1. Add other filters to confirm signals.

2. Implement stop loss to manage risks.

3. Optimize parameters and limit trade frequency. 

4. Use mainly during range-bound markets.

5. Continual backtesting and optimization.

## Improvement Areas

Some ways to improve the strategy:

1. Add volume filter to avoid false breakouts.

2. Implement stop loss mechanisms like trailing stop loss.

3. Optimize parameters based on market conditions like trends.

4. Add other indicators to confirm signals, like MACD, KDJ etc.

5. Add trend determination to avoid counter-trend trading. 

6. Optimize lookback period to balance frequency and quality.

## Summary

This strategy uses doji patterns with SMA for efficient reversal trading. It has advantages like simple rules and easy trading. But also has risks and areas for improvement. With continual optimization it can become a solid short-term trading system.



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|10|SMA Period|
|v_input_2|0.1|Tolerance|
|v_input_3|2|End|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-09-20 00:00:00
end: 2023-09-26 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Doji Reversal", overlay=true)

smaPeriod = input(title="SMA Period", defval=10, minval=0)
tolerance = input(title="Tolerance", defval=0.1, minval=0)

lookbackEnd = input(title="End", defval=2, minval=0)

avg = sma(close, smaPeriod)
signal_long = bool(false)
signal_short = bool(false)

for i = 1 to lookbackEnd
    is_doji = (abs(close[i] - open[i]) / (high[i] - low[i])) < tolerance
    signal_long := signal_long or ( is_doji and (close[i-1] <= high[i] or i == 1) and close[i-1] > high[i] and high[i] < avg and close > open )
    signal_short := signal_short or ( is_doji and (close[i-1] >= low[i] or i == 1) and close[i-1] < low[i] and low[i] > avg and close < open )

plotshape(signal_long, "LONG", style=shape.triangleup, size=size.normal)
plotshape(signal_short, "SHORT", style=shape.triangledown, size=size.normal)

strategy.entry("LONG", strategy.long, when=signal_long)
strategy.entry("SHORT", strategy.short, when=signal_short)
```

> Detail

https://www.fmz.com/strategy/427992

> Last Modified

2023-09-27 16:40:28
