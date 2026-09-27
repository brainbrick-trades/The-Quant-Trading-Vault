
> Name

Opening-and-Closing-Moving-Average-Crossover-Strategy-with-ADX-Dynamic-Indicator

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/134660a698b49d03da6.png)


#### Overview
This is a quantitative trading strategy based on the crossover of opening and closing price moving averages, combined with the Average Directional Index (ADX) as a filter. The strategy employs various types of moving averages, including SMMA, EMA, DEMA, etc., to capture market trend changes by identifying crossover points while using the ADX indicator to confirm trend strength and improve trading reliability.

#### Strategy Principle
The core logic of the strategy is to calculate moving averages of opening and closing prices. A long signal is generated when the closing price MA crosses above the opening price MA and the ADX value exceeds the set threshold. Conversely, a short signal is generated when the closing price MA crosses below the opening price MA and the ADX value exceeds the threshold. The strategy supports multiple moving average calculation methods, including Simple Moving Average (SMA), Exponential Moving Average (EMA), Double Exponential Moving Average (DEMA), etc., allowing selection of the most suitable MA type for different market characteristics.

#### Strategy Advantages
1. High Flexibility: Supports various moving average types, allowing selection of optimal MA calculation methods for different market environments
2. Trend Confirmation: ADX filtering effectively reduces false signals in oscillating markets
3. Comprehensive Risk Control: Includes stop-loss and take-profit functions for effective risk control per trade
4. High Customizability: Provides multiple parameter interfaces, including MA period, ADX threshold, trading direction, etc., facilitating strategy optimization
5. Multi-timeframe Support: Can operate on different timeframes, adapting to various trading styles

#### Strategy Risks
1. MA Lag: Moving averages are inherently lagging indicators, potentially generating delayed signals in rapidly fluctuating markets
2. False Breakout Risk: False MA breakouts may occur during market oscillation, despite ADX filtering
3. Parameter Sensitivity: Strategy performance is sensitive to parameter settings, requiring appropriate adjustments in different market environments
4. Market Adaptability: Performs well in trending markets but may trade frequently in oscillating markets
5. Computational Complexity: Multiple MA type calculations may increase system load, requiring attention to operational efficiency

#### Strategy Optimization Directions
1. Incorporate Volume Indicators: Combine volume changes to confirm trend validity
2. Optimize ADX Parameters: Dynamically adjust ADX thresholds based on different market cycles
3. Add Trend Confirmation Indicators: Consider adding other trend indicators to improve signal reliability
4. Enhance Stop-Loss Mechanism: Introduce trailing stops or volatility-adaptive stop-losses
5. Optimize Trading Timing: Consider market volatility and liquidity factors to select optimal trading times

#### Summary
This is a quantitative trading system that combines classic moving average crossover strategy with the ADX indicator. Through support for multiple MA types and ADX trend confirmation, it effectively captures market trends while maintaining comprehensive risk control mechanisms. The strategy's high customizability allows optimization for different market environments. While inherent risks exist, through proper parameter settings and continuous optimization, this strategy demonstrates good practical value.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-18 00:00:00
end: 2025-02-16 08:00:00
period: 3d
basePeriod: 3d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © algostudio

//@version=6
strategy("Open Close Cross Strategy R5.1", shorttitle="OCC Strategy R5.1", overlay=true,
     pyramiding=0, default_qty_type=strategy.percent_of_equity, default_qty_value=10, calc_on_every_tick=false)

// === INPUTS ===
useRes      = input.bool(true, title="Use Alternate Resolution?")
intRes      = input.int(3, title="Multiplier for Alternate Resolution", minval=1)
stratRes    = timeframe.ismonthly ? str.tostring(timeframe.multiplier * intRes) + "M" :
              timeframe.isweekly ? str.tostring(timeframe.multiplier * intRes) + "W" :
              timeframe.isdaily ? str.tostring(timeframe.multiplier * intRes) + "D" :
              timeframe.isintraday ? str.tostring(timeframe.multiplier * intRes) : "60"

basisType   = input.string("SMMA", title="MA Type:", options=["SMA", "EMA", "DEMA", "TEMA", "WMA", "VWMA", "SMMA", "HullMA", "LSMA", "ALMA", "SSMA", "TMA"])
basisLen    = input.int(8, title="MA Period", minval=1)
offsetSigma = input.int(6, title="Offset for LSMA / Sigma for ALMA", minval=0)
offsetALMA  = input.float(0.85, title="Offset for ALMA", minval=0, step=0.01)
scolor      = input.bool(false, title="Show Colored Bars to Indicate Trend?")
delayOffset = input.int(0, title="Delay Open/Close MA (Forces Non-Repainting)", minval=0, step=1)
tradeType   = input.string("BOTH", title="What trades should be taken:", options=["LONG", "SHORT", "BOTH", "NONE"])

