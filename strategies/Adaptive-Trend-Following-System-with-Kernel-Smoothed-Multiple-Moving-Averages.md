
> Name

Adaptive-Trend-Following-System-with-Kernel-Smoothed-Multiple-Moving-Averages

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d87753a1b09d6a11a26e.png)
![IMG](https://www.fmz.com/upload/asset/2d85b0177d297f29d4fa4.png)





## Overview
This Adaptive Trend Following System with Kernel-Smoothed Multiple Moving Averages is an advanced quantitative trading strategy that integrates five custom moving averages, multiple layers of filtering, and confirmation mechanisms to identify and capitalize on sustained market trends. The strategy employs kernel smoothing techniques instead of traditional moving averages, providing more flexible smoothing effects and adaptive capabilities that can adjust to various market conditions and timeframes.

Core functionalities include: utilizing a "ribbon" of five moving averages to visually represent the current market trend; reducing noise and false signals through an RSI filter, trend strength filter, and trend confirmation period; triggering entry signals only when specific conditions are met; and employing multiple exit options (including percentage trailing stop, ATR trailing stop, ATR take profit, and hard stop loss) to manage risk and protect profits.

## Strategy Principles
The core logic of this strategy revolves around the following key components:

1. **Kernel-Smoothed Moving Averages**: The strategy uses kernel smoothing techniques instead of standard moving averages, providing more flexible and adaptive smoothing than traditional MAs. It supports three kernel types:
   - Beta Kernel: The most versatile option, allowing independent control of positive and negative lag through the `alpha` and `beta` parameters, making the MA react differently to price increases and decreases.
   - Gaussian Kernel: Creates a bell-shaped weighting, with the `bandwidth` parameter controlling the width of the bell curve.
   - Epanechnikov Kernel: Similar to the Gaussian kernel but with a slightly different shape, also using a `bandwidth` parameter.

2. **MA Ribbon**: The five MAs form a "ribbon" on the chart, with their alignment and relative positions providing a visual indication of trend strength and direction.

3. **Crossover Detection**: The strategy monitors the crossovers between consecutive MAs in the ribbon, with users able to specify how many crossovers are required to generate a potential signal.

4. **RSI Filter**: This helps avoid entries during overextended market conditions. For long entries, the RSI must be below the oversold level; for short entries, it must be above the overbought level.

5. **Trend Strength Filter**: This unique filter uses the RSI of one of the moving averages to measure the strength of the trend, ensuring that trades are entered in the direction of a strong, established trend.

6. **Trend Confirmation**: To further reduce false signals, the strategy requires that the entry conditions (MA crossovers, RSI, and trend strength) be met for a specified number of consecutive bars before a trade is actually triggered.

7. **Exit Logic**: The strategy prioritizes exits in the following order: Hard Stop Loss, Trailing Stop (Percentage or ATR-based), and Take Profit (ATR-based). This ensures that losses are minimized and profits are protected.

## Strategy Advantages
1. **Highly Customizable Kernel Smoothing**: The use of kernel smoothing, especially the Beta kernel, provides a level of control over MA responsiveness that is not available with standard MAs. This allows for a much more adaptive and nuanced approach to trend following.

2. **Combined Trend Strength and Confirmation**: The combination of the trend strength filter (using the RSI of an MA) and the trend confirmation period provides a robust filtering mechanism that goes beyond simple MA crossovers or RSI readings. This helps to filter out weak trends and whipsaws.

3. **Multiple, Prioritized Exit Options**: The strategy's exit logic is sophisticated, offering a combination of fixed and dynamic stops and take profit levels. The prioritization ensures that the most conservative exit (hard stop) is triggered first, followed by the trailing stops, and finally the take profit.

4. **Comprehensive Input Grouping**: All inputs have been sorted into groups that control certain aspects of the strategy, allowing users to easily and quickly locate and adjust inputs as needed.

5. **Trade Direction Control**: Unlike many strategies, this one allows users to independently enable or disable long and short trades.

6. **All-in-one Trend System**: This indicator combines multiple aspects needed for trading: entry signals, stop loss calculations, and take profit calculations.

## Strategy Risks
1. **Parameter Optimization Challenges**: With the large number of parameters in the strategy, there is a risk of overfitting. Over-tuning parameters may result in a strategy that performs well in backtesting but fails in live trading. It's recommended to perform robust cross-validation and out-of-sample testing to ensure parameter settings are generalizable.

2. **Delayed Reaction to Trend Changes**: While the strategy is designed to identify sustained trends, it may not react quickly enough to sharp market reversals, leading to partial retracements. The sensitivity to trend changes versus filtering out noise can be balanced by adjusting MA lengths and kernel parameters.

3. **MA Crossover False Signals**: Even with multiple layers of filtering, false signals can still occur in ranging markets. It's advisable to use this strategy in defined trending markets or increase the trend confirmation period to reduce false signals.

4. **Premature Stop Triggering**: In highly volatile markets, stops may be triggered prematurely, causing missed opportunities when price retraces and the trend resumes. Consider ATR-based stops with appropriate adjustments to accommodate market volatility.

5. **Complexity Risk**: The complexity of the strategy may make troubleshooting and real-time monitoring difficult. Start with a simpler configuration and gradually add complexity, ensuring a thorough understanding of each component's role.

## Strategy Optimization Directions
1. **Timeframe Adaptability**: The current strategy could be further optimized to automatically adjust parameters based on different timeframes. For example, an automatic parameter adjustment feature based on the timeframe could be added to make the strategy effective on daily, hourly, or minute charts.

2. **Market Environment Detection**: Add an automatic detection mechanism for market environments (trending, ranging, or high volatility) and adjust trading parameters accordingly. For example, increase filter strength or adjust profit targets in ranging markets, and relax filtering conditions in trending markets.

3. **Dynamic RSI Thresholds**: Design the RSI overbought/oversold thresholds to be dynamic rather than static, automatically adjusting based on recent market volatility. This can enhance the strategy's adaptability across different market conditions.

4. **Integrate Volatility Metrics**: Integrate the strategy with volatility indicators such as Bollinger Bandwidth to adjust stop losses and profit targets in high-volatility environments, reducing the risk of being shaken out of valid trends.

5. **Multi-timeframe Confirmation**: Add higher timeframe trend confirmation to ensure the trading direction aligns with the larger trend. For example, only trade when the daily trend is in the same direction as the hourly trend.

6. **Performance Monitoring and Adaptation**: Implement a real-time monitoring system for strategy performance, tracking metrics such as win rate, profit-to-loss ratio, and maximum drawdown, and automatically adjusting parameters or pausing trading when performance metrics fall below preset thresholds.

7. **Machine Learning Enhancement**: Explore integrating machine learning algorithms into the parameter optimization process, allowing the strategy to learn optimal parameter combinations from historical data and continuously improve as new data accumulates.

## Summary
The Adaptive Trend Following System with Kernel-Smoothed Multiple Moving Averages is a powerful and flexible trend following tool that combines the visual clarity of a moving average ribbon with the advanced filtering and risk management capabilities of kernel smoothing, RSI, trend strength, and multiple exit options. It's designed for traders who want a customizable and robust tool for identifying and trading sustained market trends.

The strategy's greatest strength lies in its high customizability and adaptability, making it capable of adjusting to various market conditions. Through kernel smoothing techniques, it offers more nuanced control than traditional moving averages, while its multiple layers of filtering and confirmation mechanisms help reduce false signals. At the same time, the comprehensive risk management system provides multiple exit strategies, ensuring losses are minimized and profits are protected.

However, users should be aware of the challenges in parameter optimization, avoid overfitting, and adjust the strategy according to specific market environments. It's recommended to conduct thorough backtesting and forward testing to ensure the strategy performs robustly under various market conditions. With regular evaluation and optimization, this strategy has the potential to become a valuable asset in a successful trend trader's toolkit.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-03-28 00:00:00
end: 2025-03-27 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"ETH_USDT"}]
*/

