
> Name

Three-Line-Strike-Momentum-Trend-Following-Strategy-with-ADX-Filter

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8486700014a2f32ff2b.png)
![IMG](https://www.fmz.com/upload/asset/2d8242d504d1fc683b841.png)



#### Overview
This strategy is a trend-following trading system based on the Three-Line Strike pattern combined with ADX trend filtering. It identifies breakthrough patterns after three consecutive candlesticks in the same direction, confirms trend strength using the ADX indicator, and sets dynamic take-profit and stop-loss levels using ATR. This approach ensures both signal reliability and effective risk control.

#### Strategy Principles
The core logic includes several key elements:
1. Three-Line Strike Pattern Recognition: Bullish pattern requires three consecutive red candles followed by a larger green breakout candle; bearish pattern requires three consecutive green candles followed by a larger red breakout candle.
2. ADX Trend Strength Confirmation: Uses the ADX indicator to judge current trend strength, generating trading signals only when ADX value exceeds the set threshold (default 25).
3. ATR Dynamic Take-Profit and Stop-Loss: Uses ATR values to dynamically calculate take-profit and stop-loss positions, with TP set at 2x ATR and SL at 1x ATR.
4. Trade Execution Logic: When pattern recognition and trend strength conditions are met, the system automatically executes position opening and sets corresponding TP/SL orders.

#### Strategy Advantages
1. High Signal Reliability: Combines price patterns and trend indicators for dual confirmation, significantly improving trading signal reliability.
2. Reasonable Risk Control: Uses ATR for dynamic TP/SL setting, adapting risk control parameters to market volatility.
3. High Systematization: Clear strategy logic with adjustable parameters, suitable for systematic trading.
4. Strong Adaptability: Applicable to different markets and timeframes with good universality.

#### Strategy Risks
1. False Breakout Risk: May generate false breakout signals in ranging markets, leading to trading losses.
2. Slippage Risk: Due to market order entries, significant slippage may occur in less liquid markets.
3. Parameter Sensitivity: Strategy performance is sensitive to parameters like ADX threshold and ATR period, requiring optimization for different markets.
4. Trend Dependency: Strategy may underperform in ranging markets, more suitable for trending market conditions.

#### Strategy Optimization Directions
1. Pattern Recognition Enhancement: Add more price pattern validation conditions, such as considering candlestick body-to-wick ratios.
2. Trend Confirmation Improvement: Introduce additional trend indicators like MACD or moving average crossovers for auxiliary confirmation.
3. Take-Profit/Stop-Loss Optimization: Dynamically adjust ATR multipliers based on market characteristics or implement trailing stops.
4. Trading Time Optimization: Add trading time filters to avoid trading during highly volatile market periods.

#### Summary
The Three-Line Strike Momentum Trend Following Strategy is a complete trading system combining classical price patterns and technical indicators. Through ADX trend filtering and ATR dynamic risk control, this strategy maintains trading opportunities while effectively controlling risk. Despite some limitations, through proper parameter optimization and strategy improvements, this strategy has good practical application value.





> Source (PineScript)

``` pinescript
/*backtest
start: 2024-08-11 00:00:00
end: 2025-02-19 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

// Copyright ...
// Based on the TMA Overlay by Arty, converted to a simple strategy example.
// Pine Script v5

//@version=5
strategy(title='3 Line Strike [TTF] - Strategy with ATR and ADX Filter',
     shorttitle='3LS Strategy [TTF]',
     overlay=true,
     initial_capital=100000,
     default_qty_type=strategy.percent_of_equity,
     default_qty_value=100,
     pyramiding=0)

// -----------------------------------------------------------------------------
//                               INPUTS
// -----------------------------------------------------------------------------

// ATR and ADX Inputs
atrLength = input.int(title='ATR Length', defval=14, group='ATR & ADX')
adxLength = input.int(title='ADX Length', defval=14, group='ATR & ADX')
adxThreshold = input.float(title='ADX Threshold', defval=25, group='ATR & ADX')

// ### 3 Line Strike
showBear3LS = input.bool(title='Show Bearish 3 Line Strike', defval=true, group='3 Line Strike',
     tooltip="Bearish 3 Line Strike (3LS-Bear) = 3 zelené sviečky, potom veľká červená sviečka (engulfing).")
showBull3LS = input.bool(title='Show Bullish 3 Line Strike', defval=true, group='3 Line Strike',
     tooltip="Bullish 3 Line Strike (3LS-Bull) = 3 červené sviečky, potom veľká zelená sviečka (engulfing).")

// -----------------------------------------------------------------------------
//                          CALCULATIONS
// -----------------------------------------------------------------------------

// Calculate ATR
atr = ta.atr(atrLength)

// Calculate ADX components manually
tr = ta.tr(true)
plusDM = ta.change(high) > ta.change(low) and ta.change(high) > 0 ? ta.change(high) : 0
minusDM = ta.change(low) > ta.change(high) and ta.change(low) > 0 ? ta.change(low) : 0
smoothedPlusDM = ta.rma(plusDM, adxLength)
smoothedMinusDM = ta.rma(minusDM, adxLength)
smoothedTR = ta.rma(tr, adxLength)

plusDI = (smoothedPlusDM / smoothedTR) * 100
minusDI = (smoothedMinusDM / smoothedTR) * 100

dx = math.abs(plusDI - minusDI) / (plusDI + minusDI) * 100
adx = ta.rma(dx, adxLength)

// Helper Functions
getCandleColorIndex(barIndex) =>
    int ret = na
    if (close[barIndex] > open[barIndex])
        ret := 1
    else if (close[barIndex] < open[barIndex])
        ret := -1
    else
        ret := 0
    ret

isEngulfing(checkBearish) =>
    sizePrevCandle = close[1] - open[1]
    sizeCurrentCandle = close - open
    isCurrentLargerThanPrevious = math.abs(sizeCurrentCandle) > math.abs(sizePrevCandle)

    if checkBearish
        isGreenToRed = (getCandleColorIndex(0) < 0) and (getCandleColorIndex(1) > 0)
        isCurrentLargerThanPrevious and isGreenToRed
    else
        isRedToGreen = (getCandleColorIndex(0) > 0) and (getCandleColorIndex(1) < 0)
        isCurrentLargerThanPrevious and isRedToGreen

isBearishEngulfing() => isEngulfing(true)
isBullishEngulfing() => isEngulfing(false)

is3LSBear() =>
    is3LineSetup = (getCandleColorIndex(1) > 0) and (getCandleColorIndex(2) > 0) and (getCandleColorIndex(3) > 0)
    is3LineSetup and isBearishEngulfing()

is3LSBull() =>
    is3LineSetup = (getCandleColorIndex(1) < 0) and (getCandleColorIndex(2) < 0) and (getCandleColorIndex(3) < 0)
    is3LineSetup and isBullishEngulfing()

// Signals
is3LSBearSig = is3LSBear() and adx > adxThreshold
is3LSBullSig = is3LSBull() and adx > adxThreshold

// Take Profit and Stop Loss
longTP = close + 2 * atr
longSL = close - 1 * atr
shortTP = close - 2 * atr
shortSL = close + 1 * atr

// -----------------------------------------------------------------------------
//                          STRATEGY ENTRY PRÍKAZY
// -----------------------------------------------------------------------------
if (showBull3LS and is3LSBullSig)
    strategy.entry("3LS_Bull", strategy.long, comment="3LS Bullish")
    strategy.exit("Exit Bull", from_entry="3LS_Bull", limit=longTP, stop=longSL)

if (showBear3LS and is3LSBearSig)
    strategy.entry("3LS_Bear", strategy.short, comment="3LS Bearish")
    strategy.exit("Exit Bear", from_entry="3LS_Bear", limit=shortTP, stop=shortSL)

```

> Detail

https://www.fmz.com/strategy/482921

> Last Modified

2025-02-20 17:46:30
