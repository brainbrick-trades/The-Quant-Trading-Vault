
> Name

EMA-SMA-Trend-Following-with-Swing-Trading-Strategy-Combined-Volume-Filter-and-Percentage-Take-Profit-Stop-Loss-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/f82369ecfc33395bad.png)


#### Overview
This strategy is a comprehensive trading system that combines trend following with swing trading methods, utilizing EMA and SMA crossovers, swing high/low identification, volume filtering, and percentage-based take-profit and trailing stop-loss mechanisms. The strategy emphasizes multi-dimensional signal confirmation, enhancing trading accuracy through the synergy of technical indicators.

#### Strategy Principles
The strategy employs a multi-layered signal filtering mechanism, starting with EMA(10) and SMA(21) crossovers for basic trend determination, then using 6-bar left/right pivot point breakouts for entry timing, while requiring volume above the 200-period moving average to ensure sufficient liquidity. The system uses 2% take-profit and 1% trailing stop-loss for risk management. Long positions are initiated when price breaks above swing highs with volume confirmation; short positions are taken when price breaks below swing lows with volume confirmation.

#### Strategy Advantages
1. Multiple signal confirmation reduces false signals through trend, price breakout, and volume expansion verification
2. Flexible profit/loss management using percentage-based take-profit with trailing stop-loss
3. Comprehensive visualization system for monitoring trades and signals
4. High customizability with adjustable key parameters
5. Systematic risk management through preset stop-loss and take-profit levels

#### Strategy Risks
1. Potential false breakouts in ranging markets
2. Volume filtering may miss some valid signals
3. Fixed percentage take-profit might exit too early in strong trends
4. Moving average system has inherent lag in quick reversals
5. Need to consider impact of trading costs on strategy returns

#### Optimization Directions
1. Introduce volatility adaptation for dynamic adjustment of take-profit/stop-loss
2. Add trend strength filtering to avoid trading in weak trends
3. Optimize volume filtering algorithm considering relative volume changes
4. Implement time-based filters to avoid unfavorable trading periods
5. Consider market regime classification for parameter adaptation

#### Summary
The strategy builds a complete trading system through moving averages, price breakouts, and volume verification, suitable for medium to long-term trend following. Its strengths lie in multiple signal confirmation and comprehensive risk management, though performance in ranging markets needs attention. Through the suggested optimizations, particularly in adaptability, the strategy has room for improvement in stability and performance.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-09 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
// Strategy combining EMA/SMA Crossover, Swing High/Low, Volume Filtering, and Percentage TP & Trailing Stop
strategy("Swing High/Low Strategy with Volume, EMA/SMA Crossovers, Percentage TP and Trailing Stop", overlay=true)

// --- Inputs ---
source = close
TITLE = input(false, title='Enable Alerts & Background Color for EMA/SMA Crossovers')
turnonAlerts = input(true, title='Turn on Alerts?')
colorbars = input(true, title="Color Bars?")
turnonEMASMA = input(true, title='Turn on EMA1 & SMA2?')
backgroundcolor = input(false, title='Enable Background Color?')

// EMA/SMA Lengths
emaLength = input.int(10, minval=1, title='EMA Length')
smaLength = input.int(21, minval=1, title='SMA Length')
ema1 = ta.ema(source, emaLength)
sma2 = ta.sma(source, smaLength)

// Swing High/Low Lengths
leftBars = input.int(6, title="Left Bars for Swing High/Low", minval=1)
rightBars = input.int(6, title="Right Bars for Swing High/Low", minval=1)

// Volume MA Length
volMaLength = input.int(200, title="Volume Moving Average Length")

// Percentage Take Profit with hundredth place adjustment
takeProfitPercent = input.float(2.00, title="Take Profit Percentage (%)", minval=0.01, step=0.01) / 100

// Trailing Stop Loss Option
useTrailingStop = input.bool(true, title="Enable Trailing Stop Loss?")
trailingStopPercent = input.float(1.00, title="Trailing Stop Loss Percentage (%)", minval=0.01, step=0.01) / 100

// --- Swing High/Low Logic ---
pivotHigh(_leftBars, _rightBars) =>
    ta.pivothigh(_leftBars, _rightBars)

pivotLow(_leftBars, _rightBars) =>
    ta.pivotlow(_leftBars, _rightBars)

ph = fixnan(pivotHigh(leftBars, rightBars))
pl = fixnan(pivotLow(leftBars, rightBars))

// --- Volume Condition ---
volMa = ta.sma(volume, volMaLength)

// Declare exit conditions as 'var' so they are initialized
var bool longExitCondition = na
var bool shortExitCondition = na

// --- Long Entry Condition: Close above Swing High & Volume >= 200 MA ---
longCondition = (close > ph and volume >= volMa)
if (longCondition)
    strategy.entry("Long", strategy.long)

// --- Short Entry Condition: Close below Swing Low & Volume >= 200 MA ---
shortCondition = (close < pl and volume >= volMa)
if (shortCondition)
    strategy.entry("Short", strategy.short)

// --- Take Profit and Trailing Stop Logic ---

// For long position: Set take profit at the entry price + takeProfitPercent
longTakeProfitLevel = strategy.position_avg_price * (1 + takeProfitPercent)
shortTakeProfitLevel = strategy.position_avg_price * (1 - takeProfitPercent)

// --- Long Exit Logic ---
if (useTrailingStop)
    // Trailing Stop for Long
    strategy.exit("Long Exit", "Long", stop=na, trail_offset=strategy.position_avg_price * trailingStopPercent, limit=longTakeProfitLevel)
else
    // Exit Long on Take Profit only
    strategy.exit("Long Exit", "Long", limit=longTakeProfitLevel)

// --- Short Exit Logic ---
if (useTrailingStop)
    // Trailing Stop for Short
    strategy.exit("Short Exit", "Short", stop=na, trail_offset=strategy.position_avg_price * trailingStopPercent, limit=shortTakeProfitLevel)
else
    // Exit Short on Take Profit only
    strategy.exit("Short Exit", "Short", limit=shortTakeProfitLevel)

// --- Plot Swing High/Low ---

plot(ph, style=plot.style_circles, linewidth=1, color=color.blue, offset=-rightBars, title="Swing High")
plot(ph, style=plot.style_line, linewidth=1, color=color.blue, offset=0, title="Swing High")
plot(pl, style=plot.style_circles, linewidth=1, color=color.red, offset=-rightBars, title="Swing High")
plot(pl, style=plot.style_line, linewidth=1, color=color.red, offset=0, title="Swing High")
// --- Plot EMA/SMA ---
plot(turnonEMASMA ? ema1 : na, color=color.green, title="EMA")
plot(turnonEMASMA ? sma2 : na, color=color.orange, title="SMA")

// --- Alerts ---
alertcondition(longCondition, title="Long Entry", message="Price closed above Swing High with Volume >= 200 MA")
alertcondition(shortCondition, title="Short Entry", message="Price closed below Swing Low with Volume >= 200 MA")

// --- Bar Colors for Visualization ---
barcolor(longCondition ? color.green : na, title="Long Entry Color")
barcolor(shortCondition ? color.red : na, title="Short Entry Color")
bgcolor(backgroundcolor ? (ema1 > sma2 ? color.new(color.green, 50) : color.new(color.red, 50)) : na)
```

> Detail

https://www.fmz.com/strategy/474676

> Last Modified

2024-12-11 15:12:35
