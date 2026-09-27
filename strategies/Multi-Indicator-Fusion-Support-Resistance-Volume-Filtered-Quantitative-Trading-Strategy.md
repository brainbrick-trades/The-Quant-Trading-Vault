
> Name

Multi-Indicator-Fusion-Support-Resistance-Volume-Filtered-Quantitative-Trading-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d93fccd7a5e33965ecbd.png)
![IMG](https://www.fmz.com/upload/asset/2d905d9986db2c5bb6876.png)


## Overview

This strategy is a multi-indicator fusion quantitative trading system that combines Simple Moving Average (SMA), Relative Strength Index (RSI), and Support/Resistance levels to generate trading signals. The strategy also incorporates time filtering and volume filtering mechanisms to enhance trading effectiveness. The core concept is to buy when the price approaches support levels and RSI indicates oversold conditions, and to sell when the price approaches resistance levels and RSI indicates overbought conditions. Additionally, it only executes trades within a specified time range and can optionally operate only when volume is above average levels, which helps ensure liquidity and effectiveness of trades.

## Strategy Principles

The strategy is based on several classic technical analysis concepts and indicators:

1. **Simple Moving Average (SMA)**: Uses a 50-period SMA to identify the overall direction of market trends. SMA serves as a smoothing indicator for price, helping to reduce noise and display clearer trends.

2. **Relative Strength Index (RSI)**: Uses a 14-period RSI to detect overbought and oversold market conditions. RSI below 30 is considered an oversold signal, while above 70 is considered overbought.

3. **Support and Resistance Levels**: Calculated through a 30-period window, taking the lowest price and highest price during this period respectively. These levels represent key areas where price may reverse.

4. **Trading Logic**:
   - Buy Signal: Triggered when price approaches support (not exceeding 1.02 times the support) and RSI is below 30 (oversold)
   - Sell Signal: Triggered when price approaches resistance (not below 0.98 times the resistance) and RSI is above 70 (overbought)

5. **Filtering Conditions**:
   - Time Filter: Only trades within a user-specified date range
   - Volume Filter: Can choose to trade only when volume is higher than the 20-period average volume

This approach combines elements of trend following and reversal trading, attempting to capture trading opportunities when prices reach extreme levels and show potential reversal signals.

## Strategy Advantages

1. **Multi-dimensional Signal Confirmation**: By combining multiple indicators (SMA, RSI, Support/Resistance), the strategy reduces the risk of false signals, generating trading signals only when multiple conditions are simultaneously met.

2. **Dynamic Support and Resistance**: The strategy uses a rolling window to calculate support and resistance levels, allowing these key price levels to automatically adjust as market conditions change.

3. **Flexible Filtering Mechanisms**:
   - Time filtering allows trading during specific time periods, avoiding potentially unstable or inefficient market periods
   - Volume filtering ensures trading only under conditions of sufficient liquidity, reducing slippage and execution issues

4. **Clear Entry Conditions**: The strategy has clear entry rules, combining price proximity to key levels and overbought/oversold conditions, which helps capture opportunities at potential reversal points.

5. **Visual Assistance**: The strategy includes plotting of SMA, support and resistance lines, and visualization of buy and sell signals, allowing traders to intuitively understand market conditions and strategy signals.

6. **Alert Functionality**: Built-in alert conditions enable traders to be notified when new signals are generated, facilitating real-time monitoring and trade execution.

## Strategy Risks

1. **False Breakout Risk**: When price approaches support or resistance levels, false breakouts may occur, followed by quick reversals, leading to incorrect signals. Consider adding confirmation mechanisms, such as waiting for price to remain near support/resistance for a certain time or adding additional confirmation indicators.

2. **Overtrading Risk**: In ranging markets or highly volatile markets, RSI may frequently cross overbought and oversold levels, resulting in too many trading signals. This can be reduced by adjusting RSI thresholds or adding signal filtering conditions.

3. **Parameter Sensitivity**: Strategy performance is highly dependent on selected parameters (SMA period, RSI period, support/resistance window, etc.). Different markets and timeframes may require different parameter settings; robust backtesting and optimization are recommended.

4. **Single Position Management**: The current strategy lacks stop-loss and profit-taking strategies, which may lead to excessive losses during sharp market fluctuations. Adding stop-loss strategies and position sizing management is recommended.

5. **Limitations of Time Filtering**: Fixed date ranges may cause missed trading opportunities outside the date range. Consider using more dynamic time filtering methods, such as adaptive filtering based on market conditions.

## Strategy Optimization Directions

1. **Add Stop-Loss and Profit Targets**:
   - Implement dynamic stop-losses based on ATR (Average True Range)
   - Add profit targets based on support/resistance levels
   - These improvements will enhance risk management capabilities, protect capital, and lock in profits

2. **Optimize Parameter Adaptability**:
   - Implement dynamic adjustment of parameters, automatically adjusting SMA, RSI periods, and support/resistance windows based on market volatility
   - This will make the strategy better adapt to different market conditions and asset classes

3. **Enhance Filtering Mechanisms**:
   - Add trend filtering, such as only going long when price is above SMA, and short when below SMA
   - Add volatility filtering to avoid trading during periods of extreme volatility
   - These filters will improve trading quality and reduce false signals

4. **Add Position Management**:
   - Dynamically adjust position size based on volatility and signal strength
   - Implement stepped entry and exit strategies to reduce market noise impact
   - This will optimize capital utilization and control risk for each trade

5. **Integrate Market Sentiment Indicators**:
   - Add other market sentiment indicators such as MACD or Bollinger Bands
   - Analyze signal consistency across multiple timeframes
   - This will provide a more comprehensive market perspective and improve signal quality

## Summary

The Multi-Indicator Fusion Support-Resistance Volume-Filtered Quantitative Trading Strategy is a comprehensive trading system that combines SMA, RSI, and dynamic support/resistance levels. By integrating multiple technical indicators and adding time and volume filtering, the strategy attempts to capture trading opportunities at potential market reversal points while reducing false signals and unnecessary trades.

The strategy's greatest advantages lie in its multi-dimensional signal confirmation and flexible filtering mechanisms, which improve the quality of trading signals. However, it also faces challenges such as false breakout risks and parameter sensitivity. By adding stop-loss mechanisms, optimizing parameter adaptability, enhancing filters, and improving position management, the strategy can be further optimized to improve performance and stability.

For traders looking to build robust trading systems based on technical analysis, this strategy provides a solid starting point. By deeply understanding its principles and customizing it according to specific market needs, traders can develop systems that better suit their trading style and risk preferences.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-04-08 00:00:00
end: 2025-04-07 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"ETH_USDT"}]
*/

