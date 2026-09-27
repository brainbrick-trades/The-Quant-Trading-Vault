
> Name

Bollinger-Bands-with-Dual-SMA-Momentum-Enhanced-Quantitative-Trading-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d86827b13b6368d5238b.png)
![IMG](https://www.fmz.com/upload/asset/2d949951f2cbf45da67fe.png)




## Overview

The Bollinger Bands with Dual SMA Momentum Enhanced Quantitative Trading Strategy is a trend-following system specifically designed for market volatility. This strategy cleverly integrates the volatility channel of Bollinger Bands with a dual moving average trend confirmation mechanism, forming a multi-condition filtering trading decision framework. The core of the strategy lies in capturing strong signals when prices break through the upper Bollinger Band, and confirming trend direction through the positional relationship between fast and slow moving averages. It only enters long positions when multiple conditions are simultaneously satisfied, thereby improving trading accuracy and reliability.

## Strategy Principles

The technical principles of this strategy are built on the synergistic effect of three core indicators:

1. **Bollinger Bands System**: The strategy employs a 21-period Bollinger Band with a standard deviation multiplier of 2.0, and flexibly allows selection of the basis moving average type (SMA, EMA, SMMA, WMA, or VWMA) based on parameter settings. Bollinger Bands capture the range of price volatility, providing a volatility perspective reference for trading.

2. **Dual Moving Average System**: The strategy introduces a 6-period Fast Simple Moving Average (Fast SMA) and a 45-period Slow Simple Moving Average (Slow SMA), forming a dual moving average system. The crossover and positional relationship between these two moving averages can effectively identify and confirm the current trend's direction and strength.

3. **Multi-Condition Entry Mechanism**: The strategy only establishes long positions when all the following conditions are met:
   - Closing price breaks above the upper Bollinger Band (close > upper)
   - Closing price is above the Slow Moving Average (close > slowSma)
   - Fast Moving Average is above the Slow Moving Average (fastSma > slowSma)

This multi-condition design ensures that positions are only entered when a strong upward trend is confirmed by multiple technical indicators, effectively filtering out false breakouts and weak signals.

The position closing conditions are similarly based on clear technical indicator signals. When the closing price falls below the lower Bollinger Band or the Fast Moving Average drops below the Slow Moving Average, the strategy will automatically close positions. This design enables the strategy to cut losses or lock in profits in a timely manner, avoiding losses caused by trend reversals.

## Strategy Advantages

1. **Multiple Signal Confirmation Mechanism**: Combining Bollinger Band breakouts with dual moving average trend confirmation significantly reduces false breakout signals, improving trade quality and success rate.

2. **Adaptive Volatility**: The design of Bollinger Bands inherently possesses adaptive characteristics for market volatility. The channel naturally widens in high-volatility environments and narrows in low-volatility environments, allowing the strategy to adapt to different market conditions.

3. **Trend Strength Verification**: By requiring not only that the price breaks through the upper Bollinger Band, but also that it is above the slow moving average, and simultaneously that the fast moving average exceeds the slow moving average, these triple conditions ensure that only strong trends trigger trades.

4. **Flexible Parameter Configuration**: The strategy allows users to adjust Bollinger Band length, moving average type, standard deviation multiplier, and fast/slow moving average periods, enabling optimization adjustments based on different market conditions and personal trading styles.

5. **Clear Entry and Exit Logic**: The trading rules of the strategy are concise and explicit, with entry and exit conditions based on objective technical indicators, reducing the influence of subjective judgment.

## Strategy Risks

1. **Delayed Trend Identification**: Bollinger Bands and moving averages are lagging indicators, which may lead to delayed entry timing in highly volatile markets, missing some of the early gains. A solution could be to appropriately shorten the period of the fast moving average or adjust Bollinger Band parameters.

2. **Frequent Trading Risk**: In oscillating markets, prices may frequently break through the upper Bollinger Band and then fall back, leading to multiple trades and increased transaction costs. This can be mitigated by adding additional filtering conditions or extending the confirmation period to reduce false signals.

3. **Unidirectional Trading Limitation**: The current strategy only supports long trades, unable to profit in downtrend markets, resulting in insufficient capital utilization. Consider adding short trading strategies to implement bidirectional trading.

4. **Parameter Sensitivity**: Strategy performance is highly dependent on parameter settings, and different market environments may require different parameter combinations. It is recommended to conduct thorough backtesting and parameter optimization, or adopt an adaptive parameter adjustment mechanism.

5. **Transaction Cost Impact**: The strategy's set 0.1% commission and 3-point slippage may differ in actual trading, affecting real returns. Adjustments and testing should be done according to the actual fee structure of the trading platform.

## Strategy Optimization Directions

1. **Add Filtering Conditions**: Consider adding additional conditions such as volume confirmation, trend strength indicators (like ADX), or price pattern recognition to further improve signal quality. For example, require increased trading volume when Bollinger Bands break out, or ADX values greater than a specific threshold.

2. **Optimize Capital Management**: The current strategy uses 100% of account funds for trading. Consider introducing risk percentage models or volatility-adjusted position management to dynamically adjust position size based on market volatility and signal strength.

3. **Add Timeframe Verification**: Introduce multi-timeframe analysis, requiring trend direction confirmation on higher timeframes to reduce misjudgments in oscillating markets. For instance, require trend conditions to be met simultaneously on daily and 4-hour charts.

4. **Introduce Dynamic Stop-Loss Strategy**: Set dynamic stop-loss levels based on ATR (Average True Range), or use trailing stops (such as following the Bollinger Band middle line or slow moving average) to better protect profits.

5. **Add Bidirectional Trading Capability**: Extend the strategy to support short trading, establishing short positions when opposite conditions are met (price breaks below the lower Bollinger Band and fast moving average is below slow moving average), fully utilizing downtrend profits.

6. **Parameter Adaptive Mechanism**: Develop a parameter dynamic adjustment mechanism based on market states, automatically optimizing Bollinger Bands and moving average parameters in different volatility and trend strength environments to improve strategy adaptability.

## Conclusion

The Bollinger Bands with Dual SMA Momentum Enhanced Quantitative Trading Strategy integrates volatility and trend indicators to build a multi-level trading decision system. The core advantage of the strategy lies in its multiple condition confirmation mechanism, significantly improving signal quality and reliability. Despite certain lagging and parameter sensitivity issues, with proper risk management and parameter optimization, this strategy can achieve solid performance in markets with clear trends.

Further optimizations can be approached from aspects such as adding filtering conditions, improving capital management, introducing multi-timeframe analysis, and developing parameter adaptive mechanisms to make the strategy more comprehensive and robust. Overall, this is a clearly structured and logically rigorous trend-following strategy, suitable for traders with a certain understanding of technical analysis, especially in medium to long-term trend-oriented market environments.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-04-02 00:00:00
end: 2025-04-01 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("BTC Bollinger Bands w Fast and Slow SMAs", overlay=true, commission_value=0.1, slippage=3, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

length = input.int(21, minval=1)
fastSmaLength = input.int(6, title="Fast SMA Length", minval=1)  // Fast SMA with default 20
slowSmaLength = input.int(45, title="Slow SMA Length", minval=1)  // Slow SMA with default 60
maType = input.string("SMA", "Basis MA Type", options=["SMA", "EMA", "SMMA (RMA)", "WMA", "VWMA"])
src = input(close, title="Source")
mult = input.float(2.0, minval=0.001, maxval=50, title="StdDev")

// Calculate SMAs dynamically
fastSma = ta.sma(src, fastSmaLength)  // Fast SMA
slowSma = ta.sma(src, slowSmaLength)  // Slow SMA

// Bollinger Bands Calculation
ma(source, length, _type) =>
    switch _type
        "SMA" => ta.sma(source, length)
        "EMA" => ta.ema(source, length)
        "SMMA (RMA)" => ta.rma(source, length)
        "WMA" => ta.wma(source, length)
        "VWMA" => ta.vwma(source, length)

basis = ma(src, length, maType)
dev = mult * ta.stdev(src, length)
upper = basis + dev
lower = basis - dev

offset = input.int(0, "Offset", minval=-500, maxval=500)

// Plotting the bands, basis, and both dynamic SMAs
plot(basis, "Basis", color=#2962FF, offset=offset)
p1 = plot(upper, "Upper", color=#F23645, offset=offset)
p2 = plot(lower, "Lower", color=#089981, offset=offset)
plot(fastSma, "Fast SMA", color=color.orange, offset=offset)  // Plot the Fast SMA
plot(slowSma, "Slow SMA", color=color.blue, offset=offset)  // Plot the Slow SMA
fill(p1, p2, title="Background", color=color.rgb(33, 150, 243, 95))

// Strategy logic: Open long position when the price closes above the upper Bollinger Band, 
// the price is above the Slow SMA, and the Fast SMA is above the Slow SMA

// Condition to open a long position:
// 1. Price closes above the upper Bollinger Band
// 2. Price is above the Slow SMA
// 3. Fast SMA is above Slow SMA
if (close > upper and close > slowSma and fastSma > slowSma)
    // Open Long position on the next candle's open
    strategy.entry("Long", strategy.long)  // Open Long on the current candle

// Condition to close the long position: previous close below the lower Bollinger Band or Fast SMA is below Slow SMA
if (close < lower or fastSma < slowSma)
    // Close Long on the next candle's open
    strategy.close("Long")  // Close Long on the next bar's open

```

> Detail

https://www.fmz.com/strategy/489156

> Last Modified

2025-04-02 11:28:15
