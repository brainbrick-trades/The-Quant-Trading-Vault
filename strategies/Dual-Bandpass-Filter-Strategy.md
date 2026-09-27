
> Name

Dual-Bandpass-Filter-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1838a4c0975c83b5dd1.png)



### Overview

The Dual Bandpass Filter strategy is adapted from the strategy published by Broder in Stocks & Commodities magazine in 2010. It generates trading signals by calculating the value of Broder's bandpass filter to identify price fluctuations in stocks. It goes short when the bandpass filter value is higher than the threshold, and goes long when it is lower, to follow the trend.

### Strategy Logic

The key steps of this strategy are:

1. Initialize parameters including bandpass length `Length`, fluctuation coefficient `Delta`, short zone threshold `SellZone`, and long zone threshold `BuyZone`. 

2. Calculate the Broder bandpass filter `BP` using a series of trigonometric functions.

3. Determine position direction: go short if `BP` is above `SellZone`; go long if below `BuyZone`; otherwise, maintain current position.

4. Output signals: generate long/short signals based on position direction. 

5. Set bar colors based on signal results.

6. Plot the bandpass filter curve.

This strategy captures short-term fluctuations using the Broder bandpass filter, and generates trading signals when the fluctuations reach certain magnitude to follow the trend.

### Advantage Analysis

1. More sensitive to market fluctuations based on the Broder bandpass filter, which can catch short-term trends.

2. The sensitivity can be adjusted through parameter tuning to adapt to different market environments.

3. Simple and clear strategy logic, easy to understand and implement.

4. Parameters can be easily optimized to find the best combination.

5. Visual bandpass filter curve intuitively shows market fluctuations.

### Risk Analysis

1. Overly optimized bandpass filter may become too sensitive and generate false signals.

2. Unable to determine fluctuation end points, may lead to expanding losses.

3. High trading frequency may increase costs and slippage risks. 

4. Vulnerable to black swan events that trigger false signals.

5. Parameters need adjusting for different products and markets.

6. Consider setting stop loss to control loss per trade.

7. Extend exit time or add filters to reduce false signals.

### Optimization Directions

1. Optimize parameters to find the best combination, evaluating win rate, profit ratio, Sharpe ratio etc.

2. Add filters like moving average cross, price patterns to avoid trading in non-trending areas.

3. Consider combining parameters across multiple instruments for basket trading to diversify risks.

4. Add stop loss logic to control loss per trade, like dynamic stops or trailing stops.

5. Add profit taking like moving profit stops to lock in gains. Different levels can be set for different trend stages.

6. Optimize entry signals to avoid false signals in ranging markets. Consider longer holding periods or breakout signals. 

7. Expand to a cross-asset arbitrage system utilizing price differentials for hedging.

8. Backtest optimization for best asset selection and rebalancing strategies.

### Summary

The Dual Bandpass Filter strategy judges price fluctuations using Broder's bandpass filter and generates signals when the fluctuations reach thresholds, with the advantage of high sensitivity to short-term trends and easy implementation. However, it is sensitive to parameters and trading frequency, requiring optimization to reduce false signals and manage risks. Overall, it provides an option for catching short-term trends, but overfitting should be avoided, and other technical tools can be combined for trading.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|20|Length|
|v_input_2|0.5|Delta|
|v_input_3|5|SellZone|
|v_input_4|-5|BuyZone|
|v_input_5|false|Trade reverse|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-10-17 00:00:00
end: 2023-10-23 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 18/09/2018
// The related article is copyrighted material from
// Stocks & Commodities Mar 2010
// You can use in the xPrice any series: Open, High, Low, Close, HL2, HLC3, OHLC4 and ect...
//
// You can change long to short in the Input Settings
// WARNING:
// - For purpose educate only
// - This script to change bars colors.
////////////////////////////////////////////////////////////
strategy(title="Bandpass Filter Strategy ver 2.0")
Length = input(20, minval=1)
Delta = input(0.5)
SellZone = input(5, step = 0.01)
BuyZone = input(-5, step = 0.01)
reverse = input(false, title="Trade reverse")
hline(BuyZone, color=green, linestyle=line)
hline(SellZone, color=red, linestyle=line)
xPrice = hl2
hline(0, color=blue, linestyle=line)
beta = cos(3.14 * (360 / Length) / 180)
gamma = 1 / cos(3.14 * (720 * Delta / Length) / 180)
alpha = gamma - sqrt(gamma * gamma - 1)
BP = 0.5 * (1 - alpha) * (xPrice - xPrice[2]) + beta * (1 + alpha) * nz(BP[1]) - alpha * nz(BP[2])
pos = iff(BP > SellZone, 1,
	   iff(BP <= BuyZone, -1, nz(pos[1], 0))) 
possig = iff(reverse and pos == 1, -1,
          iff(reverse and pos == -1, 1, pos))	   
if (possig == 1) 
    strategy.entry("Long", strategy.long)
if (possig == -1)
    strategy.entry("Short", strategy.short)	   	    
barcolor(possig == -1 ? red: possig == 1 ? green : blue )  
plot(BP, color=red, title="Bandpass Filter Strategy")
```

> Detail

https://www.fmz.com/strategy/430069

> Last Modified

2023-10-24 17:00:02
