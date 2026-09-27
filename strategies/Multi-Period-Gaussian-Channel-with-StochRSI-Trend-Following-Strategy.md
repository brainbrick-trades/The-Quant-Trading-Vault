
> Name

Multi-Period-Gaussian-Channel-with-StochRSI-Trend-Following-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/10fab6df866d016d13c.png)


#### Overview
This strategy is a trend following trading system based on Gaussian filtering and StochRSI indicator. It uses Gaussian channels to identify market trends and combines StochRSI indicator's overbought/oversold zones to optimize entry timing. The system employs polynomial fitting to construct Gaussian channels, tracking price trends through dynamic adjustment of upper and lower bands.

#### Strategy Principle
The core of the strategy is the price channel built on Gaussian filtering algorithm. Key implementation steps include:
1. Implementing 9th-order Gaussian filtering using polynomial function f_filt9x with pole optimization
2. Calculating main filter line and volatility channel based on HLC3 price
3. Introducing reducedLag mode to decrease filtering delay and fastResponse mode to improve response speed
4. Utilizing StochRSI indicator's overbought/oversold zones (80/20) for trade signals
5. Generating long signals when Gaussian channel trends upward and price breaks above upper band, combined with StochRSI conditions
6. Closing positions when price falls below upper band

#### Strategy Advantages
1. Excellent noise reduction capability through Gaussian filtering
2. Smooth trend tracking via polynomial fitting, reducing false signals
3. Supports delay optimization and fast response modes for flexible market adaptation
4. Improved entry timing through StochRSI indicator integration
5. Dynamic channel width adapting to market volatility changes

#### Strategy Risks
1. Inherent lag in Gaussian filtering may lead to delayed entries or exits
2. May generate frequent trading signals in ranging markets, increasing transaction costs
3. StochRSI indicator might produce lagging signals under certain market conditions
4. Complex parameter optimization process requiring readjustment for different markets
5. High computational resource requirements leading to potential real-time calculation delays

#### Optimization Directions
1. Introduce adaptive parameter optimization based on market conditions
2. Add market environment recognition for different parameter combinations
3. Optimize Gaussian filtering algorithm to further reduce calculation delay
4. Incorporate additional technical indicators for cross-validation
5. Develop intelligent stop-loss mechanisms for improved risk control

#### Summary
The strategy achieves effective market trend tracking through the combination of Gaussian filtering and StochRSI indicator. While the system demonstrates strong noise reduction and trend identification capabilities, it faces challenges with latency and parameter optimization. Through continuous improvement and refinement, the strategy shows potential for generating stable returns in actual trading.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-19 00:00:00
end: 2025-02-16 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy(title="Demo GPT - Gaussian Channel Strategy v3.0", overlay=true, commission_type=strategy.commission.percent, commission_value=0.1, slippage=0, default_qty_type=strategy.percent_of_equity, default_qty_value=250)

// ============================================
// Gaussian Functions (Must be at top)
// ============================================
f_filt9x(_a, _s, _i) =>
    var int _m2 = 0, var int _m3 = 0, var int _m4 = 0, var int _m5 = 0, var int _m6 = 0,
    var int _m7 = 0, var int _m8 = 0, var int _m9 = 0, var float _f = 0.0
    _x = 1 - _a
    _m2 := _i == 9 ? 36 : _i == 8 ? 28 : _i == 7 ? 21 : _i == 6 ? 15 : _i == 5 ? 10 : _i == 4 ? 6 : _i == 3 ? 3 : _i == 2 ? 1 : 0
    _m3 := _i == 9 ? 84 : _i == 8 ? 56 : _i == 7 ? 35 : _i == 6 ? 20 : _i == 5 ? 10 : _i == 4 ? 4 : _i == 3 ? 1 : 0
    _m4 := _i == 9 ? 126 : _i == 8 ? 70 : _i == 7 ? 35 : _i == 6 ? 15 : _i == 5 ? 5 : _i == 4 ? 1 : 0
    _m5 := _i == 9 ? 126 : _i == 8 ? 56 : _i == 7 ? 21 : _i == 6 ? 6 : _i == 5 ? 1 : 0
    _m6 := _i == 9 ? 84 : _i == 8 ? 28 : _i == 7 ? 7 : _i == 6 ? 1 : 0
    _m7 := _i == 9 ? 36 : _i == 8 ? 8 : _i == 7 ? 1 : 0
    _m8 := _i == 9 ? 9 : _i == 8 ? 1 : 0
    _m9 := _i == 9 ? 1 : 0
    _f := math.pow(_a, _i) * nz(_s) + _i * _x * nz(_f[1]) - (_i >= 2 ? _m2 * math.pow(_x, 2) * nz(_f[2]) : 0) + (_i >= 3 ? _m3 * math.pow(_x, 3) * nz(_f[3]) : 0) - (_i >= 4 ? _m4 * math.pow(_x, 4) * nz(_f[4]) : 0) + (_i >= 5 ? _m5 * math.pow(_x, 5) * nz(_f[5]) : 0) - (_i >= 6 ? _m6 * math.pow(_x, 6) * nz(_f[6]) : 0) + (_i >= 7 ? _m7 * math.pow(_x, 7) * nz(_f[7]) : 0) - (_i >= 8 ? _m8 * math.pow(_x, 8) * nz(_f[8]) : 0) + (_i == 9 ? _m9 * math.pow(_x, 9) * nz(_f[9]) : 0)
    _f