//@version=5
strategy("B4100 - NW Trend Ribbon Strategy", overlay=true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, commission_type = strategy.commission.percent, commission_value = 0.02)

// === Optimized Functions ===
f_calculate_beta_kernel(length, alpha, beta) =>
    kernel = array.new_float(length, 0)
    sum = 0.0
    for i = 0 to length - 1
        x = i / (length - 1)
        w = math.pow(x, alpha - 1) * math.pow(1 - x, beta - 1)
        array.set(kernel, i, w)
        sum += w
    for i = 0 to length - 1
        array.set(kernel, i, array.get(kernel, i) / sum)
    kernel

f_calculate_gaussian_kernel(length, bandwidth) =>
    kernel = array.new_float(length, 0)
    sum = 0.0
    for i = 0 to length - 1
        x = i / (length - 1)
        w = math.exp(-0.5 * math.pow((x - 0.5) / bandwidth, 2))
        array.set(kernel, i, w)
        sum += w
    for i = 0 to length - 1
        array.set(kernel, i, array.get(kernel, i) / sum)
    kernel

f_calculate_epanechnikov_kernel(length, bandwidth) =>
    kernel = array.new_float(length, 0)
    sum = 0.0
    for i = 0 to length - 1
        x = i / (length - 1)
        w = math.max(0.0, 1 - math.pow((x - 0.5) / bandwidth, 2))
        array.set(kernel, i, w)
        sum += w
    for i = 0 to length - 1
        array.set(kernel, i, array.get(kernel, i) / sum)
    kernel

