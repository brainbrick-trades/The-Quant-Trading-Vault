
> Name

Adaptive-Cost-Average-Dynamic-Grid-Strategy-Advanced-Quantitative-Trading-System-Based-on-DCA-and-Martingale-Principles

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d83c586fb8fbf1a1122e.png)
![IMG](https://www.fmz.com/upload/asset/2d8c78dba8a4835557b84.png)





#### Overview
The Adaptive Cost-Average Dynamic Grid Strategy is a comprehensive quantitative trading strategy that combines grid trading, Dollar-Cost Averaging (DCA), and Martingale principles. This strategy primarily utilizes a multi-layered buy grid and a dynamically adjusted safety order system to respond to market volatility, aiming to achieve more stable returns in fluctuating markets. The core concept is to establish price steps, gradually increase positions as prices decline, thereby reducing the average holding cost, and then close all positions for profit when prices rebound to predetermined profit targets.

#### Strategy Principles
The strategy operates based on multi-layered intelligent buy grids and preset profit targets. The specific principles are as follows:

1. **Initial Order and Grid Construction**: The strategy first places an initial buy order based on trigger conditions (instant, price, or RSI indicator), which serves as the starting point for the grid. The system then calculates the next buy point, forming the first layer of the grid.

2. **Safety Order Mechanism**: When the price falls to a preset grid point, the system triggers a safety order, with the purchase amount increasing according to the Martingale principle (controlled by the amount multiplier i_multiplier). After each safety order is executed, the system recalculates the average holding price and dynamically adjusts the trigger price for the next safety order.

3. **Dynamic Grid Spacing**: The strategy employs non-equidistant grids, with the grid spacing expanding as the price falls (controlled by the price step multiplier i_stepMulti). This helps avoid depleting funds too early in a continuously declining market.

4. **Profit-Taking and Stop-Loss Mechanisms**: When the market price rises to the average cost plus the preset profit percentage (i_tpPct), the strategy closes all positions, completing a trading cycle. Additionally, the strategy offers an optional stop-loss feature that can trigger a complete closeout to control risk when the price falls to the average cost minus the preset stop-loss percentage (i_slPct).

5. **Cycle Management**: A complete trading cycle begins when trigger conditions are met and ends when either the profit target is reached or the stop-loss is triggered. Each cycle is independent, and the system automatically initiates new cycles based on specified conditions.

#### Strategy Advantages
1. **Cost Averaging Effect**: By gradually increasing positions as prices fall, the strategy can significantly reduce the average holding cost, allowing for profit even with relatively small price rebounds.

2. **High Adaptability**: The strategy offers multiple startup condition options (instant, price trigger, RSI indicator), which can be flexibly adjusted based on different market environments. The RSI indicator is particularly helpful in identifying overbought/oversold areas, improving the accuracy of entry timing.

3. **Efficient Capital Utilization**: Through the Martingale system's capital allocation method, the strategy only gradually invests more funds as prices fall, avoiding the risk of committing all capital at once.

4. **Highly Customizable Parameters**: The strategy provides a rich set of parameter settings, including grid step size, profit targets, safety order quantity, amount multipliers, etc., allowing users to personalize adjustments based on their risk preferences and market expectations.

5. **Visual Support**: The strategy displays the average price, profit target line, stop-loss line, and all safety order price levels on the chart, providing intuitive references for strategy monitoring and adjustment.

#### Strategy Risks
1. **Risk in Continuously Declining Markets**: In continuously declining markets, even with a set limit on the number of safety orders, the strategy may consume significant capital without achieving profit. Especially during prolonged bear markets, this could lead to long-term capital lockup.

2. **Capital Management Pressure**: The Martingale system requires each subsequent safety order to double in amount, which can lead to rapidly growing capital requirements that might exceed a trader's capacity.

3. **Parameter Optimization Challenges**: The effectiveness of the strategy highly depends on the reasonableness of parameter settings. Optimal parameters may vary greatly across different market environments, requiring continuous backtesting and optimization.

4. **Stop-Loss and Risk Control**: By default, the strategy does not enable the stop-loss mechanism, potentially facing significant losses in extreme market conditions. Even with stop-loss enabled, market gaps might prevent execution at the expected price.

5. **Liquidity Risk**: In low-liquidity markets, numerous safety orders may not execute at expected prices, causing actual results to deviate from backtesting outcomes.

#### Strategy Optimization Directions
1. **Dynamic Risk Management**: The current strategy uses a fixed stop-loss percentage, which could be improved to a dynamic stop-loss mechanism based on market volatility. For example, integrating the ATR indicator to adjust stop-loss distances, setting looser stops in high-volatility markets and tighter stops in low-volatility markets.

2. **Multi-Indicator Filtering**: The current strategy only uses RSI as an optional startup condition. More technical indicators could be introduced, such as MACD, Bollinger Bands, or moving average systems, to build a more comprehensive market state assessment mechanism and avoid initiating new cycles in unsuitable market conditions.

3. **Adaptive Grid System**: Grid spacing and safety order quantities could be dynamically adjusted based on historical volatility, setting wider grid spacing and more safety orders in high-volatility markets, and correspondingly reducing them in low-volatility markets, to better adapt to different market environments.

4. **Partial Profit-Taking Mechanism**: The current strategy only has a complete closeout mechanism. A partial profit-taking function could be added, closing part of the position when the price reaches certain levels, both securing partial profits and retaining upside potential.

5. **Time Factor Consideration**: Time-based stop-loss or adjustment mechanisms could be added, such as adjusting profit targets or ending cycles early if a cycle lasts too long, avoiding long-term capital lockup.

#### Summary
The Adaptive Cost-Average Dynamic Grid Strategy creates a trading system that automatically adjusts cost basis during price fluctuations by combining grid trading, DCA, and Martingale principles. This strategy is particularly suitable for market environments with price oscillations, effectively reducing average holding costs and enhancing profit potential from small price movements.

However, when using this strategy, careful assessment of capital requirements and market trends is necessary, especially in strongly trending markets. Reasonably setting the maximum number of safety orders, amount multipliers, and price step multipliers is key to controlling risk. Through continuous parameter optimization and the addition of dynamic risk management mechanisms, this strategy can become an effective tool in volatile markets.

For optimal results, traders are advised to conduct thorough historical backtesting before live application, adjust parameters for different market environments and trading instruments, and always maintain sufficient capital reserves to handle extreme market situations.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-29 00:00:00
end: 2024-04-17 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"ETH_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// @HannSo1o TG
// @singoslab CIS Comunity in TG
//The strategy was created to select the optimal settings for a spot bot on the OKX exchange.
//Spot DCA + Martingale.
//The strategy is not designed for launching a bot with tradingview, only for selecting optimal settings, and the bot must be launched separately on the exchange itself, 
//in the section
//https://www.okx.com/ru/trade-spot-strategy/eth-usdt#ordtype=spot_dca

//@version=6
strategy("OKX _Spot DCA + Martingale - Strategy with DCA Grid", overlay=true, commission_type=strategy.commission.percent, commission_value=0.1, slippage=3, default_qty_type=strategy.cash, default_qty_value=100, initial_capital=10000, currency=currency.USD, process_orders_on_close=true)

// Input parameters
i_priceStepPct  = input.float(1.0, "Price Step (%)", minval=0.1, group="1. Grid Parameters") / 100
i_tpPct         = input.float(1.0, "Take Profit Target per Cycle (%)", minval=0.1, group="1. Grid Parameters") / 100

i_initialOrder  = input.float(100.0, "Initial Order Amount (USDT)", minval=1, group="2. Volume Management")
i_safetyOrder   = input.float(50.0, "Safety Order Amount (USDT)", minval=1, group="2. Volume Management")
i_maxSafety     = input.int(5, "Max Number of Safety Orders", minval=1, maxval=20, group="2. Volume Management") // Added maxval=20

i_startCond     = input.string("Instantly", "Start Conditions", options=["Instantly", "Price", "RSI"], group="3. Activation Conditions")
i_multiplier    = input.float(2.0, "Amount Multiplier", minval=1, group="4. Multipliers")
i_stepMulti     = input.float(1.5, "Price Step Multiplier", minval=1, group="4. Multipliers")

i_slEnabled     = input.bool(false, "Enable Stop Loss", group="5. Protection")
i_slPct         = input.float(5.0, "Stop Loss Target (%)", minval=0.1, group="5. Protection") / 100

// RSI Parameters
i_rsiPeriod     = input.int(14, "RSI Period", group="6. RSI Settings")
i_rsiSource     = input(close, "RSI Source", group="6. RSI Settings")
i_rsiTrigger    = input.string("Down", "Trigger Condition", options=["Up", "Down"], group="6. RSI Settings")
i_rsiThreshold  = input.float(30, "Trigger Threshold", minval=1, maxval=100, group="6. RSI Settings")
i_rsiTF         = input.timeframe("3", "Timeframe", group="6. RSI Settings")

// Strategy State
var int cycleCount = 0
var float avgPrice = na
var float totalQty = 0.0
var int safetyCount = 0
var bool cycleActive = false
var float nextOrderPrice = na
var float entryPrice = na // Entry price for the cycle

// Indicator Calculations
rsiValue = request.security(syminfo.tickerid, i_rsiTF, ta.rsi(i_rsiSource, i_rsiPeriod))
triggerPrice = low * (1 - i_priceStepPct)

// Activation Conditions
startCondition = switch i_startCond
    "Instantly" => true
    "Price"     => close <= triggerPrice
    "RSI"      => i_rsiTrigger == "Down" ? ta.crossunder(rsiValue, i_rsiThreshold) : ta.crossover(rsiValue, 100 - i_rsiThreshold)

// Cycle Management Logic

if not cycleActive and startCondition
    cycleCount := cycleCount + 1
    strategy.entry("InitBuy", strategy.long, i_initialOrder)
    avgPrice := close
    totalQty := i_initialOrder / close
    safetyCount := 0
    cycleActive := true
    nextOrderPrice := close * (1 - i_priceStepPct)
    entryPrice := close // Save entry price
    
if cycleActive
    // Check for adding safety orders
    if low <= nextOrderPrice and safetyCount < i_maxSafety
        safetyCount := safetyCount + 1
        orderSize = i_safetyOrder * math.pow(i_multiplier, safetyCount)
        strategy.order("SafetyBuy_" + str.tostring(safetyCount), strategy.long, orderSize / close, limit=nextOrderPrice)
        totalQty := totalQty + (orderSize / nextOrderPrice)
        avgPrice := (avgPrice * (totalQty - (orderSize / nextOrderPrice)) + nextOrderPrice * (orderSize / nextOrderPrice)) / totalQty
        nextOrderPrice := nextOrderPrice * (1 - i_priceStepPct * math.pow(i_stepMulti, safetyCount))
    
    // Calculate exit levels
    tpLevel = avgPrice * (1 + i_tpPct)
    slLevel = avgPrice * (1 - i_slPct)
    
    // Check take profit
    if high >= tpLevel
        strategy.close_all()
        cycleActive := false
    
    // Check stop loss
    if i_slEnabled and low <= slLevel
        strategy.close_all()
        cycleActive := false

// Function to calculate safety order levels
getLevel(n) =>
    level = entryPrice
    for i = 0 to n-1
        step = i_priceStepPct * math.pow(i_stepMulti, i)
        level := level * (1 - step)
    level

// Visualization
plot(cycleActive ? avgPrice : na, "Average Price", color.green, 2)
plot(cycleActive ? avgPrice * (1 + i_tpPct) : na, "Take Profit", color.teal, 2)
plot(i_slEnabled and cycleActive ? avgPrice * (1 - i_slPct) : na, "Stop Loss", color.red, 2)

// Display safety order grid
plot(cycleActive ? entryPrice : na, "Entry Price", color.purple, 2, plot.style_linebr)

// Dynamic display of up to 20 grid levels
plot(cycleActive and i_maxSafety >= 1 ? getLevel(1) : na, "Safety Order 1", color.blue, 2)
plot(cycleActive and i_maxSafety >= 2 ? getLevel(2) : na, "Safety Order 2", color.blue, 2)
plot(cycleActive and i_maxSafety >= 3 ? getLevel(3) : na, "Safety Order 3", color.blue, 2)
plot(cycleActive and i_maxSafety >= 4 ? getLevel(4) : na, "Safety Order 4", color.blue, 2)
plot(cycleActive and i_maxSafety >= 5 ? getLevel(5) : na, "Safety Order 5", color.blue, 2)
plot(cycleActive and i_maxSafety >= 6 ? getLevel(6) : na, "Safety Order 6", color.blue, 2)
plot(cycleActive and i_maxSafety >= 7 ? getLevel(7) : na, "Safety Order 7", color.blue, 2)
plot(cycleActive and i_maxSafety >= 8 ? getLevel(8) : na, "Safety Order 8", color.blue, 2)
plot(cycleActive and i_maxSafety >= 9 ? getLevel(9) : na, "Safety Order 9", color.blue, 2)
plot(cycleActive and i_maxSafety >=10 ? getLevel(10) : na, "Safety Order 10", color.blue, 2)
plot(cycleActive and i_maxSafety >=11 ? getLevel(11) : na, "Safety Order 11", color.blue, 2)
plot(cycleActive and i_maxSafety >=12 ? getLevel(12) : na, "Safety Order 12", color.blue, 2)
plot(cycleActive and i_maxSafety >=13 ? getLevel(13) : na, "Safety Order 13", color.blue, 2)
plot(cycleActive and i_maxSafety >=14 ? getLevel(14) : na, "Safety Order 14", color.blue, 2)
plot(cycleActive and i_maxSafety >=15 ? getLevel(15) : na, "Safety Order 15", color.blue, 2)
plot(cycleActive and i_maxSafety >=16 ? getLevel(16) : na, "Safety Order 16", color.blue, 2)
plot(cycleActive and i_maxSafety >=17 ? getLevel(17) : na, "Safety Order 17", color.blue, 2)
plot(cycleActive and i_maxSafety >=18 ? getLevel(18) : na, "Safety Order 18", color.blue, 2)
plot(cycleActive and i_maxSafety >=19 ? getLevel(19) : na, "Safety Order 19", color.blue, 2)
plot(cycleActive and i_maxSafety >=20 ? getLevel(20) : na, "Safety Order 20", color.blue, 2)
```

> Detail

https://www.fmz.com/strategy/484107

> Last Modified

2025-02-28 10:26:54
