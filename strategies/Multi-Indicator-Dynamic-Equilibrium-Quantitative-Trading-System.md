
> Name

Multi-Indicator-Dynamic-Equilibrium-Quantitative-Trading-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1b1ca2a30c61ffa51bf.png)


#### Overview
This strategy is a dynamic equilibrium trading system based on multiple technical indicators. It integrates various technical analysis tools including Relative Strength Index (RSI), Bollinger Bands (BB), Exponential Moving Average (EMA), and Moving Average Convergence Divergence (MACD) to identify market opportunities through cross-validation between indicators. The strategy employs percentage-based position management, defaulting to 10% of total assets per trade, which helps control risk.

#### Strategy Principles
The core logic of the strategy is to enhance trading signal reliability through multiple indicator confirmation. Specifically:
1. Uses 14-period RSI to monitor market overbought/oversold conditions
2. Employs 20-period, 2-standard deviation Bollinger Bands to determine price volatility ranges
3. Utilizes 50 and 200-period EMAs to judge medium and long-term trends
4. Adopts MACD(12,26,9) parameter combination to capture trend reversal points

Buy signals require at least two of the following conditions:
- RSI below 30 (oversold zone)
- Price touching lower Bollinger Band
- Fast EMA crossing above slow EMA
- MACD line crossing above signal line

Sell signals trigger when either:
- RSI above 70 (overbought zone)
- Price breaking above upper Bollinger Band

#### Strategy Advantages
1. Multiple indicator cross-validation improves signal reliability
2. Percentage-based position management effectively controls risk
3. Combines benefits of trend following and range trading
4. Flexible signal conditions with strong adaptability
5. Graphical interface provides intuitive signal display

#### Strategy Risks
1. Multiple indicators may lead to signal lag
2. May generate excessive false signals in ranging markets
3. Fixed parameters may not adapt to changing market conditions
4. Lack of volume consideration might affect judgment accuracy
5. Relatively simple money management approach may impact returns

#### Strategy Optimization Directions
1. Incorporate volume indicators as auxiliary confirmation
2. Develop adaptive parameter adjustment mechanisms
3. Refine money management strategy
4. Add stop-loss and trailing stop mechanisms
5. Include market environment recognition module
6. Optimize signal filtering mechanism

#### Summary
This strategy constructs a relatively complete trading system through the combined application of multiple technical indicators. Cross-validation between indicators enhances trading signal reliability. While adopting conservative position management to control risk, there are aspects requiring optimization, but the overall framework design is reasonable and has practical application value.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-19 00:00:00
end: 2025-02-16 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("ETH/USDT Multi-Indicator Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=250)

// Parametri za RSI
rsiPeriod = 14
rsiOversold = 30
rsiOverbought = 70

// Parametri za Bollinger Bands
bbLength = 20
bbStdDev = 2

// Parametri za EMA
emaShort = 50
emaLong = 200

// Parametri za MACD
[macdLine, signalLine, _] = ta.macd(close, 12, 26, 9)

// RSI izračun
rsi = ta.rsi(close, rsiPeriod)

// Bollinger Bands izračun
basis = ta.sma(close, bbLength)
upperBand = basis + bbStdDev * ta.stdev(close, bbLength)
lowerBand = basis - bbStdDev * ta.stdev(close, bbLength)

// EMA izračun
emaFast = ta.ema(close, emaShort)
emaSlow = ta.ema(close, emaLong)

// Pravilo 1: RSI prelazi iznad 30 nakon preprodatosti
rsiSignal = rsi < rsiOversold

// Pravilo 2: Cena dotakne donju Bollinger traku
bbSignal = close < lowerBand

// Pravilo 3: EMA crossover (zlatni krst)
emaSignal = emaFast > emaSlow

// Pravilo 4: MACD prelazak iznad signalne linije
macdSignal = macdLine > signalLine

// Kombinovani signal za kupovinu (bar dva uslova ispunjena)
buySignal = (rsiSignal and bbSignal) or (emaSignal and macdSignal)

// Pravilo za prodaju (RSI prekupljen ili cena iznad gornje Bollinger trake)
sellSignal = rsi > rsiOverbought or close > upperBand

// Vizualizacija signala
plotshape(series=buySignal, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
plotshape(series=sellSignal, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

// Strategija: Otvaranje i zatvaranje pozicija
if (buySignal)
    strategy.entry("Buy", strategy.long)

if (sellSignal)
    strategy.close("Buy")

// Bollinger Bands vizualizacija
plot(upperBand, color=color.new(color.blue, 50), title="Upper Band")
plot(lowerBand, color=color.new(color.blue, 50), title="Lower Band")
plot(basis, color=color.blue, title="Basis")

// EMA vizualizacija
plot(emaFast, color=color.orange, title="EMA Short")
plot(emaSlow, color=color.red, title="EMA Long")

```

> Detail

https://www.fmz.com/strategy/482441

> Last Modified

2025-02-18 14:44:29