f_apply_kernel_ma(src, kernel, length) =>
    sum = 0.0
    for i = 0 to length - 1
        sum += src[i] * array.get(kernel, i)
    sum

f_trend_strength(ma, length) =>
    ts = ta.rsi(ma, length) / 100
    ts

// === Inputs ===
src = input.source(close, title="Price Source", tooltip="Select the price data used for calculations.  'Close' is the most common, but you can also use 'Open', 'High', 'Low', 'HL2' (typical price), etc.")

// MA Parameters
maGroup = "Moving Average Settings"
maCrossoverGroup = "Moving Average Crossover Settings"
rsiFilterGroup = "RSI Filter Settings"
trendStrengthGroup = "Trend Strength Filter Settings"
trendConfirmGroup = "Trend Confirmation Settings"
trailingStopGroup = "Trailing Stop Settings"
atrTrailingStopGroup = "ATR Trailing Stop Settings"
atrTakeProfitGroup = "ATR Take Profit Settings"
hardStopGroup = "Hard Stop Loss Settings"
tradeDirectionGroup = "Trade Direction Control"

length1 = input.int(20, title="MA1 Length", minval=1, tooltip="Number of bars used to calculate the first Moving Average.", group=maGroup)
kernelType1 = input.string(title="MA1 Kernel Type", defval="Beta", options=["Beta", "Gaussian", "Epanechnikov"], tooltip="Select the type of smoothing kernel for MA1.  'Beta' allows for lag adjustment. 'Gaussian' and 'Epanechnikov' use a bandwidth.", group=maGroup)
alpha1  = input.float(3.0, title="MA1 Beta Kernel +Lag", minval=1, maxval=10, tooltip="For Beta kernel only: Higher values increase *positive* lag (MA reacts *slower* to price increases).", group=maGroup)
beta1   = input.float(3.0, title="MA1 Beta Kernel -Lag", minval=1, maxval=10, tooltip="For Beta kernel only: Higher values increase *negative* lag (MA reacts *slower* to price decreases).", group=maGroup)
bandwidth1 = input.float(0.3, title="MA1 Bandwidth", minval=0.1, maxval=10.0, tooltip="For Gaussian/Epanechnikov kernels:  Smaller values create a *tighter* fit to the price (more sensitive). Larger values create a *smoother*, less sensitive MA.", group=maGroup)

