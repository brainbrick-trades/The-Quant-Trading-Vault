
> Name

Adaptive-EMA-Dynamic-Position-Break-out-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/762c3cfcf250c6f722.png)


#### Overview
This strategy is an adaptive trading system based on a dual moving average system, which identifies buy signals through the crossover of fast moving average (EMA25) and slow moving average (EMA100), combined with dynamic stop-loss and profit targets to optimize trading performance. The strategy adopts a breakout trading approach, focusing on risk control while ensuring returns, suitable for medium to long-term trend trading.

#### Strategy Principle
The core logic of the strategy includes three key components:
1. Signal System: Using EMA25 crossing above EMA100 to generate long signals, which typically indicates the beginning of an uptrend.
2. Risk Control: Using the lowest point of the most recent red candle below EMA100 as the stop-loss point, effectively preventing losses from false breakouts.
3. Profit Management: Adopting a 1:3 risk-reward ratio for profit targets, and automatically adjusting the stop-loss to breakeven when reaching 2% profit, achieving risk-free position holding.

#### Strategy Advantages
1. High Signal Reliability: Using slow EMA for trend confirmation effectively filters false signals.
2. Comprehensive Risk Control: Dynamic stop-loss settings and breakout confirmation mechanism reduce trading risks.
3. Stable Return Characteristics: Reasonable risk-reward ratio setting improves strategy's expected returns.
4. High Automation Level: Includes complete signal generation, stop-loss/take-profit, and position management logic.
5. Strong Adaptability: Parameters can be adjusted according to different market conditions.

#### Strategy Risks
1. Oscillating Market Risk: May trigger frequent stop-losses in sideways markets.
2. Slippage Risk: May face execution slippage during high volatility periods.
3. False Breakout Risk: Moving average crossover signals may produce false breakouts.
4. Parameter Sensitivity: Moving average period settings significantly impact strategy performance.

#### Strategy Optimization Directions
1. Incorporate Volume Confirmation: Add volume indicators to the signal system to improve breakout reliability.
2. Optimize Stop-Loss Mechanism: Consider introducing ATR dynamic stop-loss for better adaptability.
3. Add Trend Strength Filtering: Include trend strength indicators like ADX to optimize entry timing.
4. Perfect Position Management: Dynamically adjust position size based on volatility.
5. Include Market Environment Assessment: Introduce market regime identification mechanism to adopt different parameter settings in different market environments.

#### Summary
The strategy captures trend initiation points through moving average crossovers, coupled with dynamic stop-loss and profit management mechanisms, achieving favorable risk-reward characteristics. The strategy design fully considers practical requirements and demonstrates strong practicality. Through the suggested optimization directions, the strategy's stability and adaptability can be further enhanced. It is suitable for traders with strong risk tolerance who pursue medium to long-term stable returns.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-18 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("EMA Crossover with TP and SL (Buy only) and Break-even", overlay=true)

// EMA sozlamalari
emaFastLength = input.int(25, title="Fast EMA Length")
emaSlowLength = input.int(100, title="Slow EMA Length")

// Hisoblash
emaFast = ta.ema(close, emaFastLength)
emaSlow = ta.ema(close, emaSlowLength)

// Kesishishni aniqlash
bullishCross = ta.crossover(emaFast, emaSlow) // EMA 25 EMA 100 ni yuqoriga kesib o'tganda

// EMA 100 tagidagi oxirgi qizil shamning tagini olish
lastRedCandleLow = ta.valuewhen(close < open and close < emaSlow, low, 0) // EMA 100 pastidagi qizil shamning tagi

// TP va SL darajalarini hisoblash
longSL = lastRedCandleLow
longTP = close + 3 * (close - longSL) // TP SL ga nisbatan 1:2 masofada

// Savdoni ochish va 2% foyda bo'lganda SLni break-even ga o'zgartirish
if (bullishCross)
    strategy.entry("Buy", strategy.long)  // Buy pozitsiyasini ochish
    strategy.exit("Exit Buy", "Buy", stop=longSL, limit=longTP)  // SL va TP qo'yish

    // 2% foyda bo'lganda SLni break-even ga o'zgartirish
    if (strategy.position_size > 0)
        profitPercentage = (close - strategy.position_avg_price) / strategy.position_avg_price * 100
        if (profitPercentage >= 2)
            strategy.exit("Exit Buy BE", "Buy", stop=strategy.position_avg_price) // SLni break-even ga o'zgartirish

// Signalni ko'rsatish
plotshape(bullishCross, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")

// // TP va SL chizish
// if (bullishCross)
//     line.new(x1=bar_index, y1=longSL, x2=bar_index+1, y2=longSL, color=color.red, width=1, extend=extend.none)
//     line.new(x1=bar_index, y1=longTP, x2=bar_index+1, y2=longTP, color=color.green, width=1, extend=extend.none)
//     label.new(bar_index, longSL, text="SL: " + str.tostring(longSL), style=label.style_label_down, color=color.red, textcolor=color.white, size=size.small)
//     label.new(bar_index, longTP, text="TP: " + str.tostring(longTP), style=label.style_label_up, color=color.green, textcolor=color.white, size=size.small)

// EMA chizish
plot(emaFast, color=color.blue, title="Fast EMA (25)")
plot(emaSlow, color=color.orange, title="Slow EMA (100)")

// Alert qo'shish
alertcondition(bullishCross, title="Buy Signal Alert", message="EMA 25 crossed above EMA 100! Buy Signal!")

```

> Detail

https://www.fmz.com/strategy/475627

> Last Modified

2024-12-20 16:33:20
