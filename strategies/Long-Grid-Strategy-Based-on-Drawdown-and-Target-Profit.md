
> Name

Long-Grid-Strategy-Based-on-Drawdown-and-Target-Profit

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/ce6cab9b294d00c93a.png)


#### Overview
This strategy is a grid trading system that adds positions based on price drops and closes positions when reaching a fixed profit target. The core logic is to buy when the market drops to a preset percentage, close all positions when the price rebounds to the target profit, and generate returns by repeatedly executing this process. This strategy is particularly suitable for capturing short-term rebounds in oscillating markets.

#### Strategy Principle
The strategy employs a combined mechanism of grid trading and directional take-profit:
1. Initial Position: After the set start time, the system takes the first position at the current price when triggered.
2. Position Adding Mechanism: Additional buying is triggered when the price drops beyond the preset percentage (default 5%) relative to the initial entry price.
3. Position Closing Mechanism: When the price rises above the preset profit target (default 5%) relative to the initial entry price, the system closes all positions.
4. Statistical Tracking: The system tracks trade counts and cumulative profits in real-time, displaying them dynamically on the chart.

#### Strategy Advantages
1. High Automation: The strategy is fully systematic, requiring no manual intervention and can operate 24/7.
2. Risk Diversification: The batch position building approach effectively reduces single-entry risks.
3. Clear Profit Targets: Fixed profit targets ensure immediate profit-taking when reached.
4. High Adaptability: Parameter adjustments allow adaptation to different market environments and trading instruments.
5. Strong Execution: Clear strategy logic eliminates subjective emotional influences.

#### Strategy Risks
1. Trend Risk: In continuously declining markets, repeated position adding may increase losses.
2. Capital Management Risk: Without proper position control, excessive position adding may lead to high capital utilization.
3. Slippage Risk: Severe slippage during volatile market conditions may affect strategy performance.
4. Parameter Sensitivity: Strategy effectiveness is sensitive to parameter settings, requiring timely adjustments in different market environments.

#### Strategy Optimization Directions
1. Dynamic Stop Loss: Recommend adding ATR or volatility-based dynamic stop-loss mechanisms to prevent significant drawdowns.
2. Position Management: Introduce equity-based dynamic position management for more rational capital utilization.
3. Market Selection: Add trend identification indicators to pause strategy operation in trending markets.
4. Profit Target Optimization: Design dynamic profit targets that self-adjust based on market volatility.
5. Position Adding Optimization: Design progressive position sizing to avoid excessive early positions.

#### Summary
This is a structurally simple but practical grid trading strategy that builds positions in batches at preset price drops and uniformly closes positions when reaching profit targets. The strategy's core advantages lie in its execution certainty and risk diversification, but market environment selection and parameter optimization are crucial during implementation. There is significant optimization potential through adding dynamic stop-losses and improving position management. For live trading, thorough backtesting and parameter adjustment based on actual market conditions are recommended.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2025-01-04 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Buy Down 5%, Sell at 5% Profit", overlay=true, default_qty_type=strategy.fixed, default_qty_value=1)

// Inputs
initial_date = input(timestamp("2024-01-01 00:00:00"), title="Initial Purchase Date")
profit_target = input.float(5.0, title="Profit Target (%)", minval=0.1)   // Target profit percentage
rebuy_drop = input.float(5.0, title="Rebuy Drop (%)", minval=0.1)        // Drop percentage to rebuy

// Variables
var float initial_price = na             // Initial purchase price
var int entries = 0                      // Count of entries
var float total_profit = 0               // Cumulative profit
var bool active_trade = false            // Whether an active trade exists

// Entry Condition: Buy on or after the initial date
if not active_trade
    initial_price := close
    strategy.entry("Buy", strategy.long)
    entries += 1
    active_trade := true

// Rebuy Condition: Buy if price drops 5% or more from the initial price
rebuy_price = initial_price * (1 - rebuy_drop / 100)
if active_trade and close <= rebuy_price
    strategy.entry("Rebuy", strategy.long)
    entries += 1

// Exit Condition: Sell if the price gives a 5% profit on the initial investment
target_price = initial_price * (1 + profit_target / 100)
if active_trade and close >= target_price
    strategy.close_all(comment="Profit Target Hit")
    active_trade := false
    total_profit += profit_target

// Display information on the chart
plotshape(series=close >= target_price, title="Target Hit", style=shape.labelup, location=location.absolute, color=color.green, text="Sell")
plotshape(series=close <= rebuy_price, title="Rebuy", style=shape.labeldown, location=location.absolute, color=color.red, text="Rebuy")

// Draw statistics on the chart
var label stats_label = na
if (na(stats_label))
    stats_label := label.new(x=bar_index, y=close, text="", style=label.style_none, size=size.small)

label.set_xy(stats_label, bar_index, close)
label.set_text(stats_label, "Entries: " + str.tostring(entries) + "\nTotal Profit: " + str.tostring(total_profit, "#.##") + "%")

```

> Detail

https://www.fmz.com/strategy/477600

> Last Modified

2025-01-06 16:29:17