length2 = input.int(100, title="MA2 Length", minval=1, tooltip="Number of bars for the second Moving Average.", group=maGroup)
kernelType2 = input.string(title="MA2 Kernel Type", defval="Gaussian", options=["Beta", "Gaussian", "Epanechnikov"], tooltip="Kernel type for MA2 (see MA1 Kernel Type for details).", group=maGroup)
alpha2  = input.float(3.0, title="MA2 Beta Kernel +Lag", minval=1, maxval=10, tooltip="Beta kernel positive lag for MA2 (see MA1 Beta Kernel +Lag for details).", group=maGroup)
beta2   = input.float(3.0, title="MA2 Beta Kernel -Lag", minval=1, maxval=10, tooltip="Beta kernel negative lag for MA2 (see MA1 Beta Kernel -Lag for details).", group=maGroup)
bandwidth2 = input.float(0.3, title="MA2 Bandwidth", minval=0.1, maxval=10.0, tooltip="Bandwidth for MA2 (see MA1 Bandwidth for details).", group=maGroup)

length3 = input.int(150, title="MA3 Length", minval=1, tooltip="Number of bars for the third Moving Average.", group=maGroup)
kernelType3 = input.string(title="MA3 Kernel Type", defval="Epanechnikov", options=["Beta", "Gaussian", "Epanechnikov"], tooltip="Kernel type for MA3.", group=maGroup)
alpha3  = input.float(3.0, title="MA3 Beta Kernel +Lag", minval=1, maxval=10, tooltip="Beta kernel positive lag for MA3.", group=maGroup)
beta3   = input.float(3.0, title="MA3 Beta Kernel -Lag", minval=1, maxval=10, tooltip="Beta kernel negative lag for MA3.", group=maGroup)
bandwidth3 = input.float(0.3, title="MA3 Bandwidth", minval=0.1, maxval=10.0, tooltip="Bandwidth for MA3.", group=maGroup)

length4 = input.int(200, title="MA4 Length", minval=1, tooltip="Number of bars for the fourth Moving Average.", group=maGroup)
kernelType4 = input.string(title="MA4 Kernel Type", defval="Beta", options=["Beta", "Gaussian", "Epanechnikov"], tooltip="Kernel type for MA4.", group=maGroup)
alpha4  = input.float(3.0, title="MA4 Beta Kernel +Lag", minval=1, maxval=10, tooltip="Beta kernel positive lag for MA4.", group=maGroup)
beta4   = input.float(3.0, title="MA4 Beta Kernel -Lag", minval=1, maxval=10, tooltip="Beta kernel negative lag for MA4.", group=maGroup)
bandwidth4 = input.float(0.3, title="MA4 Bandwidth", minval=0.1, maxval=10.0, tooltip="Bandwidth for MA4.", group=maGroup)

length5 = input.int(250, title="MA5 Length", minval=1, tooltip="Number of bars for the fifth Moving Average.", group=maGroup)
kernelType5 = input.string(title="MA5 Kernel Type", defval="Gaussian", options=["Beta", "Gaussian", "Epanechnikov"], tooltip="Kernel type for MA5.", group=maGroup)
alpha5  = input.float(3.0, title="MA5 Beta Kernel +Lag", minval=1, maxval=10, tooltip="Beta kernel positive lag for MA5.", group=maGroup)
beta5   = input.float(3.0, title="MA5 Beta Kernel -Lag", minval=1, maxval=10, tooltip="Beta kernel negative lag for MA5.", group=maGroup)
bandwidth5 = input.float(0.3, title="MA5 Bandwidth", minval=0.1, maxval=10.0, tooltip="Bandwidth for MA5.", group=maGroup)

