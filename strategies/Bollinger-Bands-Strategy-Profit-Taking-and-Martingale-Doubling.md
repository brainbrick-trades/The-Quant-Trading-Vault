
> Name

Bollinger-Bands-Strategy-Profit-Taking-and-Martingale-Doubling

> Author

Zer3192



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|20|Length|
|v_input_3|2|Multiplier|
|v_input_4|true|Use Martingale doubling strategy|
|v_input_5|0.001|Initial position size|
|v_input_6|2|Martingale multiplier|


> Source (PineScript)

``` pinescript

//@version=4
strategy("Bollinger Bands %B Crossover", overlay=true,pyramiding = 6)

// Load Bollinger Bands %B indicator
source = input(close, title="Source")
length = input(20, minval=1, title="Length")
mult = input(2.0, minval=0.001, maxval=50, title="Multiplier")
basis = sma(source, length)
dev = mult * stdev(source, length)
upper = basis + dev
lower = basis - dev
bb = (source - lower) / (upper - lower)

// Define long and short conditions
longCondition = crossover(bb, 0)
shortCondition = crossunder(bb, 1)

// Martingale Strategy Parameters
useMartin = input(true, title="Use Martingale doubling strategy")
initialQty = input(0.001, title="Initial position size")
martinFactor = input(2, title="Martingale multiplier")


// When the buying conditions are met, a buy signal is generated and a take-profit and stop-loss are set.
if (longCondition)
    strategy.entry("Buy", strategy.long)
     if useMartin
if close<strategy.position_avg_price*0.95 and strategy.position_size >0
        strategy.order("exitBuy", "Buy",qty=strategy.position_size * martinFactor,when=strategy.long)
if strategy.position_size >0
        strategy.exit("Take Profit/Stop Loss", "Buy", profit=strategy.position_avg_price  * 1.1)

// When the selling conditions are met, a sell signal is generated and a take-profit and stop-loss are set.
if (shortCondition)
    strategy.entry("Sell",strategy.short)
     if useMartin
if close<strategy.position_avg_price*1.05 and strategy.position_size < 0
       strategy.order( "exitSell","Sell", qty=strategy.position_size * martinFactor,when=strategy.short)
if strategy.position_size >0
       strategy.exit("Take Profit/Stop Loss", "Sell", profit=strategy.position_avg_price  * 1.1)



```

> Detail

https://www.fmz.com/strategy/422794

> Last Modified

2023-10-19 08:34:55
