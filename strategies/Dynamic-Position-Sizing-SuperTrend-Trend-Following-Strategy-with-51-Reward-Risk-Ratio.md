
> Name

Dynamic-Position-Sizing-SuperTrend-Trend-Following-Strategy-with-51-Reward-Risk-Ratio

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8ee706b3ef44a1e3fc8.png)
![IMG](https://www.fmz.com/upload/asset/2d8924941a28e9b531393.png)




## Overview

The Dynamic Position Sizing SuperTrend Trend-Following Strategy with 5:1 Reward-Risk Ratio is an advanced trend-following system based on the SuperTrend indicator that combines trend identification with precise capital management techniques by dynamically calculating position sizes to control risk. The core features of this strategy include utilizing ATR (Average True Range) to determine market volatility, grouping trades in the same direction, and establishing a fixed 5:1 reward-to-risk ratio for each trade group. The system supports multiple pyramiding entries in the same direction while maintaining strict risk management, with each entry risking only 1% of the account equity. This design allows the strategy to fully capitalize on strong trends while maintaining low risk levels.

## Strategy Principles

This strategy is based on the SuperTrend indicator's trend determination mechanism, combined with advanced techniques of grouped trading and dynamic position management. The main working principles are as follows:

1. **SuperTrend Indicator Calculation**: First, the ATR value is calculated, then basic upper and lower bands are obtained by adding and subtracting the ATR multiplier from the midpoint price (HL2). The key innovation lies in using recursive smoothing techniques to calculate the final bands, which improves the indicator's stability and reliability.

2. **Trend Determination Logic**: The trend is determined by comparing the closing price with the previous final bands. When the closing price breaks above the upper band, the trend turns upward; when it breaks below the lower band, the trend turns downward; otherwise, the original trend is maintained.

3. **Signal Generation Mechanism**: Buy signals are generated when the trend changes from downward to upward; sell signals are generated when the trend changes from upward to downward.

4. **Grouped Trade Management**: The strategy groups trades in the same direction and records the initial stop level (SuperTrend value) for each group. This allows the system to uniformly manage multiple related trades, improving capital efficiency.

5. **Dynamic Position Calculation**: The position size for each trade is calculated according to the formula `math.floor(strategy.equity * 0.01 / stopDistance)`, ensuring that each additional entry risks only 1% of the account.

6. **Risk-Reward Setup**: The system automatically sets a 5:1 risk-reward ratio for each trade group, with the profit target set at 5 times the stop distance, significantly improving the strategy's expected return.

7. **Intelligent Exit Mechanism**: Includes three exit conditions: stop loss (initial SuperTrend level), take profit (5 times stop distance), and conditional exits during trend reversals (accepting loss, reaching profit target, or moving to breakeven).

## Strategy Advantages

This strategy has several significant advantages:

1. **Scientific Risk Control**: Through dynamic position adjustment, each trade risks only 1% of total capital, effectively controlling downside risk for individual trades.

2. **Enhanced Trend Tracking Capability**: The grouped trading mechanism allows the system to enter multiple times in the same trend, capturing more profit from strong, sustained trends.

3. **Optimized Risk-Reward Ratio**: The fixed 5:1 risk-reward setting ensures that successful trades yield far greater returns than losses from unsuccessful trades, improving expected returns over the long term.

4. **Flexible Position Management**: Position sizes are dynamically calculated based on current market volatility and account size, avoiding the risk imbalance problems of fixed position sizes.

5. **Intelligent Reversal Management**: During trend reversals, the system intelligently chooses exit methods based on current profit/loss status, including accepting losses, taking profits, or moving to breakeven before entering in the new direction.

6. **Recursively Smoothed SuperTrend**: The recursive calculation of final bands reduces false signals and improves the reliability of trend determination.

7. **Fully Automated Operation**: All parameters and conditions of the strategy are clearly defined, suitable for fully automated trading, reducing human intervention and emotional influence.

## Strategy Risks

Despite its excellent design, the strategy still presents some potential risks:

1. **Excessive Pyramiding Risk**: Although each additional entry risks only 1% of capital, the pyramiding setting of 500 could lead to excessively large positions in strong one-directional trends. It is recommended to lower the pyramiding parameter based on individual risk tolerance.

2. **Rapid Reversal Risk**: During severe market fluctuations, prices may gap beyond stop levels, resulting in actual losses exceeding the expected 1%. Consider reducing the risk percentage or adding additional volatility filters in highly volatile markets.

3. **Parameter Sensitivity**: Strategy performance is sensitive to ATR period and multiplier parameters, with different parameter combinations performing differently under various market conditions. Thorough parameter optimization and backtesting are recommended to find optimal parameters for specific markets.

4. **Trend Market Dependency**: As a trend-following system, this strategy may generate frequent losing trades in range-bound, oscillating markets. Consider adding market environment filters to enable the strategy only when trends are clearly defined.

5. **Capital Management Risk**: Although single-trade risk is limited to 1%, multiple simultaneously active trade groups may temporarily cause total risk to exceed acceptable levels. Consider setting additional overall risk limits, such as maximum allowable simultaneous losses not exceeding 5% of the account.

## Strategy Optimization Directions

Based on the strategy's design and potential risks, the following optimization directions can be considered:

1. **Add Trend Strength Filter**: Combine with ADX or similar indicators and only trade when the trend is strong enough to reduce false signals in oscillating markets. This can be implemented by adding `adxValue = ta.adx(14)` calculation and setting `strongTrend = adxValue > 25` as an additional entry condition.

2. **Dynamic Risk-Reward Ratio**: Automatically adjust the risk-reward ratio based on market volatility, using higher ratios during low volatility periods and lower ratios during high volatility periods. This can be adjusted by calculating the ratio of long-term ATR to current ATR.

3. **Add Partial Profit-Taking Mechanism**: Design a system for taking partial profits, such as taking 25% profit at 2x stop distance, another 25% at 3x, and reserving 50% of the position for the 5x target. This can improve overall profitability.

4. **Intelligent Pyramiding Condition Optimization**: Add additional conditions for pyramiding beyond trend signals, such as requiring specific favorable movements before allowing additional entries, avoiding excessive pyramiding during price consolidation.

5. **Integrate Multi-Timeframe Analysis**: Add higher timeframe trend confirmation and only trade when trends across multiple timeframes align, improving entry quality.

6. **Add Maximum Exposure Limit**: Set an upper limit on total account risk exposure, temporarily suspending new entry signals once the limit (e.g., 5% of total capital) is reached, until risk is reduced.

7. **Optimize SuperTrend Calculation**: Consider using a combination of SuperTrend indicators with various periods or multipliers, improving trend determination accuracy through a voting system.

## Summary

The Dynamic Position Sizing SuperTrend Trend-Following Strategy with 5:1 Reward-Risk Ratio is a highly refined trend-following system that perfectly combines precise trend identification with scientific capital management. Through dynamic position calculation, grouped trade management, and optimized 5:1 risk-reward settings, the strategy maximizes trend-capturing ability while controlling risk.

The core advantage of this strategy lies in its intelligent capital management system, ensuring that each entry risks only a fixed percentage while allowing multiple entries in strong trends to enhance returns. The optimized SuperTrend indicator calculation improves the reliability of trend determination, while diversified exit mechanisms ensure effective protection of profits.

Despite some potential risks, such as possible excessive pyramiding and dependency on trending markets, these risks can be effectively managed through the suggested optimization measures, such as adding trend strength filters, dynamically adjusting risk-reward ratios, and setting maximum exposure limits.

For traders seeking scientific, systematic trend-following methods, this strategy provides a solid framework that can be applied directly or used as a foundation for further customization. With careful parameter selection and continuous strategy monitoring, this system has the potential to achieve stable long-term performance across various market environments.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-03-31 00:00:00
end: 2025-03-29 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"ETH_USDT"}]
*/