// Entry Logic
maCrossoversRequired = input.int(3, title="MA Crossovers Required", minval=1, maxval=5, tooltip="How many moving averages must cross each other to generate a potential trade signal.  A higher number means a stronger (but potentially later) signal.", group=maCrossoverGroup)
useRsiFilter         = input.bool(true, title="Use RSI Filter", tooltip="If enabled, the RSI must also be in overbought/oversold territory for a signal to be valid.", group=rsiFilterGroup)
rsiLength           = input.int(7, title="RSI Length", minval=2, tooltip="Number of bars used to calculate the RSI.", group=rsiFilterGroup)
rsiOverbought       = input.int(60, title="RSI Overbought", minval=50, maxval=100, tooltip="RSI level considered overbought (for short entries).", group=rsiFilterGroup)
rsiOversold         = input.int(40, title="RSI Oversold", minval=0, maxval=50, tooltip="RSI level considered oversold (for long entries).", group=rsiFilterGroup)

// Trend Strength Filter
useTrendStrengthFilter = input.bool(true, title="Use Trend Strength Filter", tooltip="If enabled, the trend strength (measured by the RSI of a selected MA) must be above/below a threshold.", group=trendStrengthGroup)
trendStrengthLength   = input.int(7, title="Trend Strength Length", minval=1, tooltip="Number of bars for the trend strength calculation (RSI of the selected MA).", group=trendStrengthGroup)
trendStrengthMa       = input.int(1, title="Trend Strength MA", minval=1, maxval=5, tooltip="Which moving average (1-5) to use for calculating trend strength. 1 = MA1, 2 = MA2, etc.", group=trendStrengthGroup)
minTrendStrength     = input.float(0.5, title="Min Trend Strength (Longs)", minval=0.0, maxval=1.0, step=0.01, tooltip="Minimum trend strength (0.0 - 1.0) required for long entries. 0.5 means the selected MA's RSI must be above 50.", group=trendStrengthGroup)
maxTrendStrength     = input.float(0.5, title="Max Trend Strength (Shorts)", minval=0.0, maxval=1.0, step=0.01, tooltip="Maximum trend strength (0.0 - 1.0) required for short entries. 0.5 means the selected MA's RSI must be below 50.", group=trendStrengthGroup)

// Trend Confirmation
trendConfirmationPeriod = input.int(4, title="Trend Confirmation Period", minval=1, tooltip="Number of consecutive bars the entry conditions must be met before a trade is taken. This helps filter out false signals.", group=trendConfirmGroup)


// Exit Logic
useTrailingStop = input.bool(true, title="Use Percentage Trailing Stop", tooltip="Enable a percentage-based trailing stop loss.", group=trailingStopGroup)
trailingStopActivationPercent = input.float(2.0, title="Activation (%)", minval=0.1, step=0.1, tooltip="Percentage above/below the entry price at which the trailing stop activates.", group=trailingStopGroup) / 100
trailingStopOffsetPercent     = input.float(1.0, title="Offset (%)", minval=0.1, step=0.1, tooltip="Percentage offset from the highest/lowest price reached since entry. This determines how tightly the stop trails the price.", group=trailingStopGroup) / 100

useAtrTrailingStop    = input.bool(true, title="Use ATR Trailing Stop", tooltip="Enable a trailing stop based on the Average True Range (ATR).", group=atrTrailingStopGroup)
atrTrailingStopLength = input.int(1, title="ATR Length", minval=1, tooltip="Number of bars used to calculate the ATR.", group=atrTrailingStopGroup)
atrTrailingStopMult   = input.float(200.0, title="ATR Multiplier", minval=0.1, tooltip="Multiplier for the ATR value.  A larger multiplier creates a wider stop.", group=atrTrailingStopGroup)

useAtrTakeProfit              = input.bool(false, title="Use ATR Take Profit", tooltip="Enable a take profit level based on the Average True Range (ATR).", group=atrTakeProfitGroup)
atrTakeProfitLength           = input.int(14, title="ATR Length", minval=1, tooltip="Number of bars used to calculate the ATR for take profit.", group=atrTakeProfitGroup)
atrTakeProfitMultiplier       = input.float(3.0, title="ATR Multiplier", minval=0.1, tooltip="Multiplier for the ATR value. A larger multiplier sets a further take profit target.", group=atrTakeProfitGroup)

