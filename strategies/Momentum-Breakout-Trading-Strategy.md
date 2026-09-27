
> Name

Momentum-Breakout-Trading-Strategy

> Author

ChaoZhang

> Strategy Description



## Overview

This strategy uses the momentum indicator Bollinger Bands for breakout trading. It mainly determines whether the price breaks through the upper and lower rails of the Bollinger Bands and sends out buying and selling signals.

## Principle

This strategy is mainly based on the Bollinger Bands indicator to determine the trend direction. Bollinger Bands are strips formed by moving averages and their standard deviations. The middle line of Bollinger Bands is the n-day moving average, the upper track is the middle line + 2 times the standard deviation, and the lower track is the middle line - 2 times the standard deviation. When the price is close to the upper band, it is overbought, and when it is close to the lower band, it is oversold.

Specifically, the strategy first calculates the highest price, lowest price within n days, and calculates the middle price ((highest price + lowest price)/2). Then calculate the weighted moving average of the distance between the closing price and the middle price to form the middle line of the Bollinger Bands, and add 2 times the standard deviation above and below the middle line to form the upper and lower rails.

If the closing price breaks through the upper band, it indicates an upward trend; if it breaks through the lower band, it indicates a downward trend. Go long when it breaks through the upper band, go short when it breaks through the lower band.

In addition, the strategy also introduces a reverse position opening mechanism. When the price breaks through the upper Bollinger Band, if MACD is falling, short selling will be taken against the market.

## Advantage

1. Use Bollinger Bands to determine trend direction and possess certain trend-following capabilities.

2. Reverse opening design can obtain counter-trend profits.

3. You can customize Bollinger Band cycle, standard deviation multiple and other parameters to adapt to transactions of different cycles.

4. Can close reverse positions to reduce risk.

## Risks and Countermeasures

1. Bollinger Bands are often used for high-volatility stocks and may not be suitable for long-cycle Resources or indices. Can test the effects of different cycle parameters.

2. Breakout signals may result in false breakouts. Can combine with other factors to filter signals.

3. Reverse positions may further increase losses. The reverse position module can be turned off.

4. The retracement may be larger. Position size can be adjusted appropriately.

## Optimization Direction

1. Consider adding trend filtering to avoid unclear directional oscillation markets.

2. You can test the Bollinger Band standard deviation multiples to find more suitable parameters.

3. Stop-loss strategy can be introduced to control single trade loss.

4. Can optimize opening and adding position logic to make trading signals clearer.

## Summary

This strategy uses Bollinger Bands as the basic indicator to judge price trend breakthroughs for trading. Basic trend following strategies can be implemented using simple parameter settings. However, there is a certain risk of false breakthroughs, and it needs to be filtered with other indicators. Parameter settings, stop-loss strategies, etc. can be further optimized to control risks.


## Overview

This strategy uses Bollinger Bands momentum indicator for breakout trading, mainly judging if price breaks through the upper or lower Bollinger Bands for trading signals.

## Principles 

The strategy is primarily based on Bollinger Bands indicator to determine trend direction. Bollinger Bands consist of a middle band based on a moving average and upper/lower bands defined by standard deviations. The middle band is a n-period moving average, the upper band is middle band + 2 standard deviations, and the lower band is middle band - 2 standard deviations. When price approaches the upper band it indicates overbought conditions, and when it approaches the lower band it signals oversold conditions.

Specifically, the strategy first calculates the highest high and lowest low over last n periods, and the middle price ((highest high + lowest low)/2). It then calculates the distance between close price and middle price, uses exponential moving average of the distance to form the middle band, and adds/subtracts 2 times standard deviation above and below to form the upper and lower bands. 

When close price breaks through the upper band, it signals an uptrend; when it breaks the lower band, it signals a downtrend. The strategy goes long when the upper band is broken, and goes short when the lower band is broken.

In addition, the strategy incorporates a counter-trend mechanism. When price breaks the upper band but MACD is falling, it will take a counter-trend short position.

## Advantages

1. Using Bollinger Bands to determine trend direction provides certain trend following capability.

2. Counter-trend design allows profiting from reversals. 

3. Customizable parameters like period and standard deviation multiples make it adaptable to different trading horizons.

4. Disable counter-trend trading to reduce risk.

## Risks and Mitigations

1. Bollinger Bands work best for high volatility stocks, may not be suitable for stable commodities or indices. Can test different period parameters.

2. Breakout signals may have false breakouts. Can add filters with other indicators.

3. Counter-trend trading can further increase losses. Can disable counter-trend module. 

4. Drawdowns may be significant. Can adjust position sizing.

## Enhancement Opportunities

1. Consider adding trend filter to avoid whipsaw in non-directional markets.

2. Test different standard deviation multiples to find optimal parameters.

3. Incorporate stop loss to control single trade loss.

4. Optimize entry and add-on logic for clearer trading signals.

## Summary

