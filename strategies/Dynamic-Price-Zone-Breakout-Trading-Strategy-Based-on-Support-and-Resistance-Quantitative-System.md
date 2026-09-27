
> Name

Dynamic-Price-Zone-Breakout-Trading-Strategy-Based-on-Support-and-Resistance-Quantitative-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/121e934dae22e837310.png)


#### Overview
This strategy is a quantitative trading system based on price range breakouts. It operates by dynamically setting upper and lower price limits and executing trades when prices break through these key levels. The core concept is to capture trending opportunities when the market breaks out of established price ranges while adapting to market changes through dynamic adjustment of price zones. The strategy employs flexible position management, allowing additional trades in the same direction to maximize profits from major trends.

#### Strategy Principles
The strategy operates based on the following core mechanisms: First, it sets appropriate step sizes for different trading instruments, typically around 1.5% of the instrument's price. The system establishes price zones above and below the current price, triggering long signals when prices break above the upper limit and short signals when breaking below the lower limit. After each breakout, the price zones adjust to adapt to the new market environment. The strategy supports adding positions in the same direction, allowing up to 200 positions, enabling profit maximization during strong trends. Order processing includes multiple safeguards, including processing at bar close, recalculating after trade execution, and computing at every price tick.

#### Strategy Advantages
1. Strong Dynamic Adaptation: Price zones automatically adjust with market changes, allowing the strategy to adapt to different market conditions.
2. Excellent Trend Following Capability: Through allowing additional positions in the same direction, the strategy can fully capitalize on strong trends.
3. Comprehensive Risk Control: Clear stop-loss conditions are set, automatically closing positions when prices break below the zone.
4. Wide Applicability: The strategy can be applied to various markets through appropriate step size parameters for different trading instruments.
5. High Computational Efficiency: Employs variable persistence and efficient calculation methods to ensure smooth strategy operation.

#### Strategy Risks
1. Choppy Market Risk: Frequent false breakouts in range-bound markets may lead to consecutive stops.
2. Position Management Risk: Adding positions in the same direction may lead to over-concentration, requiring proper control of directional risk exposure.
3. Slippage Risk: Significant slippage during volatile periods may affect strategy performance.
4. Parameter Sensitivity: The effectiveness of the strategy directly depends on appropriate step size settings, requiring thorough testing.

#### Strategy Optimization Directions
1. Incorporate Volatility Indicators: Dynamically adjust step sizes based on market volatility to improve strategy adaptability.
2. Add Filtering Mechanisms: Include trend confirmation indicators to reduce losses from false breakouts.
3. Enhance Position Management: Design more detailed position control mechanisms to balance returns and risks.
4. Optimize Order Execution: Add smart order routing to reduce slippage impact.
5. Include Time Dimension: Consider market time characteristics to adjust strategy parameters during different periods.

#### Summary
This is a well-designed trend following strategy with clear logic. Through dynamic price zone settings and adjustments, combined with flexible position management, the strategy can effectively capture market trending opportunities. While there is room for optimization, overall, the strategy provides a robust quantitative trading framework. Through continuous optimization and improvement, strategy performance can be further enhanced. The strategy design thoroughly considers various aspects of practical trading, including order processing and computational efficiency, demonstrating strong practicality.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-09 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// @version=5
// Draw horizontal lines at corresponding intervals on each chart,Draw it yourself
// Add in the same direction20After the order is executed, recalculate eachtickRecalculate, save variables1000Periods,kAfter the line ends, process the order again and draw it according to the code sequence.plot
strategy("Price Level Breakout Strategy", overlay=true, pyramiding=200, calc_on_order_fills=true, calc_on_every_tick=true, max_bars_back=1000, process_orders_on_close=true, explicit_plot_zorder=true)
// varCreate persistent variable,:=is to update the variable, not to redeclare it
// This is a global variable
// a = array.new<string>(200)
// array.push(a, "a")
// plot(close, color = array.get(a, close > open ? 1 : 0))
string ticker = syminfo.ticker
var float step_size = 1000
// label.new(x=bar_index, y=close, text="Current product code: " + ticker)
// Draw according to fixed value1.5parallel lines
if ticker == "000300"
    step_size := 4000 * 0.015
if ticker == "XAUUSD"
    step_size := 3000 * 0.016
if ticker == "BTCUSD"
    step_size := 60000 * 0.015
if ticker == "SILVER"
    step_size := 50 * 0.015
if ticker == "UKOIL"
    step_size := 150 * 0.015
if ticker == "GBPUSD"
    step_size := 1.6 * 0.015
if ticker == "EURUSD"
    step_size := 1.1 * 0.015
    // from0Start drawing200line separator
if ticker == "USDJPY"
    step_size := 100 * 0.015
var float start_value = close
var float up_number = close + step_size
var float low_number = close - step_size
// hline(3.14, title='Pi', color=color.blue, linestyle=hline.style_dotted, linewidth=2)
// plot(1)
// When the price breaks the upper limit, generate a buy signal
if close > up_number
    // Generate buy signal
    strategy.entry(id = "Buy", direction = strategy.long)
    // Update new price range
    start_value := start_value + step_size
    up_number := start_value + step_size
    low_number := start_value - step_size
    strategy.close(id = "Sell")
// When the price falls below the lower limit, generate a sell signal
if close < low_number
    // Generate sell signal
    strategy.entry("Sell", strategy.short)
    // Update new price range
    start_value := start_value - step_size
    up_number := start_value + step_size
    low_number := start_value - step_size
    strategy.close(id = "Buy")

```

> Detail

https://www.fmz.com/strategy/474674

> Last Modified

2024-12-11 15:03:50