useHardStopLoss     = input.bool(false, title="Use Hard Stop Loss", tooltip="Enable a fixed stop loss.", group=hardStopGroup)
hardStopLossPercent = input.float(0.0, title="Hard Stop Loss (%)", minval=0.0, step=0.1, tooltip="Percentage below (long) or above (short) the entry price for the hard stop loss.", group=hardStopGroup) / 100
useAtrHardStopLoss  = input.bool(false, title="Use ATR Hard Stop Loss", tooltip="Use ATR to calculate hard stop loss", group=hardStopGroup)
atrHardStopLossLength = input.int(14, title="ATR Hard Stop Loss Length", minval=1, tooltip="Length of the ATR for the hard stop loss", group=hardStopGroup)
atrHardStopLossMult   = input.float(1.5, title="ATR Hard Stop Loss Multiplier", minval=0.1, tooltip="Multiplier of ATR for the hard stop loss", group=hardStopGroup)

// *** Trade Direction Control ***
enableLongs  = input.bool(true, title="Enable Long Trades", group=tradeDirectionGroup)
enableShorts = input.bool(true, title="Enable Short Trades", group=tradeDirectionGroup)

// === Pre-calculate kernels (do this only once) ===
var kernel1 = array.new_float(length1, 0.0)
var kernel2 = array.new_float(length2, 0.0)
var kernel3 = array.new_float(length3, 0.0)
var kernel4 = array.new_float(length4, 0.0)
var kernel5 = array.new_float(length5, 0.0)

if barstate.isfirst
    if kernelType1 == "Beta"
        kernel1 := f_calculate_beta_kernel(length1, alpha1, beta1)
    else if kernelType1 == "Gaussian"
        kernel1 := f_calculate_gaussian_kernel(length1, bandwidth1)
    else // Epanechnikov
        kernel1 := f_calculate_epanechnikov_kernel(length1, bandwidth1)

    if kernelType2 == "Beta"
        kernel2 := f_calculate_beta_kernel(length2, alpha2, beta2)
    else if kernelType2 == "Gaussian"
        kernel2 := f_calculate_gaussian_kernel(length2, bandwidth2)
    else // Epanechnikov
        kernel2 := f_calculate_epanechnikov_kernel(length2, bandwidth2)

    if kernelType3 == "Beta"
        kernel3 := f_calculate_beta_kernel(length3, alpha3, beta3)
    else if kernelType3 == "Gaussian"
        kernel3 := f_calculate_gaussian_kernel(length3, bandwidth3)
    else // Epanechnikov
        kernel3 := f_calculate_epanechnikov_kernel(length3, bandwidth3)

    if kernelType4 == "Beta"
        kernel4 := f_calculate_beta_kernel(length4, alpha4, beta4)
    else if kernelType4 == "Gaussian"
        kernel4 := f_calculate_gaussian_kernel(length4, bandwidth4)
    else // Epanechnikov
        kernel4 := f_calculate_epanechnikov_kernel(length4, bandwidth4)

    if kernelType5 == "Beta"
        kernel5 := f_calculate_beta_kernel(length5, alpha5, beta5)
    else if kernelType5 == "Gaussian"
        kernel5 := f_calculate_gaussian_kernel(length5, bandwidth5)
    else // Epanechnikov
        kernel5 := f_calculate_epanechnikov_kernel(length5, bandwidth5)

// === Apply pre-calculated kernels to data ===
nw_ma1 = f_apply_kernel_ma(src, kernel1, length1)
nw_ma2 = f_apply_kernel_ma(src, kernel2, length2)
nw_ma3 = f_apply_kernel_ma(src, kernel3, length3)
nw_ma4 = f_apply_kernel_ma(src, kernel4, length4)
nw_ma5 = f_apply_kernel_ma(src, kernel5, length5)

// MA Array for easier iteration
ma_array = array.new_float(5)
array.set(ma_array, 0, nw_ma1)
array.set(ma_array, 1, nw_ma2)
array.set(ma_array, 2, nw_ma3)
array.set(ma_array, 3, nw_ma4)
array.set(ma_array, 4, nw_ma5)

