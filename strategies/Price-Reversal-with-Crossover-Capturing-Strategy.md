
> Name

Price-Reversal-with-Crossover-Capturing-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/e988de74745ff4ad39.png)
 
## Overview  
The price reversal with crossover capturing strategy is a compound strategy that combines price reversal trading techniques and indicator crossovers. It first generates trading signals using price reversal patterns, then filters the signals with overbought/oversold crossovers of a stochastic oscillator, in order to capture short-term reversals in the market.


## Strategy Logic  
The strategy consists of two sub-strategies:

1. 123 Reversal Strategy
  - When the close price turns from higher to lower in two days, and the 9-day stochastic indicator is at lower band (below a threshold), a buy signal is generated  
  - When the close price turns from lower to higher in two days, and the 9-day stochastic indicator is at upper band (above a threshold), a sell signal is generated

2. Stochastic Crossover Strategy 
  - When the %K line crosses below the %D line, while both lines are in overbought levels, a sell signal is generated
  - When the %K line crosses above the %D line, while both lines are in oversold levels, a buy signal is generated
  
The compound strategy checks the signals from both sub-strategies and only triggers actual trades when the signals align in the same direction.  


## Advantages
The strategy combines price reversal patterns and indicator crossovers to evaluate both price action and indicator information, which helps filter out false signals and uncover reversal opportunities to improve profitability.  

Specific advantages include:

1. Capturing market reversals quickly without long consolidation waits 
2. Increased signal accuracy with dual validation from both sub-strategies
3. Better win rate combining analysis of both price action and indicators

## Risks
There are also some risks with this strategy:   

1. Price may reverse abruptly during high volatility, causing incorrect signals  
2. Poor indicator parameter tuning affects signal quality
3. Unsure about reversal timing, some time risk exists  

These risks can be managed by adjusting parameters, using stop losses etc.

## Enhancement Opportunities
Some ways the strategy can be enhanced:

1. Optimize indicator parameters  
2. Add other filters like volume  
3. Customize parameters based on symbol and market conditions  
4. Incorporate stop loss for risk control
5. Employ machine learning for signal identification

## Conclusion
The price reversal with crossover capturing strategy combines multiple complementary strategies to profit while controlling risks. With continuous improvements, it can be tailored into an efficient strategy that thrives in changing markets.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|---- 123 Reversal ----|
|v_input_2|14|Length|
|v_input_3|true|KSmoothing|
|v_input_4|3|DLength|
|v_input_5|50|Level|
|v_input_6|true|---- Stochastic Crossover ----|
|v_input_7|7|LengthSC|
|v_input_8|3|DLengthSC|
|v_input_9|20|Oversold|
|v_input_10|70|Overbought|
|v_input_11|false|Trade reverse|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-09 00:00:00
end: 2024-01-16 00:00:00
period: 10m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 15/09/2021
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
// This back testing strategy generates a long trade at the Open of the following 
// bar when the %K line crosses below the %D line and both are above the Overbought level.
// It generates a short trade at the Open of the following bar when the %K line 
// crosses above the %D line and both values are below the Oversold level.
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


StochCross(Length, DLength,Oversold,Overbought) =>
    pos = 0.0
    vFast = stoch(close, high, low, Length)
    vSlow = sma(vFast, DLength)
    pos := iff(vFast < vSlow and vFast > Overbought and vSlow > Overbought, 1,
    	      iff(vFast >= vSlow and vFast < Oversold and vSlow < Oversold, -1, nz(pos[1], 0))) 
    pos

strategy(title="Combo Backtest 123 Reversal & Stochastic Crossover", shorttitle="Combo", overlay = true)
line1 = input(true, "---- 123 Reversal ----")
Length = input(14, minval=1)
KSmoothing = input(1, minval=1)
DLength = input(3, minval=1)
Level = input(50, minval=1)
//-------------------------
line2 = input(true, "---- Stochastic Crossover ----")
LengthSC = input(7, minval=1)
DLengthSC = input(3, minval=1)
Oversold = input(20, minval=1)
Overbought = input(70, minval=1)
reverse = input(false, title="Trade reverse")
posReversal123 = Reversal123(Length, KSmoothing, DLength, Level)
posmStochCross = StochCross(LengthSC, DLengthSC,Oversold,Overbought)
pos = iff(posReversal123 == 1 and posmStochCross == 1 , 1,
	   iff(posReversal123 == -1 and posmStochCross == -1, -1, 0)) 
possig = iff(reverse and pos == 1, -1,
          iff(reverse and pos == -1 , 1, pos))	   
if (possig == 1 ) 
    strategy.entry("Long", strategy.long)
if (possig == -1 )
    strategy.entry("Short", strategy.short)	 
if (possig == 0) 
    strategy.close_all()
barcolor(possig == -1 ? #b50404: possig == 1 ? #079605 : #0536b3 )
```

> Detail

https://www.fmz.com/strategy/439087

> Last Modified

2024-01-17 16:29:13
