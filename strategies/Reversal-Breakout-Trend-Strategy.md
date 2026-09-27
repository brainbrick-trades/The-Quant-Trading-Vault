
> Name

Reversal-Breakout-Trend-Strategy

> Author

ChaoZhang

> Strategy Description




## Overview

The reversal trend breakout strategy is a combination strategy that combines the advantages of reversal strategies and breakout strategies and aims to issue trading signals at trend reversal points. This strategy first determines whether the price has a reversal pattern for two consecutive days, and whether the indicator Stochastic Oscillator sends a reversal signal. If so, it will generate a buy or sell signal. At the same time, this strategy will also determine whether the price breaks through the highest price or lowest price within the specified period. If the reversal and breakthrough conditions are met at the same time, a trading signal will be generated.

## Strategy Principle

This strategy consists of two parts:

1. Reverse part

Determine if the price reverses for two consecutive days (the closing price on the second day is higher than the first day, buy when the Stochastic fast line is lower than the slow line; sell when the closing price on the second day is lower than the first day, and the fast line is higher than the slow line)).

2. Breakthrough part 

Determine whether the price breaks the highest price within the look_back period (if it breaks the highest price, buy).).

When the signals of the reversal part and the breakthrough part are in the same direction (for example, the reversal shows a buy signal and the breakthrough also shows a buy signal), an actual buy or sell signal is generated.

## Strategy Advantages

This combined strategy merges the advantages of reversal and trend breakout strategies, allowing more accurate signal capture at trend turning points.

1. The reversal part can issue signals when the price reverses, suitable for capturing turning points.

2. The breakout section ensures the direction of trading signals aligns with the trend, avoiding the wrong direction of trading.

3. When both parts issue signals in the same direction, it can generate more reliable trading opportunities.

4. StochasticThe application of indicators avoids the subjectivity of judging based solely on price patterns.

## Risks and Optimization

This strategy also carries some risks to be aware of:

1. Reversal signals may be false breakouts; the reversal trend cannot be confirmed. may optimize it by:

2. Breakthrough signals may be illusionary; it is impossible to determine that the trend has started.

3. Improper setting of the two parts of indicator parameters may lead to missed trading opportunities.

4. The transaction frequency may be too high. Parameters can be adjusted appropriately to control the number of transactions.

Corresponding optimization measures:

1. Optimize reversal indicator parameters to ensure reversal signals are more reliable.

2. Optimized breakout parameters to avoid illusionary breakthroughs.

3. Adjust the parameter settings of the reversal and breakthrough parts to find the best match.

4. Appropriately adjust the transaction frequency to prevent too frequent transactions.

## Summary

The reversal trend breakout strategy comprehensively uses the advantages of reversal and trend breakout strategies to reliably send trading signals at price turning points. Through parameter optimization, you can control the trading frequency while improving signal quality and capturing reliable trading opportunities. This strategy is relatively stable overall, but attention needs to be paid to preventing risks caused by false breakthroughs and illusory breakthroughs.




## Overview

The Reversal Breakout Trend strategy is a combo strategy that combines the advantages of reversal and breakout strategies to generate trading signals at trend reversal points. It first judges if prices reverse during two consecutive days and if the Stochastic Oscillator gives reversal signals. At the same time, it also checks if prices break through the highest/lowest prices over a certain period. When reversal and breakout conditions are met, trading signals are generated.

## Strategy Logic 

The strategy consists of two parts:

1. Reversal Part

It judges if prices reverse during two consecutive days (buy when close of day 2 is higher than day 1 and Stochastic fast line is lower than slow line; sell when close of day 2 is lower than day 1 and fast line is higher than slow line).

2. Breakout Part

It judges if prices break through the highest price over the look_bak period (buy if price breaks through the highest price).

When reversal and breakout parts give signals in the same direction (e.g. reversal shows buy and breakout shows buy), actual buy/sell signals are generated.

## Advantages

This combo strategy combines the pros of reversal and trend breakout strategies and can more accurately capture signals at trend turning points:

1. The reversal part can generate signals when prices reverse, suitable to catch turning points.