// Calculate ATR values *unconditionally*
atrTrailingValue = ta.atr(atrTrailingStopLength)
atrTakeProfitValue = ta.atr(atrTakeProfitLength)
atrHardStopLossValue = ta.atr(atrHardStopLossLength)

// Calculate Trend Strength *unconditionally* (and only once)
trendStrengthValue = useTrendStrengthFilter ? f_trend_strength(array.get(ma_array, trendStrengthMa - 1), trendStrengthLength) : 0.0

// === Entry Logic ===

// MA Crossovers
longMaCrossovers  = 0
shortMaCrossovers = 0

for i = 0 to 3
    if array.get(ma_array, i) > array.get(ma_array, i + 1)
        longMaCrossovers  := longMaCrossovers  + 1
    if array.get(ma_array, i) < array.get(ma_array, i + 1)
        shortMaCrossovers := shortMaCrossovers + 1

longCrossoverCondition  = longMaCrossovers  >= maCrossoversRequired
shortCrossoverCondition = shortMaCrossovers >= maCrossoversRequired

// RSI Filter
rsiValue = ta.rsi(src, rsiLength)
longRsiCondition  = not useRsiFilter or (rsiValue < rsiOversold)
shortRsiCondition = not useRsiFilter or (rsiValue > rsiOverbought)

// Trend Strength Filter - Simplified Logic
longTrendStrengthCondition  = not useTrendStrengthFilter or trendStrengthValue >= minTrendStrength
shortTrendStrengthCondition = not useTrendStrengthFilter or trendStrengthValue <= maxTrendStrength


// --- Trend Confirmation Logic ---
var int long_confirm_count = 0
var int short_confirm_count = 0
var bool confirmedLong = false
var bool confirmedShort = false

// Update confirmation counters
if longCrossoverCondition and longRsiCondition and longTrendStrengthCondition
    long_confirm_count := long_confirm_count + 1
    short_confirm_count := 0  // Reset opposite counter
else
    long_confirm_count := 0

if shortCrossoverCondition and shortRsiCondition and shortTrendStrengthCondition
    short_confirm_count := short_confirm_count + 1
    long_confirm_count := 0 // Reset opposite counter
else
    short_confirm_count := 0

// Check for confirmed trend
confirmedLong := long_confirm_count >= trendConfirmationPeriod
confirmedShort := short_confirm_count >= trendConfirmationPeriod

// Combined Entry Conditions (using confirmed trend)
longCondition = confirmedLong  and enableLongs // Added trade direction check
shortCondition = confirmedShort and enableShorts // Added trade direction check

// === Exit Logic ===
var float longTrail = na
var float shortTrail = na
var float longTakeProfitPrice = na
var float shortTakeProfitPrice = na
var float longHardStopLossPrice = na
var float shortHardStopLossPrice = na

// Hard Stop Loss and Take Profit calculation on entry
if longCondition or shortCondition
    // Calculate Hard Stop Loss
    if useHardStopLoss
        if useAtrHardStopLoss
            longHardStopLossPrice  := close - (atrHardStopLossValue * atrHardStopLossMult)
            shortHardStopLossPrice := close + (atrHardStopLossValue * atrHardStopLossMult)
        else
            longHardStopLossPrice  := close * (1 - hardStopLossPercent)
            shortHardStopLossPrice := close * (1 + hardStopLossPercent)
    else
        longHardStopLossPrice := na
        shortHardStopLossPrice := na

    // Calculate Take Profit
    if useAtrTakeProfit
        longTakeProfitPrice  := close + (atrTakeProfitValue * atrTakeProfitMultiplier)
        shortTakeProfitPrice := close - (atrTakeProfitValue * atrTakeProfitMultiplier)
    else
        longTakeProfitPrice := na
        shortTakeProfitPrice := na

