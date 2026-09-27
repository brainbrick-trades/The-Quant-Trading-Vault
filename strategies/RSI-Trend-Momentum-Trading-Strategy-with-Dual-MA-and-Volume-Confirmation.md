
> Name

RSI-Trend-Momentum-Trading-Strategy-with-Dual-MA-and-Volume-Confirmation

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/11f03a3366467bafaf4.png)


#### Overview
This strategy is a trend-following system that combines RSI oversold signals, long-term moving averages, and volume confirmation. It aims to capture long positions during oversold conditions within established uptrends, validated by volume expansion. The strategy utilizes a 10-period RSI, dual SMAs of 250 and 500 periods, and a 20-period volume moving average as core indicators.

#### Strategy Principles
The core logic is based on three key conditions working in harmony:
1. RSI oversold signal (RSI<=30): Captures market rebound opportunities
2. Dual MA bullish alignment (SMA250>SMA500): Confirms long-term uptrend
3. Volume confirmation (Current volume>20-period volume MA*2.5): Validates price movements

A long position is initiated when all three conditions are met simultaneously. The exit signal is triggered by a death cross (shorter MA crossing below longer MA). Additionally, a 5% stop-loss is implemented for risk management.

#### Strategy Advantages
1. Multiple confirmation reduces false signals: Integration of RSI, MAs, and volume provides robust signal filtering
2. Trend-following characteristics: Long-term MAs prevent counter-trend trading
3. Comprehensive risk control: Fixed stop-loss effectively manages per-trade risk
4. High adaptability: Parameters can be adjusted for different market conditions
5. Strict trade selection: Multiple conditions ensure optimal entry timing

#### Strategy Risks
1. Lag risk: Long-period MAs introduce significant delay in trend identification
2. Over-filtering risk: Strict multiple conditions might miss valid trading opportunities
3. Ranging market risk: False signals may occur frequently in sideways markets
4. Stop-loss configuration risk: Fixed percentage stops may not suit all market conditions
5. Parameter optimization risk: Over-optimization may lead to poor live trading performance

#### Optimization Directions
1. Dynamic stop-loss: Consider implementing ATR or volatility-based dynamic stops
2. Trend strength quantification: Incorporate ADX or similar indicators for better trend assessment
3. Position sizing optimization: Adjust position size based on signal strength and market volatility
4. Exit mechanism enhancement: Add profit targets and trailing stops for flexible exits
5. Time filtering: Implement trading time filters to avoid inefficient periods

#### Summary
This is a well-designed trend-following strategy with rigorous logic, effectively balancing returns and risks through multiple technical indicators. Its core strengths lie in comprehensive signal confirmation and risk management systems, though it faces challenges in over-filtering and latency. Through the suggested optimization directions, the strategy shows potential for improved performance in practical applications.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-27 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/


// This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/
// © wielkieef

//@version=5
strategy(title=' Rsi Long-Term Strategy [15min]', overlay=true, pyramiding=1, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100, calc_on_order_fills=false, slippage=0, commission_type=strategy.commission.percent, commission_value=0.03)

// Rsi
rsi_lenght = input.int(10, title='RSI lenght', minval=0)
rsi_up = ta.rma(math.max(ta.change(close), 0), rsi_lenght)
rsi_down = ta.rma(-math.min(ta.change(close), 0), rsi_lenght)
rsi_value = rsi_down == 0 ? 100 : rsi_up == 0 ? 0 : 100 - 100 / (1 + rsi_up / rsi_down)
rsi_overs = rsi_value <= 30
rsi_overb = rsi_value >= 70

// Volume
vol_sma_length = input.int(20, title='Volume lenght  ', minval=1)
Volume_condt = volume > ta.sma(volume, vol_sma_length) * 2.5

//SMA1
lengthSMA1 = input(250, title="Lenght SMA 1")
SMA1 = ta.sma(close, lengthSMA1)
//plot(SMA1, color=color.rgb(245, 108, 3), linewidth=1, title="SMA250")

//SMA2
lengthSMA2 = input(500, title="Lenght SMA 2")
SMA2 = ta.sma(close, lengthSMA2)
//plot(SMA2, color=#9803f5, linewidth=1, title="SMA500")


//Entry Logic
Long_cond = (rsi_overs and SMA1 > SMA2 and Volume_condt )  

if Long_cond
    strategy.entry('Long', strategy.long)

//Close Logic
Long_close = ta.crossunder(SMA1,SMA2)

if Long_close
    strategy.close("Long")

//Bar colors
Bar_color = Volume_condt ? #fc9802 : SMA1 > SMA2 ? color.rgb(84, 252, 0) : SMA1 < SMA2 ? color.maroon : color.gray
barcolor(color=Bar_color)

// Rsi value Plotshapes
plotshape(rsi_value < 30 and SMA1 > SMA2 and Volume_condt, title='Buy', color=color.new(color.green, 0), style=shape.circle, location=location.belowbar, size=size.tiny, textcolor=color.new(color.black, 0))
plotshape(rsi_value > 70 and SMA1 < SMA2 and Volume_condt, title='Sell', color=color.new(color.red, 0), style=shape.circle, location=location.abovebar, size=size.tiny, textcolor=color.new(color.black, 0))
plotshape(ta.crossunder(SMA1,SMA2) , title='DEATH CROSS', color=#000000, style=shape.xcross, location=location.abovebar, size=size.small, textcolor=color.new(color.black, 0))

//Stop-Loss// this code is from author RafaelZioni, modified by wielkieef
pera(pcnt) =>
    strategy.position_size != 0 ? math.round(pcnt / 100 * strategy.position_avg_price / syminfo.mintick) : float(na)
stoploss = input.float(title=' stop loss', defval=5.0, minval=0.5)
los = pera(stoploss)
strategy.exit('SL', loss=los)




// by wielkieef
```

> Detail

https://www.fmz.com/strategy/473261

> Last Modified

2024-11-28 17:02:32
