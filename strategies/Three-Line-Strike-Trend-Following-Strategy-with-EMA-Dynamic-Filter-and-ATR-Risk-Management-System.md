
> Name

Three-Line-Strike-Trend-Following-Strategy-with-EMA-Dynamic-Filter-and-ATR-Risk-Management-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/e4b150cc1d3518450b.png)


#### Overview
This strategy is a trend-following trading system based on the Three Line Strike candlestick pattern from Japanese technical analysis. It enhances the traditional Three Line Strike pattern's reliability by incorporating an Exponential Moving Average (EMA) as a trend filter and the Average True Range (ATR) for dynamic risk management. The strategy is designed to capture market trend reversal points while effectively managing risk, making it suitable for medium to long-term trend trading.

#### Strategy Principles
The core logic is based on several key elements: First, it identifies the Three Line Strike pattern, which consists of three consecutive candles of the same color followed by a larger engulfing candle in the opposite direction. Second, it uses EMA as a trend filter, considering long signals only when price is above EMA and short signals when price is below EMA. Finally, it utilizes the ATR indicator to dynamically set take-profit and stop-loss levels, specifically 2x ATR for take-profit and 1x ATR for stop-loss.

#### Strategy Advantages
1. Combines directional trend confirmation with reversal pattern recognition, improving trade signal reliability
2. Employs dynamic take-profit and stop-loss settings that adapt to market volatility
3. Clear strategy logic with adjustable parameters, facilitating optimization for different market characteristics
4. Significantly reduces false signals through the EMA filter, enhancing strategy stability
5. Comprehensive risk management system, including money management and stop-loss mechanisms

#### Strategy Risks
1. May generate frequent false signals in ranging markets, leading to consecutive stops
2. EMA as a lagging indicator might not respond quickly enough to sharp trend reversals
3. Fixed ATR multipliers for take-profit and stop-loss may not suit all market conditions
4. Strategy performance depends heavily on clear trend direction, potentially underperforming in trendless periods
5. Entry timing accuracy is significantly influenced by the chosen candlestick timeframe

#### Strategy Optimization Directions
1. Incorporate volume indicators as confirmation, improving signal reliability
2. Dynamically adjust EMA parameters based on different market cycles for better adaptability
3. Add trend strength filters, such as ADX indicator, to reduce false signals in ranging markets
4. Optimize take-profit and stop-loss multipliers, considering dynamic adjustments based on volatility
5. Implement market regime recognition mechanisms to use different parameter settings in different market states

#### Summary
This is a comprehensive trading system that combines classical technical analysis with modern quantitative trading concepts. By integrating the traditional Three Line Strike pattern with trend following and risk management, it creates a well-rounded trading system. While certain limitations exist, the suggested optimization directions can further enhance the strategy's robustness and adaptability. Successful implementation requires traders to deeply understand market characteristics and adjust parameters according to specific circumstances.




> Source (PineScript)

``` pinescript
/*backtest
start: 2025-01-18 00:00:00
end: 2025-02-17 00:00:00
period: 2h
basePeriod: 2h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// Copyright ...
// Based on the TMA Overlay by Arty, converted to a simple strategy example.
// Pine Script v5

//@version=5
strategy(title='3 Line Strike [TTF] - Strategy with ATR and EMA Filter',
     shorttitle='3LS Strategy [TTF]',
     overlay=true,
     initial_capital=100000,
     default_qty_type=strategy.percent_of_equity,
     default_qty_value=100,
     pyramiding=0)

// -----------------------------------------------------------------------------
//                               INPUTS
// -----------------------------------------------------------------------------

// ATR and EMA Inputs
atrLength = input.int(title='ATR Length', defval=14, group='ATR & EMA')
emaLength = input.int(title='EMA Length', defval=200, group='ATR & EMA')

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

// Calculate EMA
ema = ta.ema(close, emaLength)

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
is3LSBearSig = is3LSBear() and close < ema
is3LSBullSig = is3LSBull() and close > ema

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

https://www.fmz.com/strategy/482466

> Last Modified

2025-02-18 15:30:08
