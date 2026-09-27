
> Name

MACD-KDJ-Combined-Martingale-Pyramiding-Quantitative-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/450ec9f4ee9b64520f.png)


#### Overview
This strategy is a Martingale trading system based on MACD and KDJ indicators, combining pyramiding position sizing and dynamic profit/loss management. The strategy determines entry timing through indicator crossovers, utilizes Martingale theory for position management, and enhances returns through pyramiding in trending markets. It features a comprehensive risk control system including total position control, dynamic stop-loss, and drawdown control mechanisms.

#### Strategy Principles
The core logic consists of four key elements: entry signals, position adding mechanism, profit/loss management, and risk control. Entry signals are based on the convergence of MACD line crossing the signal line and KDJ's %K crossing %D line; the position adding mechanism adopts Martingale theory, dynamically adjusting position size through a multiplier factor, supporting up to 10 additional positions; profit-taking uses trailing stops to dynamically adjust take-profit levels; stop-loss includes both fixed and trailing mechanisms. The strategy supports flexible adjustment of indicator parameters, position control parameters, and risk control parameters.

#### Strategy Advantages
1. High signal system reliability: Combines MACD trend indicator and KDJ oscillator to effectively filter false signals
2. Scientific position management: Martingale system can reduce holding costs through adding positions in counter-trends
3. Comprehensive risk control: Multiple stop-loss mechanisms and position limits effectively control risk
4. Optimized return structure: Pyramiding can achieve better returns in trending markets
5. Flexible parameters: Supports strategy parameter optimization for different market characteristics

#### Strategy Risks
1. Market risk: Frequent position additions in ranging markets may lead to enlarged losses
2. Position risk: Martingale system may result in excessive position sizes
3. Liquidity risk: Large capital deployment may face insufficient liquidity issues
4. System risk: Excessive parameter optimization may lead to strategy overfitting

#### Strategy Optimization Directions
1. Signal system optimization: Incorporate volatility indicators to adjust signal sensitivity in high-volatility environments
2. Position management optimization: Design dynamic multiplier factors for adaptive adjustment based on market conditions
3. Risk control optimization: Add drawdown control module to reduce positions during significant drawdowns
4. Parameter optimization: Introduce machine learning methods for adaptive parameter adjustment

#### Summary
The strategy builds a complete quantitative trading system by combining classic technical indicators with advanced position management methods. Its core advantages lie in signal reliability and comprehensive risk control, while maintaining strong adaptability through parameterization. Although inherent risks exist, continuous optimization and improvement allow the strategy to maintain stable performance across different market environments.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-11-04 00:00:00
end: 2024-12-04 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © aaronxu567
//@version=5
strategy("MACD and KDJ Opening Conditions with Pyramiding and Exit", overlay=true) // pyramiding

// Setting
initialOrder = input.float(50000.0, title="Initial Order") 
initialOrderSize = initialOrder/close
//initialOrderSize = input.float(1.0, title="Initial Order Size") // Initial Order Size
macdFastLength = input.int(9, title="MACD Fast Length") // MACD Setting
macdSlowLength = input.int(26, title="MACD Slow Length")
macdSignalSmoothing = input.int(9, title="MACD Signal Smoothing")
kdjLength = input.int(14, title="KDJ Length")
kdjSmoothK = input.int(3, title="KDJ Smooth K")
kdjSmoothD = input.int(3, title="KDJ Smooth D")
enableLong = input.bool(true, title="Enable Long Trades")
enableShort = input.bool(true, title="Enable Short Trades")

// Additions Setting
maxAdditions = input.int(5, title="Max Additions", minval=1, maxval=10) // Max Additions
addPositionPercent = input.float(1.0, title="Add Position Percent", minval=0.1, maxval=10) // Add Conditions
reboundPercent = input.float(0.5, title="Rebound Percent (%)", minval=0.1, maxval=10) // Rebound 
addMultiplier = input.float(1.0, title="Add Multiplier", minval=0.1, maxval=10) // 