The strategy uses Bollinger Bands as the primary indicator and trades based on trend breakouts. With simple parameters it provides basic trend following capabilities. But false breakout risks exist, requiring additional filters. Parameters, stop loss and risk controls can be enhanced. Overall it serves as a reasonable baseline breakout strategy.



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Long|
|v_input_2|true|Short|
|v_input_3|false|take, %|
|v_input_4|true|Bands Entry|
|v_input_5|false|Counter-trend entry|
|v_input_6|10|Body length|
|v_input_7|true|Trend bars|
|v_input_8|20|Period|
|v_input_9|true|Show Bands|
|v_input_10|true|Show Background|
|v_input_11|1900|From Year|
|v_input_12|2100|To Year|
|v_input_13|true|From Month|
|v_input_14|12|To Month|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-08-18 00:00:00
end: 2023-09-17 00:00:00
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//Noro
//2018

//@version=2
strategy("Noro's Bands Scalper Strategy v1.6", shorttitle = "Scalper str 1.6", overlay = true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100.0, pyramiding = 0)

//Settings
needlong = input(true, defval = true, title = "Long")
needshort = input(true, defval = true, title = "Short")
takepercent = input(0, defval = 0, minval = 0, maxval = 1000, title = "take, %")
needbe = input(true, defval = true, title = "Bands Entry")
needct = input(false, defval = false, title = "Counter-trend entry")
bodylen = input(10, defval = 10, minval = 0, maxval = 50, title = "Body length")
trb = input(1, defval = 1, minval = 1, maxval = 5, title = "Trend bars")
len = input(20, defval = 20, minval = 2, maxval = 200, title = "Period")
needbb = input(true, defval = true, title = "Show Bands")
needbg = input(true, defval = true, title = "Show Background")
fromyear = input(1900, defval = 1900, minval = 1900, maxval = 2100, title = "From Year")
toyear = input(2100, defval = 2100, minval = 1900, maxval = 2100, title = "To Year")
frommonth = input(01, defval = 01, minval = 01, maxval = 12, title = "From Month")
tomonth = input(12, defval = 12, minval = 01, maxval = 12, title = "To Month")
src = close

//PriceChannel 1
lasthigh = highest(src, len)
lastlow = lowest(src, len)
center = (lasthigh + lastlow) / 2

//Distance
dist = abs(src - center)
distsma = sma(dist, len)
hd = center + distsma
ld = center - distsma
hd2 = center + distsma * 2
ld2 = center - distsma * 2

//Trend
chd = close > hd
cld = close < ld
uptrend = trb == 1 and chd ? 1 : trb == 2 and chd and chd[1] ? 1 : trb == 3 and chd and chd[1] and chd[2] ? 1 : trb == 4 and chd and chd[1] and chd[2] and chd[3] ? 1 : trb == 5 and chd and chd[1] and chd[2] and chd[3] and chd[4] ? 1 : 0
dntrend = trb == 1 and cld ? 1 : trb == 2 and cld and cld[1] ? 1 : trb == 3 and cld and cld[1] and cld[2] ? 1 : trb == 4 and cld and cld[1] and cld[2] and cld[3] ? 1 : trb == 5 and cld and cld[1] and cld[2] and cld[3] and cld[4] ? 1 : 0
trend = dntrend == 1 and high < center ? -1 : uptrend == 1 and low > center ? 1 : trend[1]

//trend = close < ld and high < center ? -1 : close > hd and low > center ? 1 : trend[1]

//Lines
colo = needbb == false ? na : black
plot(hd2, color = colo, linewidth = 1, transp = 0, title = "High band 2")
plot(hd, color = colo, linewidth = 1, transp = 0, title = "High band 1")
plot(center, color = colo, linewidth = 1, transp = 0, title = "center")
plot(ld, color = colo, linewidth = 1, transp = 0, title = "Low band 1")
plot(ld2, color = colo, linewidth = 1, transp = 0, title = "Low band 2")

//Background
col = needbg == false ? na : trend == 1 ? lime : red
bgcolor(col, transp = 80)

//Body
body = abs(close - open)
smabody = ema(body, 30) / 10 * bodylen

//Signals
bar = close > open ? 1 : close < open ? -1 : 0
up7 = trend == 1 and ((bar == -1 and bar[1] == -1) or (body > smabody and bar == -1)) ? 1 : 0
dn7 = trend == 1 and ((bar == 1 and bar[1] == 1) or (close > hd and needbe == true)) and close > strategy.position_avg_price * (100 + takepercent) / 100 ? 1 : 0
up8 = trend == -1 and ((bar == -1 and bar[1] == -1) or (close < ld2 and needbe == true)) and close < strategy.position_avg_price * (100 - takepercent) / 100 ? 1 : 0
dn8 = trend == -1 and ((bar == 1 and bar[1] == 1) or (body > smabody and bar == 1)) ? 1 : 0

if up7 == 1 or up8 == 1 
    strategy.entry("Long", strategy.long, needlong == false ? 0 : trend == -1 and needct == false ? 0 : na, when=(time > timestamp(fromyear, frommonth, 01, 00, 00) and time < timestamp(toyear, tomonth, 31, 00, 00)))

if dn7 == 1 or dn8 == 1
    strategy.entry("Short", strategy.short, needshort == false ? 0 : trend == 1 and needct == false ? 0 : na, when=(time > timestamp(fromyear, frommonth, 01, 00, 00) and time < timestamp(toyear, tomonth, 31, 00, 00)))
    
if time > timestamp(toyear, tomonth, 31, 00, 00)
    strategy.close_all()
```

> Detail

https://www.fmz.com/strategy/427185

> Last Modified

2023-09-18 21:28:22
