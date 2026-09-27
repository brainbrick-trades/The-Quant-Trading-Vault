
> Name

Adaptive-Timeframe-SMA-Crossover-Strategy-with-Fixed-Profit-Targets

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8b33047d72fa054e3cd.png)
![IMG](https://www.fmz.com/upload/asset/2d91074276e39dd46dce6.png)





#### Overview

The Adaptive Timeframe SMA Crossover Strategy with Fixed Profit Targets is a scalping trading system based on Simple Moving Average (SMA) breakout signals, combined with fixed profit targets and specific timeframe restrictions. The core logic of this strategy utilizes the crossover relationship between price and moving average to generate long and short signals, while setting fixed point profit targets to secure gains, and only executing trades within specified timeframes. This design makes it particularly suitable for short-term trading in volatile markets with certain trending characteristics.

#### Strategy Principles

The strategy operates based on the following key components:

1. **Moving Average Calculation**: The strategy uses a Simple Moving Average (SMA) as its primary indicator, with a default period of 20, which users can adjust as needed. This moving average serves both as a trend determination reference and as a trigger condition for trade signals.

2. **Entry Conditions**:
   - Long Entry: When price crosses above the moving average (CROSSOVER) and the current price is higher than the moving average
   - Short Entry: When price crosses below the moving average (CROSSUNDER) and the current price is lower than the moving average

3. **Exit Conditions**:
   - Long Exit: When the highest price reaches the entry price plus the fixed profit target points
   - Short Exit: When the lowest price reaches the entry price minus the fixed profit target points

4. **Timeframe Restrictions**: The strategy only executes in specific timeframes, with defaults set to 1-minute, 3-minute, and 5-minute charts. If the current chart timeframe is not within the specified range, the strategy closes all positions.

5. **Visual Aids**:
   - The strategy marks entry and exit points on the chart
   - Uses green background to indicate uptrends and red background to indicate downtrends based on price position relative to the moving average

#### Strategy Advantages

1. **Clear Signal System**: Uses simple yet effective moving average crossover signals, reducing the subjectivity in trading decisions and making strategy execution more objective and disciplined.

2. **Fixed Profit Targets**: Preset profit targets help prevent excessive greed, ensure profit capture during market fluctuations, and avoid profit give-backs, which is especially important for short-term trading.

3. **Timeframe Optimization**: By restricting the strategy to execute only in specific timeframes, it avoids generating false signals on longer timeframes that are unsuitable for scalping, improving the strategy's applicability.

4. **Visual Feedback System**: Entry/exit markers and background color changes on the chart provide intuitive visual feedback, helping traders understand strategy logic and market conditions.

5. **Parameter Flexibility**: Key parameters such as moving average length, profit target, and applicable timeframes can all be adjusted according to different market conditions and trader preferences, enhancing the strategy's adaptability.

#### Strategy Risks

1. **Moving Average Lag**: Moving averages are inherently lagging indicators, which may cause delayed signals in volatile markets, missing optimal entry points or generating false signals. The solution is to adjust the MA period or incorporate other leading indicators to assist in decision-making.

2. **Limitations of Fixed Profit Targets**: Preset fixed profit targets may result in premature exits during strong trend movements, failing to fully capture trend momentum. Consider implementing dynamic profit targets or partial position management strategies.

3. **Opportunity Cost of Timeframe Restrictions**: Executing only in specific timeframes may miss effective signals in other timeframes. The solution is to expand the range of applicable timeframes or establish a multi-timeframe strategy combination.

4. **Lack of Stop-Loss Mechanism**: The current strategy lacks a clear stop-loss mechanism, which may face significant losses during sudden market reversals. Adding stop-loss conditions is recommended to control risk.

5. **Single Indicator Dependency**: Relying solely on moving averages may generate frequent false signals in sideways markets. This can be improved by adding additional filtering conditions or confirmation indicators to enhance signal quality.

#### Strategy Optimization Directions

1. **Add Stop-Loss Mechanism**: Incorporate explicit stop-loss conditions, such as ATR (Average True Range) based dynamic stops or fixed-point stops, to limit maximum loss per trade.

2. **Add Signal Filters**: Introduce additional technical indicators such as RSI (Relative Strength Index), MACD (Moving Average Convergence Divergence), or volume indicators as confirmation conditions for trade signals to reduce false signals.

3. **Implement Dynamic Profit Targets**: Automatically adjust profit targets based on market volatility, setting larger profit targets in high-volatility markets and smaller profit targets in low-volatility markets.

4. **Multi-Timeframe Analysis**: Integrate trend information from higher timeframes, only executing trades in the direction of the main trend, avoiding short-term trades against the major trend.

5. **Optimize Position Management**: Implement a scaled entry and exit strategy, allowing partial profits to run with the trend while securing some gains, balancing risk and reward.

6. **Add Market State Recognition**: Add functionality to automatically identify market states (trending/ranging) and apply different parameters or strategy variants in different market environments.

#### Summary

The Adaptive Timeframe SMA Crossover Strategy with Fixed Profit Targets is a concisely designed and practical short-term trading system that combines moving average crossover signals, fixed profit targets, and timeframe restrictions to provide traders with a disciplined approach to capturing short-term price movements. While relatively simple in design, the strategy's core logic is sound and offers broad optimization potential. By adding stop-loss mechanisms, signal filters, and dynamic parameter adjustments, this strategy can further enhance its robustness and adaptability. For investors seeking systematic trading in short timeframes, this represents a worthwhile basic strategy framework that can be further customized and optimized according to individual risk preferences and market characteristics.




> Source (PineScript)

``` pinescript
/*backtest
start: 2025-01-01 00:00:00
end: 2025-03-06 00:00:00
period: 5h
basePeriod: 5h
exchanges: [{"eid":"Futures_Binance","currency":"ETH_USDT"}]
*/

//@version=6
strategy("NDX Scalping Strategy", shorttitle="NDX Scalper", overlay=true)
// Input Parameters
maLength = input.int(20, "Moving Average Length", minval=1)
profitTarget = input.int(20, "Profit Target (points)", minval=1)
chartTimeframes = input.string("1,3,5", "Applicable Timeframes (min)")
// Moving Average CalculaƟon
ma = ta.sma(close, maLength)
// Calculate crossover condiƟons globally
longCrossover = ta.crossover(close, ma)
shortCrossunder = ta.crossunder(close, ma)
// Entry CondiƟons
longEntry = close > ma and longCrossover
shortEntry = close < ma and shortCrossunder
// Exit CondiƟons (Profit Target)
longExit = high >= (strategy.position_avg_price + profitTarget)
shortExit = low <= (strategy.position_avg_price - profitTarget)
// Ploƫng the Moving Average
plot(ma, color=color.blue, linewidth=2, title="Moving Average")
// Long Entry Signal
if longEntry 
    strategy.entry("Long", strategy.long)
    label.new(bar_index, low, text="Long", color=color.green, textcolor=color.white, size=size.normal)
// Short Entry Signal
if shortEntry
    strategy.entry("Short", strategy.short)
    label.new(bar_index, high, text="Short", color=color.red, textcolor=color.white, size=size.normal) 
// Exit Long PosiƟon
if longExit
    strategy.close("Long")
    label.new(bar_index, high, text="Exit Long", color=color.orange, textcolor=color.black,size=size.normal)
// Exit Short PosiƟon
if shortExit
    strategy.close("Short")
    label.new(bar_index, low, text="Exit Short", color=color.orange, textcolor=color.black,size=size.normal)
// Apply Timeframe RestricƟon
timeframeValid = str.contains(chartTimeframes, str.tostring(timeframe.period))
if not timeframeValid
    strategy.close_all()
// Background Color for Trend
bgcolor(close > ma ? color.new(color.green, 85) : color.new(color.red, 85)) 
```

> Detail

https://www.fmz.com/strategy/485288

> Last Modified

2025-03-07 09:49:32
