
> Name

Cloud-Based-Dual-Moving-Average-Momentum-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/4e04c1951864906e22.png)


#### Overview
This strategy is a momentum trading system based on cloud breakouts and dual moving average crossovers. It combines multiple components of the Ichimoku Cloud indicator to identify market trend direction and momentum changes, generating trading signals through price position relative to the cloud and crossovers between the conversion and base lines. The core concept is to capture momentum opportunities in strong trends.

#### Strategy Principle
The strategy utilizes the following key components:
1. Conversion Line (Tenkan-Sen): Calculates the midpoint of the highest high and lowest low over 9 periods, reflecting short-term market trends
2. Base Line (Kijun-Sen): Calculates the midpoint of the highest high and lowest low over 26 periods, reflecting medium-term market trends
3. Leading Span A (Senkou Span A): Average of conversion and base lines, displaced 26 periods forward
4. Leading Span B (Senkou Span B): Midpoint of the highest high and lowest low over 52 periods, displaced 26 periods forward
5. Lagging Span (Chikou Span): Current closing price displaced 26 periods backward

Entry conditions:
- Long: Price above the cloud (higher than both Spans A and B) and conversion line crosses above base line
- Short: Price below the cloud (lower than both Spans A and B) and conversion line crosses below base line

Exit conditions: Positions are closed when opposite trading signals appear

#### Strategy Advantages
1. Multiple timeframe analysis: Provides comprehensive market perspective through indicator combinations across different periods
2. Trend confirmation: Uses cloud position as trend filter to reduce false breakout risks
3. Momentum identification: Captures momentum changes through moving average crossovers for better entry timing
4. Adaptability: Indicator parameters automatically adjust to market volatility, adapting to different market environments
5. Visual intuition: Cloud visualization makes trend direction and strength immediately apparent

#### Strategy Risks
1. Choppy market risk: May generate frequent false signals during consolidation phases
2. Lag risk: May miss some rapid market opportunities due to longer-period moving averages
3. Parameter sensitivity: Different parameter settings significantly affect strategy performance
4. Trend reversal risk: May experience larger drawdowns during sudden trend reversals

Risk control suggestions:
- Cross-validate with other technical indicators
- Set appropriate stop-loss levels
- Dynamically adjust parameters for different market cycles
- Implement position management strategies

#### Strategy Optimization Directions
1. Parameter optimization:
- Conduct parameter sensitivity analysis for different market environments
- Introduce adaptive parameter adjustment mechanisms

2. Signal filtering:
- Add volume confirmation mechanisms
- Incorporate volatility filters
- Integrate market structure analysis

3. Risk management:
- Develop dynamic stop-loss mechanisms
- Implement volatility-based position sizing
- Add drawdown control modules

#### Summary
This is a comprehensive strategy system combining trend following and momentum trading. Through the coordinated use of cloud breakouts and moving average crossovers, it effectively captures market trend opportunities while maintaining strategy stability. Successful implementation requires careful attention to parameter optimization, risk control, and market adaptability.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-08 00:00:00
end: 2025-02-06 08:00:00
period: 2d
basePeriod: 2d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Ichimoku Cloud Strategy", shorttitle="IchimokuStrat", overlay=true)

//=== Užívateľské vstupy ===//
tenkanLen          = input.int(9,   "Tenkan-Sen Length")
kijunLen           = input.int(26,  "Kijun-Sen Length")
senkouSpanBLen     = input.int(52,  "Senkou Span B Length")
displacement       = input.int(26,  "Cloud Displacement")

//=== Výpočet Ichimoku liniek ===//

// Tenkan-Sen (Conversion Line)
tenkanHigh = ta.highest(high, tenkanLen)
tenkanLow  = ta.lowest(low, tenkanLen)
tenkan     = (tenkanHigh + tenkanLow) / 2.0

// Kijun-Sen (Base Line)
kijunHigh = ta.highest(high, kijunLen)
kijunLow  = ta.lowest(low, kijunLen)
kijun     = (kijunHigh + kijunLow) / 2.0

// Senkou Span A = (Tenkan + Kijun)/2, posunutý dopredu
spanA = (tenkan + kijun) / 2.0

// Senkou Span B = (highest high + lowest low)/2, posunutý dopredu
spanBHigh = ta.highest(high, senkouSpanBLen)
spanBLow  = ta.lowest(low, senkouSpanBLen)
spanB     = (spanBHigh + spanBLow) / 2.0

// Chikou Span (voliteľný) = current close, posunutý dozadu
chikou = close[displacement]

//=== Podmienky pre LONG / SHORT ===//
// Cena NAD oblakom => close > spanA a close > spanB
// Tenkan NAD Kijun => tenkan > kijun
longCondition = (close > spanA and close > spanB) and (tenkan > kijun)

// Cena POD oblakom => close < spanA a close < spanB
// Tenkan POD Kijun => tenkan < kijun
shortCondition = (close < spanA and close < spanB) and (tenkan < kijun)

//=== Vstup do pozícií ===//
if longCondition
    strategy.entry("Long", strategy.long)
if shortCondition
    strategy.entry("Short", strategy.short)

//=== Výstup pri opačnom signáli ===//
if strategy.position_size > 0 and shortCondition
    strategy.close("Long", comment="Exit Long")
if strategy.position_size < 0 and longCondition
    strategy.close("Short", comment="Exit Short")

//=== Vykreslenie Ichimoku = vyplnený oblak ===//

// Najskôr si ulož premenne (plot) pre spanA, spanB
plotA = plot(spanA, title="Span A", offset=displacement, color=color.new(color.green, 0))
plotB = plot(spanB, title="Span B", offset=displacement, color=color.new(color.red, 0))

// Namiesto plotfill() použijeme fill()
fill(plotA, plotB, title="Cloud Fill", color=color.new(color.green, 80))

```

> Detail

https://www.fmz.com/strategy/481103

> Last Modified

2025-02-08 15:10:06