//@version=6
strategy("Grouped SuperTrend Strategy 5x – All Signals", overlay=true, initial_capital=100000, default_qty_type=strategy.fixed, default_qty_value=0, pyramiding=500, calc_on_order_fills=true)

// INPUTS
atrPeriod     = input.int(10, title="ATR Period")
atrMultiplier = input.float(3.0, title="ATR Multiplier")

// CALCULATE ATR & BASIC BANDS
atrValue    = ta.atr(atrPeriod)
hl2         = (high + low) / 2
upperBasic  = hl2 + atrMultiplier * atrValue
lowerBasic  = hl2 - atrMultiplier * atrValue

// CALCULATE FINAL BANDS (recursive smoothing)
var float finalUpperBand = na
var float finalLowerBand = na
finalUpperBand := na(finalUpperBand[1]) ? upperBasic : (upperBasic < finalUpperBand[1] or close[1] > finalUpperBand[1] ? upperBasic : finalUpperBand[1])
finalLowerBand := na(finalLowerBand[1]) ? lowerBasic : (lowerBasic > finalLowerBand[1] or close[1] < finalLowerBand[1] ? lowerBasic : finalLowerBand[1])

// DETERMINE TREND
var int trend = 1
trend := nz(trend[1], 1)
if close > finalUpperBand[1]
    trend := 1
