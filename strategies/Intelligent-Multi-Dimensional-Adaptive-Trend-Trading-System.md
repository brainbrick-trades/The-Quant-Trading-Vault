
> Name

Intelligent-Multi-Dimensional-Adaptive-Trend-Trading-System

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d84d37c729b47ba64160.png)
![IMG](https://www.fmz.com/upload/asset/2d8e14c8ec4104dd123df.png)



#### Overview
This strategy is an intelligent trading system that integrates multiple technical indicators, analyzing Fair Value Gaps (FVG), trend signals, and price action to identify market opportunities. The system employs a dual strategy mechanism, combining trend following and swing trading characteristics, optimizing trading performance through dynamic position management and multi-dimensional exit mechanisms. The strategy particularly emphasizes risk control, enhancing signal quality through volatility filtering and volume confirmation.

#### Strategy Principles
The core logic is based on several dimensions:
1. FVG Gap Detection - Identifying potential trading opportunities by calculating price gap sizes
2. Trend Confirmation System - Combining 200-day moving average, SuperTrend indicator, and MACD for trend confirmation
3. Smart Money Confirmation - Using RSI overbought/oversold levels, volume anomalies, and price action patterns as trade triggers
4. Dynamic Position Management - Adjusting position sizes based on ATR volatility to ensure consistent risk exposure
5. Multi-layer Exit Mechanism - Managing trade exits through a combination of trailing stops and target profits

#### Strategy Advantages
1. Strong Adaptability - Strategy automatically adjusts parameters and positions based on market volatility
2. Comprehensive Risk Control - Controls risk through multiple filters and strict position management
3. Reliable Signal Quality - Enhances trading signal accuracy through multi-dimensional indicator confirmation
4. Flexible Trading Approach - Capable of capturing both trend and range-bound market opportunities
5. Scientific Money Management - Employs percentage-based risk management for rational capital utilization

#### Strategy Risks
1. Parameter Sensitivity - Multiple parameter settings may affect strategy performance, requiring continuous optimization
2. Market Environment Dependency - False breakout signals may occur in certain market conditions
3. Slippage Impact - May face significant slippage in markets with poor liquidity
4. Computational Complexity - Multiple indicator calculations may lead to signal delays
5. High Capital Requirements - Full strategy implementation requires substantial initial capital

#### Strategy Optimization Directions
1. Indicator Weight Optimization - Introduce machine learning methods to dynamically adjust indicator weights
2. Enhanced Market Adaptability - Add market volatility adaptation mechanisms
3. Signal Filtering Improvement - Introduce more market microstructure indicators
4. Execution Mechanism Enhancement - Add intelligent order splitting mechanisms to reduce impact costs
5. Risk Control Upgrade - Implement dynamic risk budgeting system

#### Summary
The strategy constructs a complete trading system by comprehensively utilizing multiple technical indicators and trading techniques. Its strength lies in its ability to adapt to market changes while maintaining strict risk control. While there is room for optimization, it is overall a well-designed quantitative trading strategy.




> Source (PineScript)

``` pinescript
/*backtest
start: 2025-01-01 00:00:00
end: 2025-02-20 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"SOL_USDT"}]
*/

//@version=6
strategy("Adaptive Trend Signals", overlay=true, margin_long=100, margin_short=100, pyramiding=1, initial_capital=50000, default_qty_type=strategy.percent_of_equity, default_qty_value=100, commission_type=strategy.commission.percent, commission_value=0.075)

// 1. Enhanced Inputs with Debugging Options

fvgSize = input.float(0.25, "FVG Size (%)", minval=0.1, step=0.05)
atrPeriod = input.int(14, "ATR Period")  // Increased for better stability
rsiPeriod = input.int(7, "RSI Period")
useSuperTrend = input.bool(true, "Use SuperTrend Filter")
useTrendFilter = input.bool(false, "Use 200 EMA Trend Filter")  // Disabled by default
volatilityThreshold = input.float(1.0, "Volatility Threshold (ATR%)", step=0.1)  // Increased threshold
useVolume = input.bool(true, "Use Volume Confirmation")
riskPercentage = input.float(2.0, "Risk %", minval=0.1, maxval=5)

// 2. Advanced Market Filters with Trend Change Detection
var int marketTrend = 0
var bool trendChanged = false
ema200 = ta.ema(close, 200)
prevMarketTrend = marketTrend
marketTrend := close > ema200 ? 1 : close < ema200 ? -1 : 0
trendChanged := marketTrend != prevMarketTrend

// 3. Enhanced FVG Detection with Adjusted Volume Requirements
bullishFVG = (low[1] > high[2] and (low[1] - high[2])/high[2]*100 >= fvgSize) or 
             (low > high[1] and (low - high[1])/high[1]*100 >= fvgSize)

bearishFVG = (high[1] < low[2] and (low[2] - high[1])/low[2]*100 >= fvgSize) or 
             (high < low[1] and (low[1] - high)/low[1]*100 >= fvgSize)

// 4. Smart Money Confirmation System with Signal Debugging
rsi = ta.rsi(close, rsiPeriod)
[macdLine, signalLine, _] = ta.macd(close, 5, 13, 5)
[supertrendLine, supertrendDir] = ta.supertrend(3, 10)

// Script 2 Indicators
[macdLine2, signalLine2, _] = ta.macd(close, 4, 11, 3)
[supertrendLine2, supertrendDir2] = ta.supertrend(3, 7)
vWAP = ta.vwap(close)
ema21 = ta.ema(close, 21)

// 5. Price Action Filters from Script 2
breakoutLong = close > ta.highest(high, 5) and (useVolume ? volume > ta.sma(volume, 10)*1.8 : true)
breakdownShort = close < ta.lowest(low, 5) and (useVolume ? volume > ta.sma(volume, 10)*1.8 : true)
bullishRejection = low < vWAP and close > (high + low)/2 and close > open
bearishRejection = high > vWAP and close < (high + low)/2 and close < open

// 6. Combined Entry Conditions
longBaseCond = (bullishFVG and rsi < 35 and macdLine > signalLine) or
              (bullishFVG and rsi < 38 and supertrendDir2 == 1) or
              (breakoutLong and macdLine2 > signalLine2) or
              (bullishRejection and close > ema21)

shortBaseCond = (bearishFVG and rsi > 65 and macdLine < signalLine) or
               (bearishFVG and rsi > 62 and supertrendDir2 == -1) or
               (breakdownShort and macdLine2 < signalLine2) or
               (bearishRejection and close < ema21)

longSignal = longBaseCond and (not useSuperTrend or supertrendDir == 1) and (not useTrendFilter or marketTrend == 1)

shortSignal = shortBaseCond and (not useSuperTrend or supertrendDir == -1) and (not useTrendFilter or marketTrend == -1)

// 7. Position Sizing with Minimum Quantity
var float longEntryPrice = na
var float shortEntryPrice = na
atr = ta.atr(atrPeriod)
positionSizeScript1 = math.max(strategy.equity * riskPercentage / 100 / (atr * 1.5), 1)
positionSizeScript2 = strategy.equity * riskPercentage / 100 / (atr * 2)

// 8. Dynamic Exit System with Dual Strategies
var float trailPrice = na
if longSignal or trendChanged and marketTrend == 1
    trailPrice := close
if shortSignal or trendChanged and marketTrend == -1
    trailPrice := close

trailOffset = atr * 0.75

// Script 1 Exit Logic
if strategy.position_size > 0
    trailPrice := math.max(trailPrice, close)
    strategy.exit("Long Exit", "Long", stop=trailPrice - trailOffset, trail_offset=trailOffset)
    
if strategy.position_size < 0
    trailPrice := math.min(trailPrice, close)
    strategy.exit("Short Exit", "Short", stop=trailPrice + trailOffset, trail_offset=trailOffset)

// Script 2 Exit Logic
longStop = close - atr * 1.2
shortStop = close + atr * 1.2
strategy.exit("Long Exit 2", "Long", stop=longStop, limit=na(longEntryPrice) ? na : longEntryPrice + (atr * 4), trail_points=not na(longEntryPrice) and close > longEntryPrice + atr ? atr * 3 : na, trail_offset=atr * 0.8)
strategy.exit("Short Exit 2", "Short", stop=shortStop, limit=na(shortEntryPrice) ? na : shortEntryPrice - (atr * 4), trail_points=not na(shortEntryPrice) and close < shortEntryPrice - atr ? atr * 3 : na, trail_offset=atr * 0.8)

// 9. Trend Change Signals and Visuals
// plot(supertrendLine, "SuperTrend", color=color.new(#2962FF, 0))
// plot(supertrendLine2, "SuperTrend 2", color=color.new(#FF00FF, 0))
// plot(ema200, "200 EMA", color=color.new(#FF6D00, 0))
// plot(ema21, "21 EMA", color=color.new(#00FFFF, 0))

bgcolor(marketTrend == 1 ? color.new(color.green, 90) : 
       marketTrend == -1 ? color.new(color.red, 90) : na)

plotshape(trendChanged and marketTrend == 1, "Bullish Trend", shape.labelup, 
         location.belowbar, color=color.green, text="▲ Trend Up")
plotshape(trendChanged and marketTrend == -1, "Bearish Trend", shape.labeldown, 
         location.abovebar, color=color.red, text="▼ Trend Down")

// 10. Signal Visualization for Both Strategies
// plotshape(longSignal, "Long Entry", shape.triangleup, location.belowbar, 
//          color=color.new(#00FF00, 0), size=size.small)
// plotshape(shortSignal, "Short Entry", shape.triangledown, location.abovebar, 
//          color=color.new(#FF0000, 0), size=size.small)
// plotshape(breakoutLong, "Breakout Long", shape.flag, location.belowbar, 
//          color=color.new(#00FF00, 50), size=size.small)
// plotshape(breakdownShort, "Breakdown Short", shape.flag, location.abovebar, 
//          color=color.new(#FF0000, 50), size=size.small)

// 11. Order Execution with Dual Entry Systems
if trendChanged and marketTrend == 1
    strategy.entry("Long Trend", strategy.long, qty=positionSizeScript1)
    longEntryPrice := close
    
if trendChanged and marketTrend == -1
    strategy.entry("Short Trend", strategy.short, qty=positionSizeScript1)
    shortEntryPrice := close

if longSignal and strategy.position_size == 0
    strategy.entry("Long Signal", strategy.long, qty=positionSizeScript2)
    longEntryPrice := close
    
if shortSignal and strategy.position_size == 0
    strategy.entry("Short Signal", strategy.short, qty=positionSizeScript2)
    shortEntryPrice := close
    
```

> Detail

https://www.fmz.com/strategy/483069

> Last Modified

2025-02-21 11:37:36
