
> Name

Multi-Indicator-Trend-Momentum-Trading-Strategy-A-Comprehensive-Quantitative-Trading-System-Based-on-Bollinger-Bands-RSI-and-OBV

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/16042be4412500efaf6.png)


#### Overview
This strategy is a trend-following and momentum trading system based on multiple technical indicators. It combines Bollinger Bands (BB), Relative Strength Index (RSI), and On-Balance Volume (OBV) to identify market trends and trading opportunities by analyzing price movements, momentum, and trading volume. The strategy adopts a medium to long-term holding approach, entering long positions when the market shows a clear upward trend with strong momentum and exiting when the price breaks below the lower Bollinger Band.

#### Strategy Principles
The core logic of the strategy is based on three aspects:
1. Using Bollinger Bands (BB) to determine price trends - When price is above the middle band, it confirms an upward trend. BB parameters are set to 20-day moving average and 2 standard deviations.
2. Using Relative Strength Index (RSI) to confirm price momentum - RSI above 50 indicates upward momentum. RSI parameter is set to 14 days.
3. Using On-Balance Volume (OBV) to verify volume support - Rising 10-day exponential moving average of OBV shows volume confirms price increases.

Entry signals require simultaneous satisfaction of: price above BB middle band, RSI above 50, and upward OBV trend.
Exit signal is: price breaking below the lower BB band.

#### Strategy Advantages
1. Multiple technical indicators cross-validation improves signal reliability
2. Combines price, momentum, and volume analysis
3. Trend-following approach captures major market moves
4. Clear exit conditions effectively control drawdown risk
5. Reasonable indicator parameters avoid over-optimization

#### Strategy Risks
1. Potential losses from frequent trading in choppy markets
2. Significant drawdowns possible during trend reversals
3. Slippage losses in sharp decline scenarios
4. Volume indicators may be ineffective in certain markets
5. Fixed parameters may not adapt to all market conditions

#### Strategy Optimization Directions
1. Add market environment classification for different parameter sets
2. Implement stop-loss mechanisms to control single trade risk
3. Optimize exit mechanism to lock in partial profits
4. Add volume filters to avoid false breakouts
5. Incorporate volatility adaptation for dynamic parameter adjustment

#### Summary
This strategy is a robust trend-following system that effectively captures market trends through the coordinated use of multiple technical indicators. The strategy logic is clear, with reasonable parameter settings and good practicality. Through the suggested optimization directions, the strategy's stability and profitability can be further improved. When applying to live trading, it is recommended to make appropriate adjustments based on specific market characteristics and capital scale.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-18 00:00:00
end: 2025-02-17 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © ahmetkaratas4238

//@version=5
strategy("İstanbul Stratejisi", overlay=true)

// Bollinger Bantları Hesaplamaları
bbLength = 20
bbMult = 2.0
basis = ta.sma(close, bbLength)
dev = bbMult * ta.stdev(close, bbLength)
upperBand = basis + dev
lowerBand = basis - dev

// RSI Hesaplamaları
rsiLength = 14
rsi = ta.rsi(close, rsiLength)
rsiThreshold = 50

// OBV Hesaplaması
obv = ta.cum(volume * math.sign(ta.change(close)))  // ta.cum yerine ta.cumulative kullanılmalı
obvTrend = ta.ema(obv, 10) > ta.ema(obv[1], 10)  // OBV'nin yükseliş trendinde olup olmadığını kontrol eder

// ALIM ŞARTLARI
buyCondition = close > basis and rsi > rsiThreshold and obvTrend

// SATIM ŞARTI
sellCondition = close < lowerBand

// Alım İşlemi Aç
if buyCondition
    strategy.entry("Long", strategy.long)

// Satım İşlemi Yap (Pozisyon Kapat)
if sellCondition
    strategy.close("Long")

// Bollinger Bantlarını Göster
plot(upperBand, title="Üst Bollinger Bandı", color=color.red)
plot(lowerBand, title="Alt Bollinger Bandı", color=color.green)
plot(basis, title="Orta Bollinger Bandı", color=color.blue)

// Alım ve Satım Sinyallerini İşaretle
plotshape(series=buyCondition, location=location.belowbar, color=color.green, style=shape.labelup, title="Alım Sinyali")
plotshape(series=sellCondition, location=location.abovebar, color=color.red, style=shape.labeldown, title="Satım Sinyali")


```

> Detail

https://www.fmz.com/strategy/482464

> Last Modified

2025-02-18 15:24:56