else if close < finalLowerBand[1]
    trend := -1
else
    trend := nz(trend[1], 1)
    
// SUPER TREND VALUE: For an uptrend use finalLowerBand, for a downtrend use finalUpperBand.
superTrend = trend == 1 ? finalLowerBand : finalUpperBand

// SIGNALS: A change in trend generates a signal.
buySignal  = (trend == 1 and nz(trend[1], 1) == -1)
sellSignal = (trend == -1 and nz(trend[1], 1) == 1)

// Plot SuperTrend
plot(superTrend, color = trend == 1 ? color.green : color.red, title="SuperTrend")

// POSITION SIZING FUNCTION: Risk 1% of equity per signal based on the stop distance.
calc_qty(stopDistance) =>
    stopDistance > 0 ? math.floor(strategy.equity * 0.01 / stopDistance) : 0

// ─── GROUPING VARIABLES ─────────────────────────────
// When a new group trade is initiated (position goes from flat to non‑zero),
// record the SuperTrend value as the group's initial stop.
var float groupInitialStop = na
if strategy.position_size == 0
    groupInitialStop := na
if strategy.position_size != 0 and strategy.position_size[1] == 0
    groupInitialStop := superTrend

// Declare groupStopDistance and groupProfitTarget with explicit type.
var float groupStopDistance = na
var float groupProfitTarget = na
if strategy.position_size > 0
    groupStopDistance := strategy.position_avg_price - groupInitialStop
    groupProfitTarget := strategy.position_avg_price + 5 * groupStopDistance
else if strategy.position_size < 0
    groupStopDistance := groupInitialStop - strategy.position_avg_price
    groupProfitTarget := strategy.position_avg_price - 5 * groupStopDistance

// ─── ENTRY LOGIC ─────────────────────────────
// Every SuperTrend signal is taken.
// For same‑direction signals (or when flat), add to the group.
// For reversal signals, exit the existing group per our conditions and then enter the new direction.

// LONG ENTRIES
if buySignal
    // Reversal: if currently short, exit short first.
    if strategy.position_size < 0
        // For shorts, a loss is when close > avg entry.
        if close > strategy.position_avg_price
            strategy.close("Short", comment="Short Reversal Loss Exit")
        // For shorts, profit when price is below the profit target.
        else if close <= groupProfitTarget
            strategy.close("Short", comment="Short Reversal Profit Target Exit")
        else
            // Otherwise, update exit to break-even.
            strategy.exit("Short_BE", from_entry="Short", stop=strategy.position_avg_price, comment="Short BE Trailing")
        // Enter new long trade.
        stopDist = close - superTrend
        qty = calc_qty(stopDist)
        if qty > 0
            strategy.entry("Long", strategy.long, qty=qty, comment="Long Entry on Reversal")
        // Reset group initial stop for new group.
        groupInitialStop := superTrend
    else
        // Flat or already long – add to the long group.
        stopDist = close - superTrend
        qty = calc_qty(stopDist)
        if qty > 0
            strategy.entry("Long", strategy.long, qty=qty, comment="Long Add Entry")

// SHORT ENTRIES
if sellSignal
    if strategy.position_size > 0
        // Reversal: if currently long, exit long first.
        if close < strategy.position_avg_price
            strategy.close("Long", comment="Long Reversal Loss Exit")
        else if close >= groupProfitTarget
            strategy.close("Long", comment="Long Reversal Profit Target Exit")
        else
            strategy.exit("Long_BE", from_entry="Long", stop=strategy.position_avg_price, comment="Long BE Trailing")
        // Enter new short trade.
        stopDist = superTrend - close
        qty = calc_qty(stopDist)
        if qty > 0
            strategy.entry("Short", strategy.short, qty=qty, comment="Short Entry on Reversal")
        groupInitialStop := superTrend
    else
        // Flat or already short – add to the short group.
        stopDist = superTrend - close
        qty = calc_qty(stopDist)
        if qty > 0
            strategy.entry("Short", strategy.short, qty=qty, comment="Short Add Entry")

// ─── EXIT ORDERS ─────────────────────────────
// Set default aggregated exit orders based on the group's initial stop and profit target.
if strategy.position_size > 0
    strategy.exit("LongExit", from_entry="Long", stop=groupInitialStop, limit=groupProfitTarget)
if strategy.position_size < 0
    strategy.exit("ShortExit", from_entry="Short", stop=groupInitialStop, limit=groupProfitTarget)

```

> Detail

https://www.fmz.com/strategy/488851

> Last Modified

2025-03-31 11:53:06