2. The breakout part ensures trade direction is aligned with the trend, avoiding trading in wrong direction.

3. Signals in the same direction from both parts create more reliable trading opportunities. 

4. The application of Stochastic avoids the subjectivity of judging by price pattern alone.

## Risks and Optimization

There are also some risks to note:

1. Reversal signals may be false breakouts, unable to confirm the reversal trend has established.

2. Breakout signals may be false breakouts, unable to judge the trend has started. 

3. Improper parameter settings of the two parts may lead to missing trades.

4. High trading frequency may occur and needs to be controlled.

Possible optimizations:

1. Optimize parameters of reversal indicators to ensure reversal signals are more reliable.

2. Optimize breakout parameters to avoid false breakouts.  

3. Adjust parameters of both parts to find the optimal match.

4. Moderate the trading frequency to prevent over-trading.

## Summary 

The Reversal Breakout Trend strategy leverages the strengths of reversal and trend breakout strategies and reliably generates trading signals at turning points. Through parameter optimization, it can improve signal quality and capture solid trading opportunities while controlling trading frequency. Overall this strategy is robust but false breakouts remain a risk to watch out for. Proper optimization and parameter tuning is key.



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|Length|
|v_input_2|true|KSmoothing|
|v_input_3|3|DLength|
|v_input_4|50|Level|
|v_input_5|4|Look Bak|
|v_input_6|false|Trade reverse|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-09-29 00:00:00
end: 2023-10-06 00:00:00
period: 45m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 26/06/2019
// This is combo strategies for get a cumulative signal. 
//
// First strategy
// This System was created from the Book "How I Tripled My Money In The 
// Futures Market" by Ulf Jensen, Page 183. This is reverse type of strategies.
// The strategy buys at market, if close price is higher than the previous close 
// during 2 days and the meaning of 9-days Stochastic Slow Oscillator is lower than 50. 
// The strategy sells at market, if close price is lower than the previous close price 
// during 2 days and the meaning of 9-days Stochastic Fast Oscillator is higher than 50.
//
// Second strategy
//    Breakout Range Long Strategy
//
// WARNING:
// - For purpose educate only
// - This script to change bars colors.
////////////////////////////////////////////////////////////
Reversal123(Length, KSmoothing, DLength, Level) =>
    vFast = sma(stoch(close, high, low, Length), KSmoothing) 
    vSlow = sma(vFast, DLength)
    pos = 0.0
    pos := iff(close[2] < close[1] and close > close[1] and vFast < vSlow and vFast > Level, 1,
	         iff(close[2] > close[1] and close < close[1] and vFast > vSlow and vFast < Level, -1, nz(pos[1], 0))) 
	pos

BreakoutRangeLong(look_bak) =>
    pos = 0
    xHighest = highest(high, look_bak)
    pos := iff(high > xHighest[1], 1, 0) 
    pos

strategy(title="Combo Backtest 123 Reversal & Breakout Range Long", shorttitle="Combo", overlay = true)
Length = input(14, minval=1)
KSmoothing = input(1, minval=1)
DLength = input(3, minval=1)
Level = input(50, minval=1)
//-------------------------
look_bak = input(4, minval=1, title="Look Bak")
reverse = input(false, title="Trade reverse")
posReversal123 = Reversal123(Length, KSmoothing, DLength, Level)
posBreakoutRangeLong = BreakoutRangeLong(look_bak)
pos = iff(posReversal123 == 1 and posBreakoutRangeLong == 1 , 1,
	   iff(posReversal123 == -1 and posBreakoutRangeLong == -1, -1, 0)) 
possig = iff(reverse and pos == 1, -1,
          iff(reverse and pos == -1, 1, pos))	   
if (possig == 1) 
    strategy.entry("Long", strategy.long)
if (possig == -1)
    strategy.entry("Short", strategy.short)	 
if (possig == 0) 
    strategy.close_all()
barcolor(possig == -1 ? red: possig == 1 ? green : blue )
```

> Detail

https://www.fmz.com/strategy/428626

> Last Modified

2023-10-07 16:15:43
