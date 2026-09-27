
> Name

Multi-Indicator-Synergistic-Trend-Following-Strategy-with-Dynamic-Stop-Loss-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1a6d8c747a4c80a50a6.png)


#### Overview
This strategy is a trend following trading system that combines multiple technical indicators. It integrates market signals from various dimensions including Moving Average (EMA), Volatility Tracking (ATR), Volume Trend (PVT), and Momentum Oscillator (Ninja) to improve trading accuracy. The strategy employs a dynamic stop-loss mechanism to strictly control risk while tracking trends.

#### Strategy Principles
The core logic is built on four main pillars:
1. Using 200-period EMA as the primary trend determination basis, dividing the market into bullish and bearish states
2. Chandelier Exit system based on ATR, determining trend turning points by tracking highs and lows combined with volatility
3. PVT indicator combining price changes with volume to confirm price trend validity
4. Ninja oscillator capturing market momentum changes by comparing short-term and medium-term moving averages

Trading signals are generated under the following conditions:
- Long: Price above 200EMA, Chandelier Exit shows buy signal, confirmed by either PVT or Ninja indicator
- Short: Price below 200EMA, Chandelier Exit shows sell signal, confirmed by either PVT or Ninja indicator

#### Strategy Advantages
1. Multi-indicator synergistic confirmation significantly reduces false breakout risks
2. Incorporates market information from multiple dimensions including trend, volatility, volume, and momentum
3. Dynamic stop-loss mechanism automatically adjusts stop positions based on market volatility
4. Systematic trading rules reduce interference from subjective judgments
5. Robust risk control mechanism with clear stop-loss levels for each trade

#### Strategy Risks
1. May generate frequent false signals in ranging markets
2. Multiple confirmation mechanisms might lead to slightly delayed entries
3. Stop-loss positions may be relatively loose during rapid market reversals
4. Parameter optimization may risk overfitting
5. Requires substantial capital buffer to withstand drawdowns

#### Strategy Optimization Directions
1. Introduce market environment recognition mechanism to use different parameter combinations in different market states
2. Add trading volume analysis dimension to optimize position management system
3. Consider adding volatility-based dynamic parameter adjustment mechanism
4. Optimize weight distribution among multiple indicators
5. Introduce time filters to avoid periods of high market volatility

#### Summary
This strategy constructs a relatively complete trading system through multi-indicator synergy and dynamic stop-loss mechanism. Its core advantages lie in multi-dimensional signal confirmation and strict risk control. While there are risks of lag and false signals, through continuous optimization and improvement, the strategy has the potential to maintain stable performance across different market environments. Traders are advised to conduct thorough backtesting and parameter optimization before live trading.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-11-12 00:00:00
end: 2024-12-11 08:00:00
period: 2h
basePeriod: 2h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Triple Indicator Strategy", shorttitle="TIS", overlay=true)

// --- Inputs ---
var string calcGroup = "Calculation Parameters"
atrLength = input.int(22, title="ATR Period", group=calcGroup)
atrMult = input.float(3.0, title="ATR Multiplier", step=0.1, group=calcGroup)
emaLength = input.int(200, title="EMA Length", group=calcGroup)

// --- ATR and EMA Calculations ---
atr = atrMult * ta.atr(atrLength)
ema200 = ta.ema(close, emaLength)

// --- Chandelier Exit Logic ---
longStop = ta.highest(high, atrLength) - atr
shortStop = ta.lowest(low, atrLength) + atr

var int dir = 1
dir := close > shortStop ? 1 : close < longStop ? -1 : dir

buySignal = dir == 1 and dir[1] == -1
sellSignal = dir == -1 and dir[1] == 1

// --- Price Volume Trend (PVT) ---
pvt = ta.cum((close - close[1]) / close[1] * volume)
pvtSignal = ta.ema(pvt, 21)
pvtBuy = ta.crossover(pvt, pvtSignal)
pvtSell = ta.crossunder(pvt, pvtSignal)

// --- Ninja Indicator ---
ninjaOsc = (ta.ema(close, 3) - ta.ema(close, 13)) / ta.ema(close, 13) * 100
ninjaSignal = ta.ema(ninjaOsc, 24)
ninjaBuy = ta.crossover(ninjaOsc, ninjaSignal)
ninjaSell = ta.crossunder(ninjaOsc, ninjaSignal)

// --- Strategy Conditions ---
longCondition = buySignal and close > ema200 and (pvtBuy or ninjaBuy)
shortCondition = sellSignal and close < ema200 and (pvtSell or ninjaSell)

if longCondition
    strategy.entry("Buy", strategy.long)
    strategy.exit("Exit Long", "Buy", stop=low - atr)

if shortCondition
    strategy.entry("Sell", strategy.short)
    strategy.exit("Exit Short", "Sell", stop=high + atr)

// --- Plotting ---
plot(ema200, title="EMA 200", color=color.blue, linewidth=2)
plotshape(buySignal, title="Chandelier Buy", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
plotshape(sellSignal, title="Chandelier Sell", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)

// --- Labels for Buy/Sell with price ---
if buySignal
    label.new(bar_index, low, "Buy: " + str.tostring(close), color=color.green, style=label.style_label_up, yloc=yloc.belowbar, size=size.small)

if sellSignal
    label.new(bar_index, high, "Sell: " + str.tostring(close), color=color.red, style=label.style_label_down, yloc=yloc.abovebar, size=size.small)

// --- Alerts ---
alertcondition(longCondition, title="Buy Alert", message="Buy Signal Triggered!")
alertcondition(shortCondition, title="Sell Alert", message="Sell Signal Triggered!")
```

> Detail

https://www.fmz.com/strategy/474978

> Last Modified

2024-12-13 11:45:19
