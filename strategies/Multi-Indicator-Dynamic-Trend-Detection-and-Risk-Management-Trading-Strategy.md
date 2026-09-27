
> Name

Multi-Indicator-Dynamic-Trend-Detection-and-Risk-Management-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/13a9d64c17f594a0675.png)


#### Overview
This strategy is an automated trading system that combines multiple technical indicators, primarily using RSI (Relative Strength Index), CHOP (Choppiness Index), and Stochastic indicators to identify market trends while managing trading risks through dynamic take-profit and stop-loss mechanisms. The strategy operates on a 5-minute timeframe for scalping trades, utilizing multiple indicator cross-validation to enhance trading accuracy and reliability.

#### Strategy Principle
The strategy employs four core indicators for trend detection and trade signal generation:
1. RSI for identifying overbought/oversold conditions (RSI<30 oversold, >70 overbought)
2. CHOP Index for determining market choppiness (<50 indicates clear trend)
3. Stochastic K and D line crossovers for trade timing confirmation
4. SMA (Simple Moving Average) for overall trend assistance

Trading rules are:
- Long Entry: RSI<30 + CHOP<50 + K line crosses above D line
- Short Entry: RSI>70 + CHOP<50 + K line crosses below D line
The strategy implements percentage-based dynamic take-profit and stop-loss levels for risk control.

#### Strategy Advantages
1. Multiple indicator cross-validation enhances signal reliability
2. CHOP Index filters out choppy markets, reducing false signals
3. Dynamic TP/SL mechanism automatically adjusts risk management levels based on entry price
4. 5-minute timeframe suitable for scalping, reducing holding risk
5. Adjustable indicator parameters provide strong adaptability

#### Strategy Risks
1. Multiple indicator combination may lead to delayed signals
2. Potential missed opportunities in highly volatile markets
3. Fixed percentage TP/SL may not suit all market conditions
4. Short timeframe trading susceptible to market noise
Risk mitigation through proper money management and position sizing is recommended.

#### Optimization Directions
1. Implement adaptive parameter mechanism based on market volatility
2. Add volume indicator validation to enhance signal effectiveness
3. Develop dynamic TP/SL algorithm adjusting to market volatility
4. Add trend strength filter for better trade opportunity selection
5. Consider time-based filters to avoid high volatility periods

#### Summary
This strategy builds a relatively complete trading system through multiple indicator combination and strict risk control. While there are areas for optimization, the overall design is clear and has practical application value. Through continuous optimization and parameter adjustment, the strategy's stability and profitability can be further enhanced.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-12-17 00:00:00
end: 2025-01-16 00:00:00
period: 4h
basePeriod: 4h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT","balance":49999}]
*/

//@version=5
strategy("RSI + CHOP + Stochastic Strategy", overlay=true)

// Parametry wskaźników
rsiPeriod = input(14, title="RSI Period")
chopPeriod = input(14, title="Choppiness Period")
stochK = input(14, title="Stochastic K Period")
stochD = input(3, title="Stochastic D Period")
stochSmoothK = input(3, title="Stochastic Smooth K Period")
smaPeriod = input(50, title="SMA Period")

// Parametry Take Profit i Stop Loss
longTakeProfitPct = input.float(1.0, title="Long Take Profit %", minval=0.1, step=0.1) / 100
longStopLossPct = input.float(5.0, title="Long Stop Loss %", minval=0.1, step=0.1) / 100
shortTakeProfitPct = input.float(1.0, title="Short Take Profit %", minval=0.1, step=0.1) / 100
shortStopLossPct = input.float(5.0, title="Short Stop Loss %", minval=0.1, step=0.1) / 100

// Obliczenia wskaźników
rsiValue = ta.rsi(close, rsiPeriod)

highLowRange = ta.highest(high, chopPeriod) - ta.lowest(low, chopPeriod)
chopIndex = 100 * math.log10(highLowRange / ta.sma(close, chopPeriod)) / math.log10(2)

stoch = ta.stoch(close, high, low, stochK)
k = stoch[0]
d = stoch[1]

// Obliczenia SMA
smaValue = ta.sma(close, smaPeriod)

// Warunki kupna i sprzedaży
buyCondition = (rsiValue < 30) and (chopIndex < 50) and (ta.crossover(k, d))
sellCondition = (rsiValue > 70) and (chopIndex < 50) and (ta.crossunder(k, d))

var float longStopLevel = na
var float longTakeProfitLevel = na
var float shortStopLevel = na
var float shortTakeProfitLevel = na

// Wejście w pozycję długą
if (buyCondition and na(longStopLevel))
    strategy.entry("Long", strategy.long)
    longStopLevel := na // Zresetuj poziom Stop Loss
    longTakeProfitLevel := na // Zresetuj poziom Take Profit

// Wejście w pozycję krótką
if (sellCondition and na(shortStopLevel))
    strategy.entry("Short", strategy.short)
    shortStopLevel := na // Zresetuj poziom Stop Loss
    shortTakeProfitLevel := na // Zresetuj poziom Take Profit

// Ustaw poziomy Take Profit i Stop Loss na podstawie ceny wejścia w pozycję
if (strategy.position_size > 0 and na(longTakeProfitLevel))
    longStopLevel := strategy.position_avg_price * (1 - longStopLossPct)
    longTakeProfitLevel := strategy.position_avg_price * (1 + longTakeProfitPct)

if (strategy.position_size < 0 and na(shortTakeProfitLevel))
    shortStopLevel := strategy.position_avg_price * (1 + shortStopLossPct)
    shortTakeProfitLevel := strategy.position_avg_price * (1 - shortTakeProfitPct)

// Resetowanie poziomów po wyjściu z pozycji
if (strategy.position_size == 0)
    longStopLevel := na
    longTakeProfitLevel := na
    shortStopLevel := na
    shortTakeProfitLevel := na

// Wyjście z pozycji długiej
if (strategy.position_size > 0)
    strategy.exit("Take Profit", "Long", limit=longTakeProfitLevel, stop=longStopLevel)

// Wyjście z pozycji krótkiej
if (strategy.position_size < 0)
    strategy.exit("Take Profit", "Short", limit=shortTakeProfitLevel, stop=shortStopLevel)

// Oznaczenie poziomów stop loss i take profit na wykresie
plot(series=longStopLevel, title="Long Stop Loss", color=color.red, linewidth=1, style=plot.style_circles)
plot(series=longTakeProfitLevel, title="Long Take Profit", color=color.green, linewidth=1, style=plot.style_circles)
plot(series=shortStopLevel, title="Short Stop Loss", color=color.red, linewidth=1, style=plot.style_circles)
plot(series=shortTakeProfitLevel, title="Short Take Profit", color=color.green, linewidth=1, style=plot.style_circles)

// Wyświetlanie wskaźników na wykresie
plot(rsiValue, title="RSI", color=color.blue, linewidth=2)
hline(30, "RSI 30", color=color.red)
hline(70, "RSI 70", color=color.red)

plot(chopIndex, title="Choppiness Index", color=color.purple, linewidth=2)
hline(50, "CHOP 50", color=color.red)

plot(k, title="Stochastic K", color=color.green, linewidth=2)
plot(d, title="Stochastic D", color=color.red, linewidth=2)
hline(20, "Stoch 20", color=color.red)
hline(80, "Stoch 80", color=color.red)

// Wyświetlanie SMA na wykresie
plot(smaValue, title="SMA", color=color.orange, linewidth=2)

```

> Detail

https://www.fmz.com/strategy/478721

> Last Modified

2025-01-17 15:55:00