// Stop Setting
takeProfitTrigger = input.float(2.0, title="Take Profit Trigger (%)", minval=0.1, maxval=10) // 
trailingStopPercent = input.float(0.3, title="Trailing Stop (%)", minval=0.1, maxval=10) // 
stopLossPercent = input.float(6.0, title="Stop Loss Percent", minval=0.1, maxval=10) // 

// MACD Calculation
[macdLine, signalLine, _] = ta.macd(close, macdFastLength, macdSlowLength, macdSignalSmoothing)

// KDJ Calculation
k = ta.sma(ta.stoch(close, high, low, kdjLength), kdjSmoothK)
d = ta.sma(k, kdjSmoothD)
j = 3 * k - 2 * d

// Long Conditions
enterLongCondition = enableLong and ta.crossover(macdLine, signalLine) and ta.crossover(k, d)

// Short Conditions
enterShortCondition = enableShort and ta.crossunder(macdLine, signalLine) and ta.crossunder(k, d)

// Records
var float entryPriceLong = na
var int additionsLong = 0 // Record the number of additions to long positions
var float nextAddPriceLong = na // The trigger price for the next increase in long positions
var float lowestPriceLong = na // Lowest long price
var bool longPending = false // Long position pending mark

var float entryPriceShort = na
var int additionsShort = 0 // Record the number of times of empty position and added position
var float nextAddPriceShort = na // Trigger price for next increase of short position
var float highestPriceShort = na // Highest short price
var bool shortPending = false // Short position add pending mark

var bool plotEntryLong = false
var bool plotAddLong = false
var bool plotEntryShort = false
var bool plotAddShort = false

// Open Long
if (enterLongCondition and strategy.opentrades == 0)
    strategy.entry("long", strategy.long, qty=initialOrderSize,comment = 'Long')
    entryPriceLong := close
    nextAddPriceLong := close * (1 - addPositionPercent / 100)
    additionsLong := 0
    lowestPriceLong := na
    longPending := false
    plotEntryLong := true

// Add Long
if (strategy.position_size > 0 and additionsLong < maxAdditions)
    // Conditions Checking
    if (close < nextAddPriceLong) and not longPending
        lowestPriceLong := close
        longPending := true

    if (longPending)
        // Rebound Checking
        if (close > lowestPriceLong * (1 + reboundPercent / 100))
            // Record Price
            float addQty = initialOrderSize*math.pow(addMultiplier,additionsLong+1)
            strategy.entry("long", strategy.long, qty=addQty,comment = 'Add Long')
            additionsLong += 1
            longPending := false
            nextAddPriceLong := math.min(nextAddPriceLong, close) * (1 - addPositionPercent / 100) // Price Updates
            plotAddLong := true
        else
            lowestPriceLong := math.min(lowestPriceLong, close)

// Open Short
if (enterShortCondition and strategy.opentrades == 0)
    strategy.entry("short", strategy.short, qty=initialOrderSize,comment = 'Short')
    entryPriceShort := close
    nextAddPriceShort := close * (1 + addPositionPercent / 100)
    additionsShort := 0
    highestPriceShort := na
    shortPending := false
    plotEntryShort := true

// add Short
if (strategy.position_size < 0 and additionsShort < maxAdditions)
    // Conditions Checking
    if (close > nextAddPriceShort) and not shortPending
        highestPriceShort := close
        shortPending := true

    if (shortPending)
        // rebound Checking
        if (close < highestPriceShort * (1 - reboundPercent / 100))
            // Record Price
            float addQty = initialOrderSize*math.pow(addMultiplier,additionsShort+1)
            strategy.entry("short", strategy.short, qty=addQty,comment = "Add Short")
            additionsShort += 1
            shortPending := false
            nextAddPriceShort := math.max(nextAddPriceShort, close) * (1 + addPositionPercent / 100) // Price Updates
            plotAddShort := true
        else
            highestPriceShort := math.max(highestPriceShort, close)

