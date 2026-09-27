
> Name

Multi-level-Bollinger-Bands-Trend-Following-and-Reversal-Trading-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8a9c271ecebe0c63531.png)
![IMG](https://www.fmz.com/upload/asset/2d7f32eb66138557d580f.png)



#### Overview
The Multi-level Bollinger Bands Trend Following and Reversal Trading Strategy is a comprehensive trading system based on the Bollinger Bands indicator. This strategy cleverly combines trend following and reversal trading characteristics by capturing market opportunities through the interaction between price and the upper and lower Bollinger Bands. The system has designed a three-layer exit mechanism, including zone judgment, moving average crossover, and trailing stop profit, which maximizes profit capture while effectively controlling risk. This strategy is applicable to various market environments and time periods, particularly suitable for highly volatile financial markets.

#### Strategy Principles
The core principle of this strategy is to use Bollinger Bands as a dynamic reference range for price fluctuations, combined with carefully designed multi-level entry and exit rules.

The entry logic is divided into two parts:
1. Long entry conditions: Enter long when the price crosses above the lower Bollinger Band (Crossover Lower Band), or when the price touches below the lower band and then rebounds (i.e., the low price is below the lower band but the closing price is above the lower band).
2. Short entry conditions: Enter short when the price crosses below the upper Bollinger Band (Crossunder Upper Band), or when the price touches above the upper band and then falls back (i.e., the high price is above the upper band but the closing price is below the upper band).

The exit logic includes three protective measures:
1. First layer (zone judgment): Starting from the X-th bar after entry, exit when the closing price enters a specific area of the Bollinger Bands. Specifically, for long positions, close the position if the price falls to the first 1/3 area between the lower band and the middle band; for short positions, close the position if the price rises to the first 1/3 area between the upper band and the middle band.
2. Second layer (moving average crossover): Starting from the Y-th bar after entry, close the position if the closing price crosses the 20-period moving average (MA20).
3. Third layer (trailing stop profit): Activate the trailing stop profit mechanism when the price breaks through the opposite edge of the Bollinger Bands, and automatically exit once the profit retraces by Z%, securing most of the gains.

Bollinger Bands parameters can be flexibly adjusted, including the moving average period (default 20) and standard deviation multiplier (default 2.0). Exit settings can also be adjusted according to market characteristics, including X (default 3), Y (default 10), and trailing stop profit retreat percentage Z (default 30%).

#### Strategy Advantages
1. Captures various market opportunities: The strategy includes both trend following and reversal trading logic, allowing it to find trading opportunities in different market environments. When the market is in a consolidation state, it can capitalize on price rebounds/falls after touching the edges of Bollinger Bands; when the market begins a trend movement, it can follow the trend through signals of price breakthrough at the edges of Bollinger Bands.

2. Multi-level risk control: Through three different exit condition mechanisms, the strategy can protect capital in various situations. The first layer of zone judgment can quickly identify incorrect trading directions; the second layer of moving average crossover is suitable for medium-term trend changes; the third layer of trailing stop profit protects profits after significant gains.

3. Flexible parameters: The strategy provides multiple adjustable parameters, allowing traders to optimize the system according to different market and time period characteristics. Bollinger Bands length and multiplier can be adjusted to adapt to market volatility, and the time parameters (X and Y) of exit conditions as well as the trailing stop profit retreat ratio (Z) can be set according to the trader's risk preference.

4. Visualization advantage: Bollinger Bands and newly added middle reference lines are directly drawn on the chart, facilitating intuitive analysis of price positions and potential support/resistance areas, improving decision-making efficiency.

5. Clear code structure: The strategy code is well-organized, with standardized variable naming and detailed comments, making it easy to understand and maintain. Entry and exit logic are clearly separated, facilitating subsequent expansion and optimization.

#### Strategy Risks
1. Lack of explicit stop-loss mechanism: The current strategy does not include traditional stop-loss conditions, which may lead to significant losses under extreme market conditions. It is recommended that traders manually add fixed stop-loss or ATR-based dynamic stop-loss logic according to their risk tolerance.

2. Over-reliance on Bollinger Bands: In highly volatile or low liquidity markets, Bollinger Bands may be too wide or too narrow, leading to decreased signal quality. It is recommended to test different Bollinger Bands parameter settings in different market environments.

3. Parameter sensitivity: Strategy performance may be sensitive to parameter settings, such as Bollinger Bands length, standard deviation multiplier, and time parameters for exit conditions. Inappropriate parameter selection may lead to overtrading or missing important opportunities.

4. Fixed trailing stop profit trigger conditions: In the current code, the trigger condition for the trailing stop profit is set to a fixed 2 times risk distance, which may not be applicable to all market environments. In highly volatile markets, this may cause the stop profit to be set too far, failing to effectively protect profits.

5. Symmetry risk for long and short conditions: The strategy uses symmetrical entry and exit logic for long and short directions, but in actual markets, rising and falling behaviors are often asymmetrical (e.g., stock markets usually fall faster than they rise). It is recommended to consider setting different parameters for long and short directions.

#### Strategy Optimization Directions
1. Add intelligent stop-loss mechanism: Dynamic stop-loss based on ATR (Average True Range) can be introduced, or stop-loss distance can be set based on Bollinger Bands width, making the stop-loss more aligned with actual market volatility. This can be implemented by adding a stop parameter in the strategy.entry function or using the stop_loss parameter of the strategy.exit function.

2. Optimize entry filtering conditions: Consider adding trend confirmation indicators, such as Directional Movement Index (DMI) or Relative Strength Index (RSI), to filter low-quality signals. For example, only accept trend following signals when ADX>25, or only accept reversal signals in RSI overbought/oversold areas.

3. Adaptive parameter settings: Design Bollinger Bands parameters and exit condition parameters in an adaptive form, automatically adjusting based on market volatility. For example, calculate the volatility over the past N periods and dynamically adjust the standard deviation multiplier of Bollinger Bands accordingly.

4. Improve trailing stop profit mechanism: Make the trigger conditions and tracking distance for trailing stop profit adjustable, rather than fixed at 2 times risk distance. Consider adjusting the trailing stop profit retreat percentage based on volatility characteristics of different time periods.

5. Add time filtering: Introduce trading session filtering to avoid high volatility periods before market opening and closing, or add optimal trading time filters for specific markets.

6. Multi-timeframe analysis: Integrate multi-timeframe analysis framework, requiring the trend direction of higher timeframes to be consistent with the current trading direction to improve signal quality. For example, only accept long signals on a 4-hour chart when the daily trend is upward.

7. Optimize money management: Add position calculation logic based on volatility, increasing positions in low volatility environments and decreasing positions in high volatility environments, to balance risk and return.

#### Conclusion
The Multi-level Bollinger Bands Trend Following and Reversal Trading Strategy is a comprehensively designed trading system that effectively manages risk while capturing market opportunities through the dynamic characteristics of the Bollinger Bands indicator combined with multi-level exit rules. The greatest advantage of this strategy lies in its flexibility and adaptability, allowing it to find trading opportunities in different market environments and adapt to different trading instruments and time periods through parameter adjustments.

Although the strategy has some risk points, such as the lack of a clear stop-loss mechanism and parameter sensitivity, through the optimization directions proposed in this article, such as adding intelligent stop-loss, optimizing entry filtering conditions, adaptive parameter settings, etc., the robustness and profitability of the strategy can be further enhanced.

For traders, it is recommended to conduct thorough backtesting before actual application and adjust parameters according to specific market characteristics. At the same time, this strategy should be used as part of a complete trading system, combined with other technical and fundamental analysis, to develop comprehensive trading decisions.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-04-01 00:00:00
end: 2025-03-31 00:00:00
period: 6d
basePeriod: 6d
exchanges: [{"eid":"Futures_Binance","currency":"ETH_USDT"}]
*/

//@version=6
strategy("Bollinger Bands Strategy", overlay=true)

// Input parameters
length = input.int(20, "BB Length", minval=1, group="Bollinger Bands settings")
mult = input.float(2.0, "BB Multiplier", minval=0.001, maxval=50, group="Bollinger Bands settings")
X = input.int(3, "Exit Condition 1 Bars (X)", minval=1, group="Exit settings")
Y = input.int(10, "Exit Condition 2 Bars (Y)", minval=1, group="Exit settings")
Z = input.float(30.0, "Trail Profit Retreat Z%", minval=1.0, maxval=100.0, step=1.0, group="Exit settings")

// Calculate Bollinger Bands
source = close
basis = ta.sma(source, length)          // 20 period moving average
dev = mult * ta.stdev(source, length)   // standard deviation
upper = basis + dev                     // Shangyuan
lower = basis - dev                     // Lower edge
mid1 = upper - (upper - basis)/3
mid2 = lower + (basis - lower)/3

// Draw Bollinger Bands
plot(basis, "Basis", color=color.gray)
plot(upper, "Upper", color=color.blue)
plot(lower, "Lower", color=color.blue)
plot(mid1,"mid1",color = color.yellow)
plot(mid2,"mid2",color = color.yellow)
//fill(upper, lower, color=color.new(color.blue, 90), title="BB Fill")

// Entry Conditions
longEntry = ta.crossover(source, lower) or (low < lower and close > lower)
shortEntry = ta.crossunder(source, upper) or (high > upper and close < upper)

// Entry execution
if (longEntry)
    strategy.entry("Long", strategy.long)

if (shortEntry)
    strategy.entry("Short", strategy.short)

// Exit Condition Variables
var float longEntryPrice = na
var float shortEntryPrice = na
var int longBarsSinceEntry = 0
var int shortBarsSinceEntry = 0

// Update Position Status
if (strategy.position_size > 0)  // Long positions
    if (na(longEntryPrice))      // Record entry price and initial count
        longEntryPrice := strategy.position_avg_price
        longBarsSinceEntry := 0
    longBarsSinceEntry := longBarsSinceEntry + 1

if (strategy.position_size < 0)  // Short positions
    if (na(shortEntryPrice))
        shortEntryPrice := strategy.position_avg_price
        shortBarsSinceEntry := 0
    shortBarsSinceEntry := shortBarsSinceEntry + 1

// Long Exit Conditions
if (strategy.position_size > 0)
    // Conditions 1:No. X Root K After Line, Closing Price < lower + (basis - lower) / 3
    longExitLevel1 = lower + (basis - lower) / 3
    if (longBarsSinceEntry >= X and close < longExitLevel1)
        strategy.close("Long", comment="Long Exit Condition 1")
    
    // Conditions 2:No. Y Root K After Line, Closing Price < basis
    if (longBarsSinceEntry >= Y and close < basis)
        strategy.close("Long", comment="Long Exit Condition 2")
    
    // Conditions 3:Trailing take profit (closing price > upper trigger)
    distanceLong = longEntryPrice - lower
    trailPriceLong = longEntryPrice + (distanceLong * 2)  // Assume 2x risk distance as the trigger point, adjustable.
    trailOffsetLong = distanceLong * (1 - Z / 100)
    strategy.exit("Long Trail", "Long", trail_price=trailPriceLong, trail_offset=trailOffsetLong)

// Short Exit Conditions
if (strategy.position_size < 0)
    // Conditions 1:No. X Root K After Line, Closing Price > upper - (upper - basis) / 3
    shortExitLevel1 = upper - (upper - basis) / 3
    if (shortBarsSinceEntry >= X and close > shortExitLevel1)
        strategy.close("Short", comment="Short Exit Condition 1")
    
    // Conditions 2:No. Y Root K After Line, Closing Price > basis
    if (shortBarsSinceEntry >= Y and close > basis)
        strategy.close("Short", comment="Short Exit Condition 2")
    
    // Conditions 3:Trailing take profit (closing price < lower trigger)
    distanceShort = upper - shortEntryPrice
    trailPriceShort = shortEntryPrice - (distanceShort * 2)  // Assume 2x risk distance as the trigger point, adjustable.
    trailOffsetShort = distanceShort * (1 - Z / 100)
    strategy.exit("Short Trail", "Short", trail_price=trailPriceShort, trail_offset=trailOffsetShort)

// Clear variables (when position ends))
if (strategy.position_size == 0)
    longEntryPrice := na
    shortEntryPrice := na
    longBarsSinceEntry := 0
    shortBarsSinceEntry := 0
```

> Detail

https://www.fmz.com/strategy/489010

> Last Modified

2025-04-01 10:16:29
