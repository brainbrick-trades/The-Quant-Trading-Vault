
> Name

WMX-Williams-Fractals-Reversal-Pivot-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/16a61b1fbe58739b0e1.png)
 
## Overview  

This strategy adopts the Williams indicator fractal breakout principle and combines specific K-line patterns to design an efficient long and short opening and closing model. It can accurately go long and short at the key reversal points of market movements to capture medium and short term trends and obtain excess returns.

## Strategy Principle

This strategy uses the fractal points in the Williams indicator to determine reversal signals. When a top or bottom fractal appears and it is consistent with the K-line entity direction, a trading signal is generated.   

Specifically, a custom indicator called WMX Williams Fractals is defined in the strategy. It uses factor functions to determine the top fractal (upFractal) and bottom fractal (dnFractal).  

The top fractal logic is: the highest price of the current K-line is higher than the highest price of the previous n K-lines (n is an adjustable parameter), thus forming a top side breakout fractal.

The bottom fractal logic is: the lowest price of the current K-line is lower than the lowest price of the previous n K-lines, thus forming an bottom side breakout fractal.   

After getting the top and bottom fractals, determine whether they change, that is, from none to exist or vice versa. At this time, the fractal has just formed, indicating a greater possibility of reversal.

Then, combined with the K-line entity direction to determine specific trading signals. When the top fractal is formed and Close is higher than Open, go long. When the bottom fractal is formed and Close is lower than Open, go short.

## Strategy Advantages  

1. Use the Williams indicator fractal points to determine the reversal timing. It is a mature and reliable technical indicator.  

2. Combine the K-line entity direction to confirm trading signals and avoid choppy non-trend regions.   

3. Few parameters that only need to adjust the fractal period n, easy to test and optimize.  

4. Flexible settings for opening positions rules like position sizing, closing conditions, etc., easy to apply in live trading.

## Strategy Risks  

1. After the fractal forms, the market may not completely reverse, need to combine with trend judgment.  

2. Stop loss position setting needs to be cautious to prevent being knocked out by noisy huge volatility moves.

3. The n parameter needs to adjust for different products. If the period is too large or too small it will affect the results.  

Solutions:  

1. Can add indicators like moving average to judge major trend, avoid trading against trends.  

2. Use dynamic trailing stop loss or set reasonable drawdown based stop loss.  

3. Utilize Walk Forward Analysis to optimize parameters and find the optimal values.   

## Strategy Optimization Directions   

1. Fractal reversal strategies tend to form multiple profits then reverse again to form losses. Can consider adding trend filters to further limit trading range and reduce unnecessary reversal trades.   

2. Current simple stop loss method cannot effectively track market moves. Can try more advanced stop loss techniques like moving stop loss, time based stop loss, dynamic stop loss etc.   

3. Currently only use K-line entity direction. If considering more K-line information like wicks and close location, can design even more precise trade signals.  

## Conclusion  

This is a reversal strategy based on technical indicators. It utilizes the Williams indicator fractals to capture changes in the trend of the underlying at key pivot points, combined with K-line entity direction to form trade signals, aiming to achieve excess returns.   

Compared to other reversal strategies, this strategy features parameterized design for clear logic and easy understanding. It has flexible parameter adjustments for convenient testing, and can directly be applied in live trading. Next step further optimizations on trend filtering, stop loss methods etc. can improve strategy performance.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|2|Periods|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-14 00:00:00
end: 2023-12-14 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © WMX_Q_System_Trading

//@version=4
SystemName="WMX Williams Fractals strategy V4"
InitCapital = 1000000
InitPosition = 100
InitCommission = 0.075
InitPyramidMax = 10
strategy(title=SystemName, shorttitle=SystemName, overlay=true, initial_capital=InitCapital, default_qty_type=strategy.percent_of_equity, default_qty_value=InitPosition, commission_type=strategy.commission.percent, commission_value=InitCommission)


//study("WMX Williams Fractals", shorttitle="WMX Fractals", format=format.price, precision=0, overlay=true)
// Define "n" as the number of periods and keep a minimum value of 2 for error handling.
n = input(title="Periods", defval=2, minval=2, type=input.integer)
h=close
l=close

factorh(High)=>
    upFractal = (                                                                                                          (High[n+2]  < High[n]) and (High[n+1]  < High[n]) and (High[n-1] < High[n]) and (High[n-2] < High[n]))
             or (                                                                               (High[n+3]  < High[n]) and (High[n+2]  < High[n]) and (High[n+1] == High[n]) and (High[n-1] < High[n]) and (High[n-2] < High[n]))
             or (                                                    (High[n+4]  < High[n]) and (High[n+3]  < High[n]) and (High[n+2] == High[n]) and (High[n+1] <= High[n]) and (High[n-1] < High[n]) and (High[n-2] < High[n]))
             or (                          (High[n+5] < High[n]) and (High[n+4]  < High[n]) and (High[n+3] == High[n]) and (High[n+2] == High[n]) and (High[n+1] <= High[n]) and (High[n-1] < High[n]) and (High[n-2] < High[n]))
             or ((High[n+6] < High[n]) and (High[n+5] < High[n]) and (High[n+4] == High[n]) and (High[n+3] <= High[n]) and (High[n+2] == High[n]) and (High[n+1] <= High[n]) and (High[n-1] < High[n]) and (High[n-2] < High[n]))
    upFractal
upFractal=factorh(h)
factorl(Low)=>
    dnFractal = (                                                                                                  (Low[n+2]  > Low[n]) and (Low[n+1]  > Low[n]) and (Low[n-1] > Low[n]) and (Low[n-2] > Low[n]))
             or (                                                                         (Low[n+3]  > Low[n]) and (Low[n+2]  > Low[n]) and (Low[n+1] == Low[n]) and (Low[n-1] > Low[n]) and (Low[n-2] > Low[n]))
             or (                                                (Low[n+4]  > Low[n]) and (Low[n+3]  > Low[n]) and (Low[n+2] == Low[n]) and (Low[n+1] >= Low[n]) and (Low[n-1] > Low[n]) and (Low[n-2] > Low[n]))
             or (                        (Low[n+5] > Low[n]) and (Low[n+4]  > Low[n]) and (Low[n+3] == Low[n]) and (Low[n+2] == Low[n]) and (Low[n+1] >= Low[n]) and (Low[n-1] > Low[n]) and (Low[n-2] > Low[n]))
             or ((Low[n+6] > Low[n]) and (Low[n+5] > Low[n]) and (Low[n+4] == Low[n]) and (Low[n+3] >= Low[n]) and (Low[n+2] == Low[n]) and (Low[n+1] >= Low[n]) and (Low[n-1] > Low[n]) and (Low[n-2] > Low[n]))
    
dnFractal=factorl(l)

U=valuewhen(upFractal[0]!= upFractal[1],l[0],3)
L=valuewhen(dnFractal[0]!=dnFractal[1],h[0],3)

longcon=crossover(close ,L) and close>open
shortcon=crossunder(close ,U) and close<open

if longcon
    
    strategy.entry("Long", strategy.long,   when = strategy.position_size <= 0 )
    
if  shortcon
    strategy.entry("Short", strategy.short,  when = strategy.position_size >= 0 )
        





```

> Detail

https://www.fmz.com/strategy/435469

> Last Modified

2023-12-15 10:37:01
