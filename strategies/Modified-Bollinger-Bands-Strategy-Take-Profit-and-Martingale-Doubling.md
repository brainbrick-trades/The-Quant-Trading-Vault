
> Name

Modified-Bollinger-Bands-Strategy-Take-Profit-and-Martingale-Doubling

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
|v_input_7|1.5|Take-profit multiple|
|v_input_8|0.95|Stop loss multiple|


> Source (PineScript)

``` pinescript

//@version=4
strategy("Bollinger Bands %B Crossover", overlay=true,pyramiding = 5)

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
// take profit and stop loss
profitTarget = input(1.5, title="Take-profit multiple")
stopLoss = input(0.95, title="Stop loss multiple")
//Define the percentage to trigger adding positions
dropPercentage=10
//Calculate current total position cost
totalCost=strategy.position_avg_price*strategy.position_size
//Calculate current position profit and loss
profitLoss=(close-totalCost)/totalCost*100



// When the buying conditions are met, a buy signal is generated, and take-profit is set
if (longCondition)
    strategy.entry("Buy", strategy.long)
     if useMartin
//Determine whether to add position
if profitLoss<=-dropPercentage and strategy.position_size >0
        strategy.order("Buy1", "Buy",qty=strategy.position_size * martinFactor,when=strategy.long )
if strategy.position_size >0
        strategy.exit("Take Profit/Stop Loss", "Buy", profit=strategy.position_avg_price  *profitTarget )

// When the selling conditions are met, a sell signal is generated, and take-profit is set
if (shortCondition)
    strategy.entry("Sell",strategy.short)
     if useMartin
//Determine whether to add position
if profitLoss<= -dropPercentage and strategy.position_size <0
       strategy.order( "Sell2","Sell", qty=strategy.position_size * martinFactor,when=strategy.short)
if strategy.position_size <0
       strategy.exit("Take Profit/Stop Loss", "Sell", profit=strategy.position_avg_price  *stopLoss )



```

> Detail

https://www.fmz.com/strategy/429401

> Last Modified

2023-10-29 21:56:29
