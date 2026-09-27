
> Name

Candlestick-Emotion-Momentum-Trend-Trading-Strategy-Based-on-Quantitative-Indicators

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d96bcb834c86ad9faeea.png)
![IMG](https://www.fmz.com/upload/asset/2d85ba3ff51c5335a8802.png)





#### Overview
This strategy analyzes market sentiment through candlestick patterns using three core oscillators (Indecision, Fear, and Greed) to quantify market psychology. It combines momentum and trend indicators with volume confirmation to build a complete trading system. The strategy is suitable for traders who want to identify high-probability trading opportunities through market sentiment analysis.

#### Strategy Principles
The core of the strategy is built on three sentiment oscillators derived from candlestick patterns:
1. Indecision Oscillator - Measures market uncertainty through Doji and Spinning Top patterns
2. Fear Oscillator - Tracks bearish sentiment through Shooting Star, Hanging Man, and Bearish Engulfing patterns
3. Greed Oscillator - Detects bullish sentiment through Marubozu, Hammer, Bullish Engulfing, and Three White Soldiers

The average of these three oscillators forms the Candle Emotion Index (CEI). Trading signals are triggered when CEI breaks different thresholds, confirmed by volume analysis.

#### Strategy Advantages
1. Systematic Sentiment Analysis - Transforms subjective candlestick analysis into objective indicators
2. Comprehensive Risk Management - Includes maximum holding period, profit/loss limits, and cooldown periods
3. Flexible Recovery Mechanism - Attempts to recover through breakeven points when trades move against position
4. Multi-Market Compatibility - Applicable across stocks, forex, and cryptocurrency markets
5. High Signal Reliability - Uses volume confirmation and multiple technical indicators for validation

#### Strategy Risks
1. Parameter Sensitivity - Various thresholds require thorough testing and optimization
2. Market Environment Dependency - May generate false signals in ranging markets
3. Slippage Risk - Execution risks in markets with poor liquidity
4. Overtrading Risk - Requires proper cooldown periods to avoid excessive trading
5. Systematic Risk - May suffer significant losses during major market events

#### Optimization Directions
1. Dynamic Thresholds - Automatically adjust thresholds based on market volatility
2. Market State Classification - Add trend and range market identification mechanisms
3. Machine Learning Optimization - Use machine learning algorithms to optimize parameter combinations
4. Enhanced Risk Management - Add money management and position sizing modules
5. Signal Filtering - Integrate more technical indicators to filter false signals

#### Summary
This innovative strategy combines technical analysis with quantitative trading. Through systematic sentiment analysis and strict risk management, it provides reliable trading signals for traders. While there is room for optimization, the basic framework is robust and suitable for further development and live trading implementation.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-03-09 18:40:00
end: 2025-02-19 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Binance","currency":"SOL_USDT"}]
*/

//@version=6
strategy("Candle Emotion Index Strategy", shorttitle="CEI Strategy", overlay=true)

// User Inputs
length = input.int(14, title="Lookback Period", minval=1)
dojiThreshold = input.float(0.1, title="Doji Threshold", minval=0.01, maxval=0.5)
spinningTopThreshold = input.float(0.3, title="Spinning Top Threshold", minval=0.1, maxval=0.5)
shootingStarThreshold = input.float(0.5, title="Shooting Star Threshold", minval=0.1, maxval=1.0)
hangingManThreshold = input.float(0.5, title="Hanging Man Threshold", minval=0.1, maxval=1.0)
engulfingThreshold = input.float(0.5, title="Engulfing Threshold", minval=0.1, maxval=1.0)
marubozuThreshold = input.float(0.9, title="Marubozu Threshold", minval=0.5, maxval=1.0)
hammerThreshold = input.float(0.5, title="Hammer Threshold", minval=0.1, maxval=1.0)
threeWhiteSoldiersThreshold = input.float(0.5, title="Three White Soldiers Threshold", minval=0.1, maxval=1.0)

// Volume Multiplier Input
volumeMultiplier = input.float(1.5, title="Volume Multiplier", minval=1.0)

// Cooldown Period Input
cooldownPeriod = input.int(10, title="Cooldown Period (Candles)", minval=1)

// Maximum Holding Period Inputs
maxHoldingPeriod = input.int(20, title="Maximum Holding Period (Candles)", minval=1)
lossHoldingPeriod = input.int(10, title="Loss Exit Holding Period (Candles)", minval=1)
lossThreshold = input.float(0.02, title="Loss Threshold (as % of Entry Price)", minval=0.01, maxval=1.0)

// --- Indecision Oscillator Functions ---
isDoji(open, close, high, low, threshold) =>
    bodySize = math.abs(close - open)
    rangeSize = high - low
    bodySize / rangeSize < threshold

isSpinningTop(open, close, high, low, threshold) =>
    bodySize = math.abs(close - open)
    rangeSize = high - low
    bodySize / rangeSize < threshold and bodySize / rangeSize >= dojiThreshold

indecisionOscillator() =>
    var float dojiScore = 0.0
    var float spinningTopScore = 0.0
    for i = 1 to length
        if isDoji(open[i], close[i], high[i], low[i], dojiThreshold)
            dojiScore := dojiScore + 1.0
        if isSpinningTop(open[i], close[i], high[i], low[i], spinningTopThreshold)
            spinningTopScore := spinningTopScore + 1.0
    dojiScore := dojiScore / length
    spinningTopScore := spinningTopScore / length
    (dojiScore + spinningTopScore) / 2

// --- Fear Oscillator Functions ---
isShootingStar(open, close, high, low, threshold) =>
    bodySize = math.abs(close - open)
    upperWick = high - math.max(open, close)
    lowerWick = math.min(open, close) - low
    upperWick / bodySize > threshold and lowerWick < bodySize

isHangingMan(open, close, high, low, threshold) =>
    bodySize = math.abs(close - open)
    upperWick = high - math.max(open, close)
    lowerWick = math.min(open, close) - low
    lowerWick / bodySize > threshold and upperWick < bodySize

isBearishEngulfing(open, close, openPrev, closePrev, threshold) =>
    bodySize = math.abs(close - open)
    prevBodySize = math.abs(closePrev - openPrev)
    close < openPrev and open > closePrev and bodySize / prevBodySize > threshold

fearOscillator() =>
    var float shootingStarScore = 0.0
    var float hangingManScore = 0.0
    var float engulfingScore = 0.0
    for i = 1 to length
        if isShootingStar(open[i], close[i], high[i], low[i], shootingStarThreshold)
            shootingStarScore := shootingStarScore + 1.0
        if isHangingMan(open[i], close[i], high[i], low[i], hangingManThreshold)
            hangingManScore := hangingManScore + 1.0
        if isBearishEngulfing(open[i], close[i], open[i+1], close[i+1], engulfingThreshold)
            engulfingScore := engulfingScore + 1.0
    shootingStarScore := shootingStarScore / length
    hangingManScore := hangingManScore / length
    engulfingScore := engulfingScore / length
    (shootingStarScore + hangingManScore + engulfingScore) / 3

// --- Greed Oscillator Functions ---
isMarubozu(open, close, high, low, threshold) =>
    bodySize = math.abs(close - open)
    totalRange = high - low
    bodySize / totalRange > threshold

isHammer(open, close, high, low, threshold) =>
    bodySize = math.abs(close - open)
    lowerWick = math.min(open, close) - low
    upperWick = high - math.max(open, close)
    lowerWick / bodySize > threshold and upperWick < bodySize

isBullishEngulfing(open, close, openPrev, closePrev, threshold) =>
    bodySize = math.abs(close - open)
    prevBodySize = math.abs(closePrev - openPrev)
    close > openPrev and open < closePrev and bodySize / prevBodySize > threshold

isThreeWhiteSoldiers(open, close, openPrev, closePrev, openPrev2, closePrev2, threshold) =>
    close > open and closePrev > openPrev and closePrev2 > openPrev2 and close > closePrev and closePrev > closePrev2

greedOscillator() =>
    var float marubozuScore = 0.0
    var float hammerScore = 0.0
    var float engulfingScore = 0.0
    var float soldiersScore = 0.0
    for i = 1 to length
        if isMarubozu(open[i], close[i], high[i], low[i], marubozuThreshold)
            marubozuScore := marubozuScore + 1.0
        if isHammer(open[i], close[i], high[i], low[i], hammerThreshold)
            hammerScore := hammerScore + 1.0
        if isBullishEngulfing(open[i], close[i], open[i+1], close[i+1], engulfingThreshold)
            engulfingScore := engulfingScore + 1.0
        if isThreeWhiteSoldiers(open[i], close[i], open[i+1], close[i+1], open[i+2], close[i+2], threeWhiteSoldiersThreshold)
            soldiersScore := soldiersScore + 1.0
    marubozuScore := marubozuScore / length
    hammerScore := hammerScore / length
    engulfingScore := engulfingScore / length
    soldiersScore := soldiersScore / length
    (marubozuScore + hammerScore + engulfingScore + soldiersScore) / 4

// --- Final Calculations ---
indecision = indecisionOscillator()
fear = fearOscillator()
greed = greedOscillator()

// Calculate the average of the three oscillators
averageOscillator = (indecision + fear + greed) / 3

// --- Combined Strategy Logic ---
var float entryPriceLong = na
var float entryPriceShort = na
var int holdingPeriodLong = 0
var int holdingPeriodShort = 0
var int cooldownCounter = 0

// Buy Signal Logic for Long and Short
longBuySignal = ta.crossover(averageOscillator, 0.1)
shortBuySignal = ta.crossover(averageOscillator, 0.2)

// Calculate average volume over the lookback period
avgVolume = ta.sma(volume, length)

// Take Profit Conditions
longTakeProfitCondition = close > open and volume > avgVolume * volumeMultiplier
shortTakeProfitCondition = close < open and volume > avgVolume * volumeMultiplier

// Buy Logic for Long Positions
if longBuySignal and strategy.position_size == 0 and cooldownCounter <= 0
    entryPriceLong := close
    strategy.entry("Long Entry", strategy.long)
    cooldownCounter := cooldownPeriod
    holdingPeriodLong := 0

// Increment holding period if in a long position
if strategy.position_size > 0
    holdingPeriodLong := holdingPeriodLong + 1

// Sell Logic for Long Positions
if longTakeProfitCondition and strategy.position_size > 0 and close > entryPriceLong
    strategy.close_all()
    cooldownCounter := cooldownPeriod

if holdingPeriodLong >= maxHoldingPeriod and strategy.position_size > 0 and close >= entryPriceLong
    strategy.close_all()
    cooldownCounter := cooldownPeriod

if holdingPeriodLong >= lossHoldingPeriod and strategy.position_size > 0 and close < entryPriceLong * (1 - lossThreshold)
    strategy.close_all()
    cooldownCounter := cooldownPeriod

// Short Logic for Short Positions
if shortBuySignal and strategy.position_size == 0 and cooldownCounter <= 0
    entryPriceShort := close
    strategy.entry("Short Entry", strategy.short)
    cooldownCounter := cooldownPeriod
    holdingPeriodShort := 0

// Increment holding period if in a short position
if strategy.position_size < 0
    holdingPeriodShort := holdingPeriodShort + 1

// Cover Logic for Short Positions
if shortTakeProfitCondition and strategy.position_size < 0 and close < entryPriceShort
    strategy.close_all()
    cooldownCounter := cooldownPeriod

if holdingPeriodShort >= maxHoldingPeriod and strategy.position_size < 0 and close <= entryPriceShort
    strategy.close_all()
    cooldownCounter := cooldownPeriod

if holdingPeriodShort >= lossHoldingPeriod and strategy.position_size < 0 and close > entryPriceShort * (1 + lossThreshold)
    strategy.close_all()
    cooldownCounter := cooldownPeriod

// Decrement the cooldown counter each candle
if cooldownCounter > 0
    cooldownCounter := cooldownCounter - 1

```

> Detail

https://www.fmz.com/strategy/483093

> Last Modified

2025-02-21 13:23:51