//@version=5
strategy("SMA + RSI + S/R Strategy with Filters", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

// === Input Settings ===
smaPeriod = input.int(50, title="SMA Period")
rsiPeriod = input.int(14, title="RSI Period")
srWindow = input.int(30, title="Support/Resistance Window")
volumeFilter = input.bool(true, title="Enable Volume Filter")
tradeOnlyAboveVolume = input.bool(true, title="Only trade when volume > avg")

// === Indicators ===
sma = ta.sma(close, smaPeriod)
rsi = ta.rsi(close, rsiPeriod)
support = ta.lowest(low, srWindow)
resistance = ta.highest(high, srWindow)
avgVolume = ta.sma(volume, 20)

// === Volume Filter ===
volumeCondition = not volumeFilter or (volume > avgVolume)

// === Signals ===
buySignal = (close <= support * 1.02) and (rsi < 30) and volumeCondition
sellSignal = (close >= resistance * 0.98) and (rsi > 70) and volumeCondition

// === Strategy Backtest ===
if buySignal
    strategy.entry("Buy", strategy.long)
if sellSignal
    strategy.entry("Sell", strategy.short)

// === Plot Lines ===
plot(sma, title="SMA", color=color.orange)
plot(support, title="Support", color=color.green)
plot(resistance, title="Resistance", color=color.red)

// === Plot Signals ===
plotshape(buySignal, title="Buy Signal", location=location.belowbar, color=color.lime, style=shape.triangleup, size=size.small)
plotshape(sellSignal, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)

// === Alerts ===
alertcondition(buySignal, title="Buy Alert", message="Buy Signal Triggered!")
alertcondition(sellSignal, title="Sell Alert", message="Sell Signal Triggered!")

```

> Detail

https://www.fmz.com/strategy/489731

> Last Modified

2025-04-08 09:46:04