// Trailing Stop Logic - updated for each bar
if strategy.position_size > 0
    // Calculate trailing stop
    float tempTrail = na

    if useTrailingStop
        if close > strategy.position_avg_price * (1 + trailingStopActivationPercent)
            tempTrail := close * (1 - trailingStopOffsetPercent)
            if na(longTrail) or tempTrail > longTrail
                longTrail := tempTrail

    if useAtrTrailingStop
        float atrTrail = close - (atrTrailingValue * atrTrailingStopMult)
        if na(longTrail) or atrTrail > longTrail
            longTrail := atrTrail

if strategy.position_size < 0
    // Calculate trailing stop
    float tempTrail = na

    if useTrailingStop
        if close < strategy.position_avg_price * (1 - trailingStopActivationPercent)
            tempTrail := close * (1 + trailingStopOffsetPercent)
            if na(shortTrail) or tempTrail < shortTrail
                shortTrail := tempTrail

    if useAtrTrailingStop
        float atrTrail = close + (atrTrailingValue * atrTrailingStopMult)
        if na(shortTrail) or atrTrail < shortTrail
            shortTrail := atrTrail

// === Strategy Execution ===
if longCondition
    strategy.entry("Long", strategy.long)
    longTrail := na  // Reset on new entry
    shortTrail := na // Reset on new entry

if shortCondition
    strategy.entry("Short", strategy.short)
    shortTrail := na // Reset on new entry
    longTrail := na  // Reset on new entry

// Unified exit logic with proper ordering
if strategy.position_size > 0
    // Define effective stop level (combining hard stop and trailing stop)
    float effectiveStopLevel = na

    if not na(longHardStopLossPrice) and useHardStopLoss
        effectiveStopLevel := longHardStopLossPrice

    if not na(longTrail) and (useTrailingStop or useAtrTrailingStop)
        if na(effectiveStopLevel) or longTrail > effectiveStopLevel
            effectiveStopLevel := longTrail

    // Combined exit strategy with proper parameters
    strategy.exit("Long Exit", "Long",
                 limit = useAtrTakeProfit ? longTakeProfitPrice : na,
                 stop = effectiveStopLevel)

if strategy.position_size < 0
    // Define effective stop level (combining hard stop and trailing stop)
    float effectiveStopLevel = na

    if not na(shortHardStopLossPrice) and useHardStopLoss
        effectiveStopLevel := shortHardStopLossPrice

    if not na(shortTrail) and (useTrailingStop or useAtrTrailingStop)
        if na(effectiveStopLevel) or shortTrail < effectiveStopLevel
            effectiveStopLevel := shortTrail

    // Combined exit strategy with proper parameters
    strategy.exit("Short Exit", "Short",
                 limit = useAtrTakeProfit ? shortTakeProfitPrice : na,
                 stop = effectiveStopLevel)

// === Plotting ===
plotColorMa1 = nw_ma1 > nw_ma1[1] ? color.rgb(100, 250, 120) : color.rgb(255, 100, 120)
plotColorMa2 = nw_ma2 > nw_ma2[1] ? color.rgb(100, 250, 120) : color.rgb(255, 100, 120)
plotColorMa3 = nw_ma3 > nw_ma3[1] ? color.rgb(100, 250, 120) : color.rgb(255, 100, 120)
plotColorMa4 = nw_ma4 > nw_ma4[1] ? color.rgb(100, 250, 120) : color.rgb(255, 100, 120)
plotColorMa5 = nw_ma5 > nw_ma5[1] ? color.rgb(100, 250, 120) : color.rgb(255, 100, 120)

plot(nw_ma1, title="NW MA 1", color=plotColorMa1, linewidth=2)
plot(nw_ma2, title="NW MA 2", color=plotColorMa2, linewidth=2)
plot(nw_ma3, title="NW MA 3", color=plotColorMa3, linewidth=2)
plot(nw_ma4, title="NW MA 4", color=plotColorMa4, linewidth=2)
plot(nw_ma5, title="NW MA 5", color=plotColorMa5, linewidth=2)
```

> Detail

https://www.fmz.com/strategy/488517

> Last Modified

2025-03-28 15:13:28
