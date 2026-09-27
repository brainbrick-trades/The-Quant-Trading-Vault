
> Name

Adaptive-Multi-Period-Trading-Strategy-Based-on-Wave-Trend-Momentum-Breakout

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/e6294d749a16565795.png)


#### Overview
This strategy is a momentum trading system based on the WaveTrend indicator, which identifies market overbought and oversold conditions by calculating price momentum changes and generates trading signals at key price level breakouts. The strategy employs double-smoothed momentum curves (WT1 and WT2) to filter market noise and enhance signal reliability.

#### Strategy Principle
The core of the strategy builds the WaveTrend indicator through the following steps:
1. Uses HLC3 price as benchmark, calculating n1-period EMA as price center
2. Calculates price deviation from center, using 0.015 as normalization factor
3. Smooths deviation with n2-period EMA to get main trend line WT1
4. Smooths WT1 with 4-period SMA to get signal line WT2
5. Sets trading triggers at overbought (60) and oversold (-60) levels
Long signals are generated when WT1 crosses above WT2 in oversold territory; short signals when WT1 crosses below WT2 in overbought territory.

#### Strategy Advantages
1. Robust signal generation mechanism, significantly reducing false signals through double smoothing and overbought/oversold filtering
2. Strong parameter adaptability, allowing traders to adjust channel length and moving average periods for different market characteristics
3. Combines advantages of trend following and momentum reversal, capturing both major trends and reversal trades at extreme positions
4. Excellent visualization, enabling traders to intuitively understand market conditions and potential trading opportunities

#### Strategy Risks
1. May generate frequent trading signals in ranging markets, increasing transaction costs
2. Fixed overbought/oversold thresholds may not suit all market environments
3. Double smoothing process may lead to signal lag, missing optimal entry points in fast markets
4. Requires proper stop-loss settings for risk control, as strategy lacks integrated risk management mechanism

#### Strategy Optimization Directions
1. Introduce adaptive overbought/oversold thresholds, dynamically adjusting based on market volatility
2. Add volume confirmation mechanism to improve signal reliability
3. Integrate trend strength filter to reduce reversal trades during strong trends
4. Add time filter to avoid trading during low volatility periods
5. Develop complete position management system, dynamically adjusting position size based on signal strength

#### Summary
This is a well-designed trend momentum trading strategy that effectively captures market reversal opportunities through the WaveTrend indicator. The strategy's core strengths lie in its robust signal generation mechanism and good adaptability. Through the suggested optimization directions, the strategy's stability and profitability can be further enhanced. For investors seeking medium to long-term trading opportunities, this is a trading system worth considering.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-19 00:00:00
end: 2025-02-16 08:00:00
period: 2h
basePeriod: 2h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy(title="WaveTrend [LazyBear] Strategy", shorttitle="WT_LB_Strategy", overlay=true)

// Pôvodné vstupné parametre
n1       = input.int(10,  title="Channel Length")
n2       = input.int(21,  title="Average Length")
obLevel1 = input.int(60,  title="Over Bought Level 1")
obLevel2 = input.int(53,  title="Over Bought Level 2")
osLevel1 = input.int(-60, title="Over Sold Level 1")
osLevel2 = input.int(-53, title="Over Sold Level 2")

// Výpočet WaveTrendu
ap   = hlc3
esa  = ta.ema(ap, n1)
d    = ta.ema(math.abs(ap - esa), n1)
ci   = (ap - esa) / (0.015 * d)
tci  = ta.ema(ci, n2)

// Vyhladené krivky
wt1  = tci
wt2  = ta.sma(wt1, 4)

// Plotovanie nulovej línie a OB/OS úrevní
plot(0,         color=color.gray, linewidth=1)
plot(obLevel1,  color=color.red)
plot(osLevel1,  color=color.green)
plot(obLevel2,  color=color.red)
plot(osLevel2,  color=color.green)

// Plot WaveTrendu
plot(wt1, color=color.green, title="WT1")
plot(wt2, color=color.red,   title="WT2")
plot(wt1 - wt2, color=color.blue, style=plot.style_area, title="WT Fill")

//------------------------------------------------------
// STRATEGY LOGIC (ukážková)
//------------------------------------------------------
if ta.crossover(wt1, wt2) and wt1 <= osLevel1
    strategy.close("Short")
    strategy.entry("Long", strategy.long)

if ta.crossunder(wt1, wt2) and wt1 >= obLevel1
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

```

> Detail

https://www.fmz.com/strategy/482427

> Last Modified

2025-02-18 13:52:37
