
> Name

Dynamic-Moving-Average-Crossover-Trend-Following-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d90376151f47c54222d7.png)
![IMG](https://www.fmz.com/upload/asset/2d80f15f034088daf4844.png)



#### Overview
This strategy is a trend following system based on multiple moving average crossovers, combining SMA and EMA indicators to capture market trends. The strategy utilizes a customizable period Simple Moving Average (SMA) and two Exponential Moving Averages (EMA) to construct a complete trend following trading system. It also integrates dynamic stop-loss and profit target management mechanisms to effectively control risk and lock in profits.

#### Strategy Principles
The strategy primarily makes trading decisions based on the dynamic relationships between three moving averages. The system determines trend direction by monitoring price position relative to SMA and crossovers between fast and slow EMAs. Entry signals are triggered in two ways: first, when price is above (below) SMA and fast EMA crosses above (below) slow EMA; second, when price breaks through SMA and previous price action consistently remains above (below) SMA. The strategy employs a dynamic stop-loss mechanism, with initial stops based on EMA position or fixed percentage, adjusting as profits increase.

#### Strategy Advantages
1. Multiple moving averages working together improve trend identification accuracy and reduce losses from false breakouts
2. Dual entry conditions design captures both early trend opportunities and confirmed trend continuations
3. Dynamic stop-loss mechanism protects profits while allowing trends sufficient room to develop
4. Reasonable profit-to-loss ratio settings achieve good balance between risk control and profit potential
5. Moving average crossovers as additional exit conditions help avoid trend reversal risks

#### Strategy Risks
1. May generate frequent trades resulting in losses in ranging markets
2. Multiple moving average system may lag in rapidly volatile markets
3. Fixed stop-loss multipliers may not suit all market conditions
4. Trailing stops may lock in profits too early in highly volatile markets
5. Over-optimization of parameters may lead to poorer live performance compared to backtests

#### Optimization Directions
1. Introduce volatility indicators to dynamically adjust stop-loss and take-profit multipliers for better market adaptation
2. Add volume indicators as confirmation to improve entry signal reliability
3. Dynamically adjust moving average periods based on market volatility characteristics
4. Implement trend strength filters to avoid frequent trading in weak trend environments
5. Develop adaptive trailing stop mechanisms that dynamically adjust stop distances based on market volatility

#### Summary
The strategy constructs a complete trend following system through the coordination of multiple moving averages, with detailed rules for entries, exits, and risk management. Its strengths lie in effective trend identification and following, while protecting profits through dynamic stop-loss mechanisms. Though inherent risks exist, the proposed optimization directions can further enhance strategy stability and adaptability. The overall design is reasonable, offering good practical value and optimization potential.




> Source (PineScript)

``` pinescript
/*backtest
start: 2025-02-17 17:00:00
end: 2025-02-20 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Binance","currency":"SOL_USDT"}]
*/

//@version=5
strategy("Trading strategy (customEMA/SMAParameters)", overlay=true, initial_capital=100000, currency=currency.EUR, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// Input parameters: adjustable SMA and EMA timeframe
smaLength     = input.int(120, "SMA Length", minval=1, step=1)
emaFastPeriod = input.int(13, "EMA Fast Period", minval=1, step=1)
emaSlowPeriod = input.int(21, "EMA Slow Period", minval=1, step=1)

// Calculate moving average
smaVal   = ta.sma(close, smaLength)
emaFast  = ta.ema(close, emaFastPeriod)
emaSlow  = ta.ema(close, emaSlowPeriod)

// Draw moving average
plot(smaVal, color=color.orange, title="SMA")
plot(emaFast, color=color.blue, title="EMA Fast")
plot(emaSlow, color=color.red, title="EMA Slow")

// Entry Conditions - go long
// condition1:Closing price higher thanSMA and EMA Fast Cross upward EMA Slow
longTrigger1 = (close > smaVal) and ta.crossover(emaFast, emaSlow)
// condition2:Closing price crosses aboveSMA Forward5RootKThe lowest price of the <<#1#>> line is higher than each of itsSMA
longTrigger2 = ta.crossover(close, smaVal) and (low[1] > smaVal[1] and low[2] > smaVal[2] and low[3] > smaVal[3] and low[4] > smaVal[4] and low[5] > smaVal[5])
longCondition = longTrigger1 or longTrigger2

// Entry Conditions - go short
// condition1:Closing price lower thanSMA and EMA Fast Downward Breakthrough EMA Slow
shortTrigger1 = (close < smaVal) and ta.crossunder(emaFast, emaSlow)
// condition2:Closing price crosses belowSMA Forward5RootKThe highest price of the <<#2#>> line is lower than each of itsSMA
shortTrigger2 = ta.crossunder(close, smaVal) and (high[1] < smaVal[1] and high[2] < smaVal[2] and high[3] < smaVal[3] and high[4] < smaVal[4] and high[5] < smaVal[5])
shortCondition = shortTrigger1 or shortTrigger2

// Define variables to record the entry price andEMA FastValue used to calculate stop loss
var float entryPriceLong      = na
var float entryEMA_Fast_Long   = na
var float entryPriceShort     = na
var float entryEMA_Fast_Short = na

// Entry and initial take profit and stop loss settings - go long
// Take stop loss"At Opening PositionEMA FastPrice"and"0.2%stop loss"The larger one among them; the take profit is a multiple of the stop loss5times
if (longCondition and strategy.position_size == 0)
    entryPriceLong      := close
    entryEMA_Fast_Long  := emaFast
    strategy.entry("Long", strategy.long)
    stopPercLong = math.max(0.002, (entryPriceLong - entryEMA_Fast_Long) / entryPriceLong)
    stopLong     = entryPriceLong * (1 - stopPercLong)
    tpLong       = entryPriceLong * (1 + 5 * stopPercLong)
    strategy.exit("LongExit", "Long", stop=stopLong, limit=tpLong)

// Entry and initial take profit and stop loss settings - go short
// Take stop loss"At Opening PositionEMA FastPrice"and"0.2%stop loss"The larger one among them; the take profit is a multiple of the stop loss5times
if (shortCondition and strategy.position_size == 0)
    entryPriceShort      := close
    entryEMA_Fast_Short  := emaFast
    strategy.entry("Short", strategy.short)
    stopPercShort = math.max(0.002, (entryEMA_Fast_Short - entryPriceShort) / entryPriceShort)
    stopShort     = entryPriceShort * (1 + stopPercShort)
    tpShort       = entryPriceShort * (1 - 5 * stopPercShort)
    strategy.exit("ShortExit", "Short", stop=stopShort, limit=tpShort)

// Trailing stop logic
// When position profit reaches0.8%Update stop loss and take profit, and keep take profit and stop loss.5times
var float longHighest = na
if (strategy.position_size > 0)
    longHighest := na(longHighest) ? high : math.max(longHighest, high)
    if (high >= entryPriceLong * 1.008)
        newLongStop = longHighest * (1 - 0.003)
        newPerc     = (entryPriceLong - newLongStop) / entryPriceLong
        newLongTP   = entryPriceLong * (1 + 5 * newPerc)
        strategy.exit("LongExit", "Long", stop=newLongStop, limit=newLongTP)
else
    longHighest := na

var float shortLowest = na
if (strategy.position_size < 0)
    shortLowest := na(shortLowest) ? low : math.min(shortLowest, low)
    if (low <= entryPriceShort * 0.992)
        newShortStop  = shortLowest * (1 + 0.003)
        newPercShort  = (newShortStop - entryPriceShort) / entryPriceShort
        newShortTP    = entryPriceShort * (1 - 5 * newPercShort)
        strategy.exit("ShortExit", "Short", stop=newShortStop, limit=newShortTP)
else
    shortLowest := na

// Additional closing conditions
// If holding a long positionEMA FastBreak belowEMA Slow,Then immediately close long
if (strategy.position_size > 0 and ta.crossunder(emaFast, emaSlow))
    strategy.close("Long", comment="EMABreak Below Flat Long")
// If holding a short positionEMA FastBreak aboveEMA Slow,Then immediately close short
if (strategy.position_size < 0 and ta.crossover(emaFast, emaSlow))
    strategy.close("Short", comment="EMABreak Above Flat Short")

```

> Detail

https://www.fmz.com/strategy/483509

> Last Modified

2025-02-24 09:46:10