// === BASE FUNCTIONS ===
variant(type, src, len, offSig, offALMA) =>
    if type == "EMA"
        ta.ema(src, len)
    else if type == "DEMA"
        ta.ema(ta.ema(src, len), len) * 2 - ta.ema(ta.ema(ta.ema(src, len), len), len)
    else if type == "TEMA"
        3 * (ta.ema(src, len) - ta.ema(ta.ema(src, len), len)) + ta.ema(ta.ema(ta.ema(src, len), len), len)
    else if type == "WMA"
        ta.wma(src, len)
    else if type == "VWMA"
        ta.vwma(src, len)
    else if type == "SMMA"
        ta.sma(src, len)
    else if type == "HullMA"
        ta.wma(2 * ta.wma(src, len / 2) - ta.wma(src, len), math.round(math.sqrt(len)))
    else if type == "LSMA"
        ta.linreg(src, len, offSig)
    else if type == "ALMA"
        ta.alma(src, len, offALMA, offSig)
    else if type == "TMA"
        ta.sma(ta.sma(src, len), len)
    else
        ta.sma(src, len)

// Security wrapper
reso(exp, use, res) => use ? request.security(syminfo.tickerid, res, exp, lookahead=barmerge.lookahead_on) : exp

// === SERIES SETUP ===
closeSeries = variant(basisType, close[delayOffset], basisLen, offsetSigma, offsetALMA)
openSeries  = variant(basisType, open[delayOffset], basisLen, offsetSigma, offsetALMA)

// Alternate resolution series
closeSeriesAlt = reso(closeSeries, useRes, stratRes)
openSeriesAlt  = reso(openSeries, useRes, stratRes)

// Trend Colors
trendColour = closeSeriesAlt > openSeriesAlt ? color.green : color.red
bcolour     = closeSeries > openSeriesAlt ? color.lime : color.red
barcolor(scolor ? bcolour : na, title="Bar Colours")

closeP = plot(closeSeriesAlt, title="Close Series", color=trendColour, linewidth=2, style=plot.style_line)
openP  = plot(openSeriesAlt, title="Open Series", color=trendColour, linewidth=2, style=plot.style_line)
fill(closeP, openP, color=trendColour)
// === ADX FILTER ===
// ADX Calculation
// Input parameters
adxLength = input.int(14, title="ADX Length", minval=1)
adxfilter = input.int(13, title="ADX filter", minval=1)
// Calculate +DM and -DM (Directional Movement)
plusDM = math.max(high - high[1], 0)
minusDM = math.max(low[1] - low, 0)

// Remove cases where both are positive
plusDM := plusDM > minusDM ? plusDM : 0
minusDM := minusDM > plusDM ? minusDM : 0

// Smooth the directional movement using RMA
smoothedPlusDM = ta.rma(plusDM, adxLength)
smoothedMinusDM = ta.rma(minusDM, adxLength)

// Calculate True Range and smooth it
tr = ta.atr(adxLength)
smoothedTR = ta.rma(tr, adxLength)

// Compute +DI and -DI
plusDI = (smoothedPlusDM / smoothedTR) * 100
minusDI = (smoothedMinusDM / smoothedTR) * 100

// Compute DX (Directional Index)
dx = math.abs(plusDI - minusDI) / (plusDI + minusDI) * 100

// Compute ADX by smoothing DX
adx = ta.rma(dx, adxLength)




// === UPDATED TRADE CONDITIONS ===
xlong     = ta.crossover(closeSeriesAlt, openSeriesAlt) and adx > adxfilter
xshort    = ta.crossunder(closeSeriesAlt, openSeriesAlt) and adx > adxfilter
longCond  = xlong
shortCond = xshort


// === STRATEGY ===
slPoints  = input.float(0, title="Initial Stop Loss Points", minval=0)
tpPoints  = input.float(0, title="Initial Target Profit Points", minval=0)
ebar      = input.int(10000, title="Number of Bars for Back Testing", minval=0)

tdays     = (timenow - time) / 60000.0

tdays     := timeframe.ismonthly ? tdays / 1440.0 / 5.0 / 4.3 / timeframe.multiplier :
             timeframe.isweekly ? tdays / 1440.0 / 5.0 / timeframe.multiplier :
             timeframe.isdaily ? tdays / 1440.0 / timeframe.multiplier :
             tdays / timeframe.multiplier

TP = tpPoints > 0 ? tpPoints : na
SL = slPoints > 0 ? slPoints : na

if (ebar == 0 or tdays <= ebar)
    if longCond and tradeType != "SHORT"
        strategy.entry("long", strategy.long)
    if shortCond and tradeType != "LONG"
        strategy.entry("short", strategy.short)
    if shortCond and tradeType == "LONG"
        strategy.close("long")
    if longCond and tradeType == "SHORT"
        strategy.close("short")
    strategy.exit("XL", from_entry="long", profit=TP, loss=SL)
    strategy.exit("XS", from_entry="short", profit=TP, loss=SL)

// === END ===


```

> Detail

https://www.fmz.com/strategy/482420

> Last Modified

2025-02-18 13:35:54
