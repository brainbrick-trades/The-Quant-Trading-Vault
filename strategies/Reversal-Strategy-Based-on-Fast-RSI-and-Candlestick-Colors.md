
> Name

Reversal-Strategy-Based-on-Fast-RSI-and-Candlestick-Colors

> Author

ChaoZhang

> Strategy Description



  
The name of this strategy is "Reversal Strategy Based on Fast RSI and candlestick Color". This strategy uses fast RSI to determine overbought and oversold and the candlestick color to determine the trend direction, and conducts reversal trades when the two send common signals.

The fast RSI indicator parameter setting is smaller and can capture the overbought and oversold phenomenon of the price more quickly. When the Rapid RSI is below 30, it means oversold, and when it is above 70, it means overbought.

KLine color white indicates price closed near the opening price, green represents a price increase, red represents a price decrease.

Trading logic is as follows:

When the fast RSI shows oversold, and four consecutive red candlesticks appear, it is considered a strong reversal signal to go long.;

When the fast RSI shows overbought, and four consecutive green candlesticks appear, it is considered a strong reversal signal to go short.;

If currently holding a long position, close it on one green candlestick; if currently holding a short position, close it on one red candlestick.

The advantage of this strategy is that the indicator combination is accurate and reliable in judging reversal signals. However, due to the large investment intensity, strict fund management is required. A stop-loss strategy is also required.

In general, reversal trading relies on indicators to accurately determine timing. Reasonable application of indicators such as RSI and supplemented by candlestick information can improve the strategy effect. However, no single strategy can be perfect, and traders still need to maintain flexibility in trading thinking.




||



This strategy is named "Reversal Strategy Based on Fast RSI and Candlestick Colors". It uses the fast RSI to judge overbought/oversold levels and candlestick colors to determine trend direction, entering reversal trades when both give concurring signals.

The fast RSI has smaller parameters and can more quickly detect price overbought/oversold conditions. RSI below 30 suggests oversold state, while above 70 is overbought. 

Candlestick colors show white prices closing near open, green represents rising and red flags falling prices. 

The trading logic is:

When fast RSI shows oversold and 4 consecutive red candles appear, it is considered a strong reversal signal for going long.

When fast RSI overbought and 4 straight green candles appear, it signals a strong reversal opportunity for going short.

If already holding long positions, exit when 1 green candle appears. If holding short positions, exit when 1 red candle appears.

The advantage of this strategy is using indicator combos to accurately determine reversal signals. But strict money management is required due to heavy position sizing. Stop loss is also essential.

In summary, reversal trading relies on indicators precisely identifying timing. Reasonable application of RSI plus candlestick information can improve strategy performance. But no single strategy is perfect. Traders still need to maintain flexible trading mindset.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Long|
|v_input_2|true|Short|
|v_input_3|5|leverage|
|v_input_4|true|Only Profit|
|v_input_5|7|Fast RSI Period|
|v_input_6|30|RSI limit|
|v_input_7_close|0|RSI Price: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_8|true|RSI Bars|
|v_input_9|4|Color Bars|
|v_input_10|1900|From Year|
|v_input_11|2100|To Year|
|v_input_12|true|From Month|
|v_input_13|12|To Month|
|v_input_14|true|From day|
|v_input_15|31|To day|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-09-06 00:00:00
end: 2023-01-20 00:00:00
period: 4d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//Noro
//2018

//@version=2
strategy(title = "Noro's Hundred Strategy v1.0", shorttitle = "Hundred str 1.0", overlay = true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, pyramiding = 0)

//Settings
needlong = input(true, defval = true, title = "Long")
needshort = input(true, defval = true, title = "Short")
lev = input(5, defval = 5, minval = 1, maxval = 100, title = "leverage")
onlyprofit = input(true, defval = true, title = "Only Profit")
fast = input(7, defval = 7, minval = 2, maxval = 50, title = "Fast RSI Period")
limit = input(30, defval = 30, minval = 1, maxval = 100, title = "RSI limit")
rsisrc = input(close, defval = close, title = "RSI Price")
rsibars = input(1, defval = 1, minval = 1, maxval = 20, title = "RSI Bars")
cbars = input(4, defval = 4, minval = 1, maxval = 20, title = "Color Bars")
fromyear = input(1900, defval = 1900, minval = 1900, maxval = 2100, title = "From Year")
toyear = input(2100, defval = 2100, minval = 1900, maxval = 2100, title = "To Year")
frommonth = input(01, defval = 01, minval = 01, maxval = 12, title = "From Month")
tomonth = input(12, defval = 12, minval = 01, maxval = 12, title = "To Month")
fromday = input(01, defval = 01, minval = 01, maxval = 31, title = "From day")
today = input(31, defval = 31, minval = 01, maxval = 31, title = "To day")

//Fast RSI
fastup = rma(max(change(rsisrc), 0), fast)
fastdown = rma(-min(change(rsisrc), 0), fast)
fastrsi = fastdown == 0 ? 100 : fastup == 0 ? 0 : 100 - (100 / (1 + fastup / fastdown))

//Limits
bar = close > open ? 1 : close < open ? -1 : 0
uplimit = 100 - limit
dnlimit = limit

//RSI Bars
upsignal = fastrsi > uplimit ? 1 : 0
dnsignal = fastrsi < dnlimit ? 1 : 0
uprsi = sma(upsignal, rsibars) == 1
dnrsi = sma(dnsignal, rsibars) == 1

//Signals
long = strategy.position_size >= 0
short = strategy.position_size <= 0
up = sma(bar, cbars) == -1 and long and dnrsi
dn = sma(bar, cbars) == 1 and short and uprsi
profit = (strategy.position_size > 0 and close > strategy.position_avg_price) or (strategy.position_size < 0 and close < strategy.position_avg_price) or onlyprofit == false
exit = ((strategy.position_size > 0 and bar == 1) or (strategy.position_size < 0 and bar == -1)) and profit
lot = strategy.position_size == 0 ? strategy.equity / close * lev : lot[1]

//Trading
if up
    if strategy.position_size < 0
        strategy.close_all()
        
    strategy.entry("Long", strategy.long, needlong == false ? 0 : lot)

if dn
    if strategy.position_size > 0
        strategy.close_all()
        
    strategy.entry("Short", strategy.short, needshort == false ? 0 : lot)
    
if time > timestamp(toyear, tomonth, today, 23, 59) or exit
    strategy.close_all()
```

> Detail

https://www.fmz.com/strategy/426616

> Last Modified

2023-09-13 17:24:54