// Take Profit or Stop Loss
if (strategy.position_size != 0)
    float stopLossLevel = strategy.position_avg_price * (strategy.position_size > 0 ? (1 - stopLossPercent / 100) : (1 + stopLossPercent / 100))
    float trailOffset = strategy.position_avg_price * (trailingStopPercent / 100) / syminfo.mintick

    if (strategy.position_size > 0)
        strategy.exit("Take Profit/Stop Loss", from_entry="long", stop=stopLossLevel, trail_price=strategy.position_avg_price * (1 + takeProfitTrigger / 100), trail_offset=trailOffset)
    else
        strategy.exit("Take Profit/Stop Loss", from_entry="short", stop=stopLossLevel, trail_price=strategy.position_avg_price * (1 - takeProfitTrigger / 100), trail_offset=trailOffset)

// Plot
plotshape(series=plotEntryLong, location=location.belowbar, color=color.blue, style=shape.triangleup, size=size.small, title="Long Signal")
plotshape(series=plotAddLong, location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small, title="Add Long Signal")
plotshape(series=plotEntryShort, location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small, title="Short Signal")
plotshape(series=plotAddShort, location=location.abovebar, color=color.orange, style=shape.triangledown, size=size.small, title="Add Short Signal")

// Plot Clear
plotEntryLong := false
plotAddLong := false
plotEntryShort := false
plotAddShort := false



// // table
// var infoTable = table.new(position=position.top_right,columns = 2,rows = 6,bgcolor=color.yellow,frame_color = color.white,frame_width = 1,border_width = 1,border_color = color.black)
// if barstate.isfirst
//     t1="Open Price"
//     t2="Avg Price"
//     t3="Additions"
//     t4='Next Add Price'
//     t5="Take Profit"
//     t6="Stop Loss"
//     table.cell(infoTable, column = 0, row = 0,text=t1       ,text_size=size.auto)
//     table.cell(infoTable, column = 0, row = 1,text=t2       ,text_size=size.auto)
//     table.cell(infoTable, column = 0, row = 2,text=t3       ,text_size=size.auto)
//     table.cell(infoTable, column = 0, row = 3,text=t4       ,text_size=size.auto)
//     table.cell(infoTable, column = 0, row = 4,text=t5       ,text_size=size.auto)
//     table.cell(infoTable, column = 0, row = 5,text=t6       ,text_size=size.auto)
// if barstate.isconfirmed and strategy.position_size!=0
//     ps=strategy.position_size
//     pos_avg=strategy.position_avg_price
//     opt=strategy.opentrades
//     t1=str.tostring(strategy.opentrades.entry_price(0),format.mintick)
//     t2=str.tostring(pos_avg,format.mintick)
//     t3=str.tostring(opt>1?(opt-1):0)
//     t4=str.tostring(ps>0?nextAddPriceLong:nextAddPriceShort,format.mintick)
//     t5=str.tostring(pos_avg*(1+(ps>0?1:-1)*takeProfitTrigger*0.01),format.mintick)
//     t6=str.tostring(pos_avg*(1+(ps>0?-1:1)*stopLossPercent*0.01),format.mintick)
//     table.cell(infoTable, column = 1, row = 0,text=t1  ,text_size=size.auto)
//     table.cell(infoTable, column = 1, row = 1,text=t2  ,text_size=size.auto)
//     table.cell(infoTable, column = 1, row = 2,text=t3  ,text_size=size.auto)
//     table.cell(infoTable, column = 1, row = 3,text=t4  ,text_size=size.auto)
//     table.cell(infoTable, column = 1, row = 4,text=t5  ,text_size=size.auto)
//     table.cell(infoTable, column = 1, row = 5,text=t6  ,text_size=size.auto)
    
```

> Detail

https://www.fmz.com/strategy/474057

> Last Modified

2024-12-05 16:35:26
