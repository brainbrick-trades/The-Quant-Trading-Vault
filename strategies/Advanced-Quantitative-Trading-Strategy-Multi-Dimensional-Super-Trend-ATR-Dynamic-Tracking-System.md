
> Name

Advanced-Quantitative-Trading-Strategy-Multi-Dimensional-Super-Trend-ATR-Dynamic-Tracking-System

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d87a1da55b5e6d08c5a7.png)
![IMG](https://www.fmz.com/upload/asset/2d80b27889c701b37302e.png)




#### Overview
This strategy is a quantitative trading system based on multiple technical indicators, primarily driven by the SuperTrend indicator, combined with ATR dynamic stop-loss mechanism, and utilizing MACD, ADX, RSI, and other indicators for multi-dimensional trend confirmation and risk control. The strategy employs a six-layer filtering mechanism to identify high-probability trading opportunities while incorporating triple divergence detection for early market risk warning.

#### Strategy Principles
The strategy uses SuperTrend indicator as its core, calculating trend direction through factor and ATR parameters. Entry signals must satisfy the following conditions:
1. SuperTrend direction indication
2. MACD histogram position verification
3. ADX trend strength confirmation
4. Candlestick pattern confirmation
5. Volume expansion verification
6. Triple divergence detection

The system implements ATR dynamic stop-loss for risk control and manages positions based on trend reversal signals.

#### Strategy Advantages
1. Multi-dimensional indicator fusion improves signal reliability
2. ATR dynamic stop-loss mechanism adapts to market volatility
3. Triple divergence detection system provides risk warnings
4. Volume verification ensures trading activity
5. Gas fee filtering mechanism reduces transaction costs
6. Complete visualization system facilitates strategy monitoring

#### Strategy Risks
1. Multiple filters may cause missed trading opportunities
2. Parameter optimization faces overfitting risks
3. High market volatility periods may trigger frequent stop-losses
4. Gas fee fluctuations may affect strategy returns
5. Indicator combinations may generate chaotic signals in sideways markets

#### Strategy Optimization Directions
1. Introduce market cycle recognition module for parameter adaptation
2. Develop machine learning-based signal weighting system
3. Optimize Gas fee prediction model for better timing
4. Add transaction cost calculation module
5. Develop volatility-based position management system

#### Summary
This strategy constructs a robust quantitative trading system through multi-dimensional indicator fusion and strict risk control. The modular design facilitates subsequent optimization and expansion, but parameter tuning and market adaptability need attention in practical applications. Innovative designs such as triple divergence warning and Gas fee filtering further enhance the strategy's practicality.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-22 00:00:00
end: 2025-02-19 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=6
strategy("ETH Super trend enhancement strategy-Simplified version", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

// ---------- Parameter configuration area ----------
// Super trend parameters
atrPeriod = input.int(8, "ATRtimeframe(8-10)", minval=8, maxval=10)
factor = input.float(3.5, "Multiplier(3.5-4)", minval=3.5, maxval=4, step=0.1)

// MACDParameters
fastLength = input.int(10, "MACDFast line cycle")
slowLength = input.int(21, "MACDSlow line cycle")
signalLength = input.int(7, "Signal line period")

// ADXParameters
adxLength = input.int(18, "ADXtimeframe")
adxThreshold = input.int(28, "ADXTrend Threshold")

// Volume verification
volFilterRatio = input.float(1.8, "Trading volume amplification multiple", step=0.1)

// ATRstop loss
atrStopMulti = input.float(2.2, "ATRStop Loss Multiplier", step=0.1)

// ---------- Core indicator calculations ----------
// 1. Supertrend (fixed index usage))
[supertrend, direction] = ta.supertrend(factor, atrPeriod)
plot(supertrend, color=direction < 0 ? color.new(color.green, 0) : color.new(color.red, 0), linewidth=2)

// 2. MACDIndicator
[macdLine, signalLine, histLine] = ta.macd(close, fastLength, slowLength, signalLength)
macdCol = histLine > histLine[1] ? color.green : color.red

// 3. ADXTrend Strength
[DIMinus, DIPlus, ADX] = ta.dmi(adxLength, adxLength)

// 4. Volume verification
volMA = ta.sma(volume, 20)
volValid = volume > volMA * volFilterRatio

// 5. ATRDynamic Stop Loss
atrVal = ta.atr(14)
var float stopPrice = na

// ---------- Triple divergence detection ----------
// RSIDivergence Detection
rsiVal = ta.rsi(close, 14)
priceHigh = ta.highest(high, 5)
rsiHigh = ta.highest(rsiVal, 5)
divergenceRSI = high >= priceHigh[1] and rsiVal < rsiHigh[1]

// MACDHistogram Divergence
macdHigh = ta.highest(histLine, 5)
divergenceMACD = high >= priceHigh[1] and histLine < macdHigh[1]

// Volume Divergence
volHigh = ta.highest(volume, 5)
divergenceVol = high >= priceHigh[1] and volume < volHigh[1]

tripleDivergence = divergenceRSI and divergenceMACD and divergenceVol

// ---------- Signal generation logic ----------
// Bullish Condition(6Layer Filter)
longCondition = 
  direction < 0 and            // Supertrend Bullish
  histLine > 0 and             // MACDBars Above Zero Line
  ADX > adxThreshold and       // Trend Strength Qualified
  close > open and             // Bull Candle Confirmation
  volValid and                 // Volume verification
  not tripleDivergence         // No Triple Top Divergence

// Short conditions (simplified conditions))
shortCondition = 
  direction > 0 and            // Supertrend Bearish
  histLine < 0 and             // MACDBars Below Zero Line
  ADX > adxThreshold and       // Trend Strength Qualified
  close < open and             // Bear Candle Confirmation
  volValid and                 // Volume verification
  tripleDivergence             // Triple top divergence appears

// ---------- Trade Execution Module ----------
if (longCondition)
    strategy.entry("Long", strategy.long)
    stopPrice := close - atrVal * atrStopMulti

if (shortCondition)
    strategy.entry("Short", strategy.short)
    stopPrice := close + atrVal * atrStopMulti

// Trailing Stop Triggered
strategy.exit("Exit Long", "Long", stop=stopPrice)
strategy.exit("Exit Short", "Short", stop=stopPrice)

// Trend Reversal Exit
if (direction > 0 and strategy.position_size > 0)
    strategy.close("Long")
    
if (direction < 0 and strategy.position_size < 0)
    strategy.close("Short")

// ---------- Visual Prompt ----------
plotshape(longCondition, style=shape.triangleup, location=location.belowbar, color=color.green, size=size.small, title="Buy Signal")
plotshape(shortCondition, style=shape.triangledown, location=location.abovebar, color=color.red, size=size.small, title="Sell Signal")
plot(strategy.position_size != 0 ? stopPrice : na, color=color.orange, style=plot.style_linebr, linewidth=2, title="Dynamic Stop-loss Line")

// ---------- Alert System ----------
alertcondition(tripleDivergence, title="Triple top divergence warning", message="ETH has a triple top divergence!")

longCondition := longCondition 
```

> Detail

https://www.fmz.com/strategy/483101

> Last Modified

2025-02-21 13:34:24