f_pole(_a, _s, _i) =>
    _f1 = f_filt9x(_a, _s, 1)
    _f2 = _i >= 2 ? f_filt9x(_a, _s, 2) : 0.0
    _f3 = _i >= 3 ? f_filt9x(_a, _s, 3) : 0.0
    _f4 = _i >= 4 ? f_filt9x(_a, _s, 4) : 0.0
    _f5 = _i >= 5 ? f_filt9x(_a, _s, 5) : 0.0
    _f6 = _i >= 6 ? f_filt9x(_a, _s, 6) : 0.0
    _f7 = _i >= 7 ? f_filt9x(_a, _s, 7) : 0.0
    _f8 = _i >= 8 ? f_filt9x(_a, _s, 8) : 0.0
    _f9 = _i == 9 ? f_filt9x(_a, _s, 9) : 0.0
    _fn = _i == 1 ? _f1 : _i == 2 ? _f2 : _i == 3 ? _f3 : _i == 4 ? _f4 : _i == 5 ? _f5 : _i == 6 ? _f6 : _i == 7 ? _f7 : _i == 8 ? _f8 : _i == 9 ? _f9 : na
    [_fn, _f1]

// ============================================
// Date Filter
// ============================================
startDate = input(timestamp("1 Jan 2018"), "Start Date", group="Time Settings")
endDate = input(timestamp("31 Dec 2069"), "End Date", group="Time Settings")
timeCondition = true

// ============================================
// Stochastic RSI (Hidden Calculations)
// ============================================
stochRsiK = input.int(3, "Stoch RSI K", group="Stochastic RSI", tooltip="Only for calculations, not visible")
stochRsiD = input.int(3, "Stoch RSI D", group="Stochastic RSI")
rsiLength = input.int(14, "RSI Length", group="Stochastic RSI")
stochLength = input.int(14, "Stochastic Length", group="Stochastic RSI")

rsiValue = ta.rsi(close, rsiLength)
k = ta.sma(ta.stoch(rsiValue, rsiValue, rsiValue, stochLength), stochRsiK)
d = ta.sma(k, stochRsiD)

// ============================================
// Gaussian Channel
// ============================================
gaussianSrc = input(hlc3, "Source", group="Gaussian")
poles = input.int(4, "Poles", minval=1, maxval=9, group="Gaussian")
samplingPeriod = input.int(144, "Sampling Period", minval=2, group="Gaussian")
multiplier = input.float(1.414, "Multiplier", step=0.1, group="Gaussian")
reducedLag = input.bool(false, "Reduced Lag Mode", group="Gaussian")
fastResponse = input.bool(false, "Fast Response Mode", group="Gaussian")

// Gaussian Calculations
beta = (1 - math.cos(4 * math.asin(1) / samplingPeriod)) / (math.pow(1.414, 2 / poles) - 1)
alpha = -beta + math.sqrt(math.pow(beta, 2) + 2 * beta)
lag = (samplingPeriod - 1) / (2 * poles)

srcData = reducedLag ? gaussianSrc + (gaussianSrc - gaussianSrc[lag]) : gaussianSrc
trData = reducedLag ? ta.tr(true) + (ta.tr(true) - ta.tr(true)[lag]) : ta.tr(true)

[mainFilter, filter1] = f_pole(alpha, srcData, poles)
[trFilter, trFilter1] = f_pole(alpha, trData, poles)

finalFilter = fastResponse ? (mainFilter + filter1) / 2 : mainFilter
finalTrFilter = fastResponse ? (trFilter + trFilter1) / 2 : trFilter

upperBand = finalFilter + finalTrFilter * multiplier
lowerBand = finalFilter - finalTrFilter * multiplier

// ============================================
// Trading Logic
// ============================================
longCondition = 
  finalFilter > finalFilter[1] and      // Green Channel
  close > upperBand and                 // Price above upper band
  (k >= 80 or k <= 20) and             // Stoch RSI condition
  timeCondition

exitCondition = ta.crossunder(close, upperBand)

if longCondition
    strategy.entry("Long", strategy.long)

if exitCondition
    strategy.close("Long")

// ============================================
// Visuals (Gaussian Only)
// ============================================
bandColor = finalFilter > finalFilter[1] ? color.new(#00ff00, 0) : color.new(#ff0000, 0)
plot(finalFilter, "Filter", bandColor, 2)
plot(upperBand, "Upper Band", bandColor)
plot(lowerBand, "Lower Band", bandColor)
fill(plot(upperBand), plot(lowerBand), color.new(bandColor, 90))

barcolor(close > open and close > upperBand ? color.green : 
         close < open and close < lowerBand ? color.red : na)
```

> Detail

https://www.fmz.com/strategy/482426

> Last Modified

2025-02-18 13:50:36
