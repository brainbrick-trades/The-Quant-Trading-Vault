
> Name

Multi-EMA-Trend-Following-Strategy-with-Dynamic-Position-Management-System

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d947ad81628f572d3ae4.png)
![IMG](https://www.fmz.com/upload/asset/2d8db8b6d656ed24d199a.png)



## Overview

The Multi-EMA Trend Following Strategy with Dynamic Position Management System is a quantitative trading strategy based on multiple Exponential Moving Averages (EMAs). This strategy monitors five different EMA periods (12, 144, 169, 576, and 676) to construct a complete trading system, including trend determination, entry signal identification, batch position building, dynamic stop-loss, and dynamic take-profit mechanisms. The strategy supports multiple position additions, with a maximum of 5 trading positions, and implements independent risk control measures for each position. The system precisely captures market trend reversal points through the arrangement of EMA indicators and the intersection relationship between price and key moving averages, achieving batch position building and profit-taking while maintaining the trend.

## Strategy Principles

The core logic of this strategy is based on the positional relationship between multiple EMA indicators and the interaction between price and key EMAs:

1. **Trend Determination Mechanism**:
   - Long trend condition: EMA12 > EMA144 > EMA169 > EMA576 > EMA676
   - Short trend condition: EMA12 < EMA144 < EMA169 < EMA576 < EMA676

2. **Entry Signals**:
   - Long entry: When the low breaks through EMA144 and the closing price is above EMA169, under the long trend condition
   - Short entry: When the high breaks through EMA144 and the closing price is below EMA169, under the short trend condition

3. **Batch Position Building**:
   - First position: Entry signal is met with no existing positions
   - Second position: Entry signal is met with one existing position
   - Third to fifth positions: In addition to meeting the entry signal, the time interval since the last position must exceed 50 candles

4. **Dynamic Stop-Loss and Take-Profit**:
   - Each position adopts a dynamic stop-loss point based on the lowest price (for longs) or highest price (for shorts) of 12 candles at the time of entry
   - Applies a symmetrical take-profit strategy with target price being "entry price + (entry price - stop-loss price)"
   - Batch profit-taking: When each position reaches the take-profit level, 50% is closed first, and the remaining portion continues to be held until the stop-loss is triggered

5. **Overall Risk Control**:
   - All positions are closed when the EMA12 and EMA144 indicators cross (EMA12 breaks below EMA144 in a long trend, or EMA12 breaks above EMA144 in a short trend)
   
Overall, this strategy establishes market trend direction through multiple EMA arrangements, determines entry timing through price interaction with EMA144, sets dynamic stop-loss and take-profit levels based on recent price fluctuation ranges, and optimizes capital management through batch position building and profit-taking, ultimately forming a complete trading system.

## Strategy Advantages

1. **Systematic Trend Determination**:
   - Utilizes five EMAs of different periods to form a multi-dimensional trend determination system, reducing risks from false breakouts
   - The arrangement of EMA indicators provides a quantitative standard for trend strength, making trading decisions more objective

2. **Precise Entry Mechanism**:
   - Combines price and moving average crossovers as entry trigger conditions, improving entry timing effectiveness
   - Requires confirmation of entry signals within 12 candles, reducing the risk of lagging trades

3. **Intelligent Capital Management**:
   - Supports up to 5 positions with batch building, adapting to different market development stages
   - Subsequent positions require a minimum time interval (50 candles), avoiding excessive position building in a short period

4. **Flexible Profit Strategy**:
   - Adopts the "symmetrical take-profit" principle, dynamically calculating target profit levels based on entry price and stop-loss point
   - Batch profit-taking (50% position) secures partial profits while retaining upside potential

5. **Strict Risk Control**:
   - Each position has an independent stop-loss point based on recent volatility range (12 candles)
   - Trend reversal signals (EMA12 and EMA144 crossover) trigger complete position closure, stopping losses promptly

6. **High Adaptability**:
   - Supports both long and short trades, adapting to various market environments
   - Through parameter adjustments (such as ATR multiple, candle count), it can adapt to different instruments and timeframes

## Strategy Risks

1. **Moving Average Lag Risk**:
   - EMA indicators have a certain lag, which may lead to poor entry or exit timing during dramatic market fluctuations
   - Mitigation: Consider incorporating short-term momentum indicators as supplements to improve system reaction speed

2. **Capital Pressure from Batch Position Building**:
   - The strategy supporting up to 5 positions may lead to excessive capital concentration
   - Mitigation: Set reasonable capital allocation ratio for each position based on total capital, ensuring balanced distribution

3. **Limitations of Fixed Period Parameters**:
   - The EMA periods in the code (12, 144, 169, 576, 676) are fixed values, which may not be suitable for all market environments
   - Mitigation: Introduce adaptive period calculation methods or establish dedicated parameter optimization processes for different instruments

4. **Potential Issues with Symmetrical Take-Profit**:
   - In strong trend markets, symmetrical take-profit may secure profits too early, missing larger profit opportunities
   - Mitigation: Consider setting trailing stop-loss for the remaining 50% position to adapt to strong trend markets

5. **Overly Strict Entry Conditions**:
   - The combination of multiple conditions (EMA arrangement + price crossover + closing confirmation) may cause missing some effective signals
   - Mitigation: Set alternative entry mechanisms for different market phases to improve signal capture sensitivity

6. **Data Dependency Risk**:
   - The strategy relies on long-period EMAs (such as 576, 676), requiring sufficient historical data to operate effectively
   - Mitigation: Consider using alternative indicators or adjusting the calculation methods for long-period EMAs when data is insufficient

## Strategy Optimization Directions

1. **Introduce Adaptive Parameter Mechanism**:
   - Change fixed EMA periods (12, 144, 169, 576, 676) to adaptive parameters based on market volatility
   - Optimization reason: Optimal EMA periods vary significantly across different market environments; an adaptive mechanism can improve strategy universality

2. **Enhance Entry Signal Filtering**:
   - Incorporate additional confirmation conditions such as volume and market volatility (e.g., ATR) for entry signals
   - Optimization reason: Pure moving average crossover signals are easily disturbed by market noise; additional filtering conditions can improve signal quality

3. **Improve Capital Management System**:
   - Dynamically adjust the capital allocation ratio for each position based on total account capital and market volatility
   - Optimization reason: The current strategy's capital allocation ratio is fixed and cannot automatically adjust according to risk levels; introducing dynamic capital management can improve capital utilization efficiency

4. **Optimize Stop-Loss and Take-Profit Mechanisms**:
   - Design differentiated stop-loss and take-profit strategies for different position entries, such as fixed ratio take-profit for initial positions and trailing stop-loss for subsequent positions
   - Optimization reason: A uniform stop-loss and take-profit strategy is difficult to adapt to different market phases; differentiated strategies can more flexibly respond to market changes

5. **Add Time Filters**:
   - Introduce trading time filtering mechanisms to avoid high volatility periods (such as market open, pre-close) or major data release periods
   - Optimization reason: Market fluctuations during specific time periods often lack directionality; adding time filters can avoid unnecessary trades

6. **Add Trend Strength Assessment**:
   - Develop trend strength indicators and only allow trading when trend strength reaches a threshold
   - Optimization reason: The current strategy generates signals even in weak trend environments; introducing trend strength assessment can reduce false signals in oscillating markets

7. **Build Multi-Timeframe Coordination System**:
   - Incorporate trend determination from higher timeframes as a trading direction filter
   - Optimization reason: Single timeframe trading systems are easily affected by short-term fluctuations; multi-timeframe coordination can improve system stability

## Summary

The Multi-EMA Trend Following Strategy with Dynamic Position Management System is a quantitative trading strategy with complete structure and clear logic. The strategy establishes a trend determination framework through multiple EMA arrangements, determines entry timing through the interaction between price and key moving averages, and achieves refined capital management and risk control through batch position building and dynamic stop-loss and take-profit mechanisms. The advantages of the strategy lie in systematic trend determination, precise entry mechanisms, intelligent capital management, and strict risk control, making it adaptable to different market environments.

However, the strategy also has risks such as moving average lag, fixed parameter limitations, and capital management pressure. To further enhance the strategy's performance, considerations can be given to introducing adaptive parameter mechanisms, enhancing signal filtering, improving capital management systems, optimizing stop-loss and take-profit mechanisms, and building multi-timeframe coordination systems.

Overall, this strategy provides a highly operable framework for quantitative trading by balancing trend following with risk control. Through continuous optimization and parameter adjustments for specific market environments, the strategy has the potential to achieve stable performance in actual trading.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-09-08 00:00:00
end: 2024-12-08 00:00:00
period: 2h
basePeriod: 2h
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=6
strategy("Professional level trading system", overlay=false, close_entries_rule = "ANY")
x1 = input.float(1.5,"atrMultiples",step=0.1)
x2 = input.int(50,"kNumber of lines",step=1)
s1 = strategy.opentrades.entry_price(0)
s2 = strategy.opentrades.entry_price(1)
s3 = strategy.opentrades.entry_price(2)
s4 = strategy.opentrades.entry_price(3)
s5 = strategy.opentrades.entry_price(4)
s6 = strategy.opentrades.entry_price(5)
s7 = strategy.opentrades.entry_price(6)
s8 = strategy.opentrades.entry_price(7)
s9 = strategy.opentrades.entry_price(8)
c = strategy.position_size,o = strategy.opentrades
ema12_len = input.int(12,"EMA12Length")
ema144_len = input.int(144, "EMA144Length")
ema169_len = input.int(169,"EMA169Length")
ema576_len = input.int(376, "EMA576Length")
ema676_len = input.int(576,"EMA676Length")
ema12 = ta.ema(close,ema12_len)
ema144 = ta.ema(close, ema144_len)
ema169 = ta.ema(close, ema169_len)
ema576 = ta.ema(close, ema576_len)
ema676 = ta.ema(close, ema676_len)
e3 = ta.valuewhen(o ==2 and o[1] == 1 and c > 0,bar_index,0)
e4 = ta.valuewhen(o ==3 and o[1] == 2 and c > 0,bar_index,0)
e5 = ta.valuewhen(o ==4 and o[1] == 3 and c > 0,bar_index,0)
le1 = false
le1 := c <= 0 and ema12 > ema144 and ema144 > ema169 and ema169 > ema576 and ema576 > ema676 and low < ema144 and low[1] > ema144 and close > ema169? true :  close < ema169 or ema12 < ema144 ? false : le1[1]
le11 = false
le11 := le1 and bar_index - ta.valuewhen(low < ema144 and low[1] > ema144,bar_index,0) < 12 ? true : false
le2 = false
le2 := c > 0 and o == 1 and o[1] == 1 and ema12 > ema144 and ema144 > ema169 and ema169 > ema576 and ema576 > ema676 and low < ema144 and low[1] > ema144 and close > ema169? true :  close < ema169 or ema12 < ema144 or o < 1? false : le2[1]
le21 = false
le21 := le2 and bar_index - ta.valuewhen(low < ema144 and low[1] > ema144 and o == 1 and o[1]==1,bar_index,0) < 12 ? true : false
le3 = false
le3 := c > 0 and o == 2 and o[1] == 2 and ema12 > ema144 and ema144 > ema169 and ema169 > ema576 and ema576 > ema676 and low < ema144 and low[1] > ema144 and close > ema169? true :  close < ema169 or ema12 < ema144 or o < 2? false : le3[1]
le31 = false
le31 := le3 and bar_index - e3 > 50 and bar_index - ta.valuewhen(low < ema144 and low[1] > ema144 and o == 2 and o[1]==2,bar_index,0) < 12 ? true : false
le4 = false
le4 := c > 0 and o == 3 and o[1] == 3 and ema12 > ema144 and ema144 > ema169 and ema169 > ema576 and ema576 > ema676 and low < ema144 and low[1] > ema144 and close > ema169? true :  close < ema169 or ema12 < ema144 or o < 3? false : le4[1]
le41 = false
le41 := le4 and bar_index - e4 > 50 and bar_index - ta.valuewhen(low < ema144 and low[1] > ema144 and o == 3 and o[1]==3,bar_index,0) < 12 ? true : false
le5 = false
le5 := c > 0 and o == 4 and o[1] == 4 and ema12 > ema144 and ema144 > ema169 and ema169 > ema576 and ema576 > ema676 and low < ema144 and low[1] > ema144 and close > ema169? true :  close < ema169 or ema12 < ema144 or o < 4? false : le5[1]
le51 = false
le51 := le5 and bar_index - e5 > 50 and bar_index - ta.valuewhen(low < ema144 and low[1] > ema144 and o == 4 and o[1]==4,bar_index,0) < 12 ? true : false
d1 = ta.valuewhen(o == 1 and o[1] == 0 and c > 0,ta.lowest(12),0)
d2 = ta.valuewhen(o == 2 and o[1] == 1 and c > 0,ta.lowest(12),0)
d3 = ta.valuewhen(o == 3 and o[1] == 2 and c > 0,ta.lowest(12),0)
d4 = ta.valuewhen(o == 4 and o[1] == 3 and c > 0,ta.lowest(12),0)
d5 = ta.valuewhen(o == 5 and o[1] == 4 and c > 0,ta.lowest(12),0)
if le11 and close > ema12 and o == 0
    strategy.order("l1",strategy.long,comment="first order")
if c > 0 and o > 0
    strategy.exit("Exit position1","l1",limit = 2*s1- d1,stop= d1,qty_percent = 50)
    strategy.exit("Exit position11","l1",stop= d1)

if le21 and close > ema12 and o == 1
    strategy.order("l2",strategy.long,comment="second order")
if c > 0 and o == 2
    strategy.exit("Exit position2","l2",limit = 2*s2- d2,stop= d2,qty_percent = 50)
    strategy.exit("Exit position21","l2",stop= d2)

if le31 and close > ema12 and o == 2
    strategy.order("l3",strategy.long,comment="third order")
if c > 0 and o == 3
    strategy.exit("Exit position3","l3",limit = 2*s3- d3,stop= d3,qty_percent = 50)
    strategy.exit("Exit position31","l3",stop= d3)

if le41 and close > ema12 and o == 3
    strategy.order("l4",strategy.long,comment="fourth order")
if c > 0 and o == 4 
    strategy.exit("Exit position4","l4",limit = 2*s4- d4,stop= d4,qty_percent = 50)
    strategy.exit("Exit position41","l4",stop= d4)

if le51 and close > ema12 and o == 4
    strategy.order("l5",strategy.long,comment="fifth order")
if c > 0 and o == 5
    strategy.exit("Exit position5","l5",limit = 2*s5- d5,stop= d5,qty_percent = 50)
    strategy.exit("Exit position51","l5",stop= d5)
bgcolor(le2?color.red:na)
if c > 0 and ema12 < ema144
    strategy.close_all("Exit all positions when breaking below the moving average")

//go short
es3 = ta.valuewhen(o ==2 and o[1] == 1 and c < 0,bar_index,0)
es4 = ta.valuewhen(o ==3 and o[1] == 2 and c < 0,bar_index,0)
es5 = ta.valuewhen(o ==4 and o[1] == 3 and c < 0,bar_index,0)
se1 = false
se1 := c >= 0 and ema12 < ema144 and ema144 < ema169 and ema169 < ema576 and ema576 < ema676 and high > ema144 and high[1] < ema144 and close < ema169? true :  close > ema169 or ema12 > ema144 ? false : se1[1]
se11 = false
se11 := se1 and bar_index - ta.valuewhen(high > ema144 and high[1] < ema144,bar_index,0) < 12 ? true : false
se2 = false
se2 := c < 0 and o == 1 and o[1] == 1 and ema12 < ema144 and ema144 < ema169 and ema169 < ema576 and ema576 < ema676 and high > ema144 and high[1] < ema144 and close < ema169? true :  close > ema169 or ema12 > ema144 or o < 1? false : se2[1]
se21 = false
se21 := se2 and bar_index - ta.valuewhen(high > ema144 and high[1] < ema144 and o == 1 and o[1]==1,bar_index,0) < 12 ? true : false
se3 = false
se3 := c < 0 and o == 2 and o[1] == 2 and ema12 < ema144 and ema144 < ema169 and ema169 < ema576 and ema576 < ema676 and high > ema144 and high[1] < ema144 and close < ema169 ? true :  close > ema169 or ema12 > ema144 or o < 2? false : se3[1]
se31 = false
se31 := se3 and bar_index - es3 > 50 and bar_index - ta.valuewhen(high > ema144 and high[1] < ema144 and o == 2 and o[1]==2,bar_index,0) < 12 ? true : false
se4 = false
se4 := c < 0 and o == 3 and o[1] == 3 and ema12 < ema144 and ema144 < ema169 and ema169 < ema576 and ema576 < ema676 and high > ema144 and high[1] < ema144 and close < ema169? true :  close > ema169 or ema12 > ema144 or o < 3? false : se4[1]
se41 = false
se41 := se4 and bar_index - es4 > 50 and bar_index - ta.valuewhen(high > ema144 and high[1] < ema144 and o == 3 and o[1]==3,bar_index,0) < 12 ? true : false
se5 = false
se5 := c < 0 and o == 4 and o[1] == 4 and ema12 < ema144 and ema144 < ema169 and ema169 < ema576 and ema576 < ema676 and high > ema144 and high[1] < ema144 and close < ema169 ? true :  close > ema169 or ema12 > ema144 or o < 4? false : se5[1]
se51 = false
se51 := se5 and bar_index - es5 > 50 and bar_index - ta.valuewhen(high > ema144 and high[1] < ema144 and o == 4 and o[1]==4,bar_index,0) < 12 ? true : false
ds1 = ta.valuewhen(o == 1 and o[1] == 0 and c < 0 ,ta.highest(12),0)
ds2 = ta.valuewhen(o == 2 and o[1] == 1 and c < 0,ta.highest(12),0)
ds3 = ta.valuewhen(o == 3 and o[1] == 2 and c < 0,ta.highest(12),0)
ds4 = ta.valuewhen(o == 4 and o[1] == 3 and c < 0,ta.highest(12),0)
ds5 = ta.valuewhen(o == 5 and o[1] == 4 and c < 0,ta.highest(12),0)
if se11 and close < ema12 and o == 0
    strategy.order("s1",strategy.short,comment="first order")
if c < 0 and o > 0
    strategy.exit("Exit position1","s1",limit = 2*s1- ds1,stop= ds1,qty_percent = 50)
    strategy.exit("Exit position11","s1",stop= ds1)

if se21 and close < ema12 and o == 1
    strategy.order("s2",strategy.short,comment="second order")
if c < 0 and o == 2
    strategy.exit("Exit position2","s2",limit = 2*s2- ds2,stop= ds2,qty_percent = 50)
    strategy.exit("Exit position21","s2",stop= ds2)

if se31 and close < ema12 and o == 2
    strategy.order("s3",strategy.short,comment="third order")
if c < 0 and o == 3
    strategy.exit("Exit position3","s3",limit = 2*s3- ds3,stop= ds3,qty_percent = 50)
    strategy.exit("Exit position31","s3",stop= ds3)

if se41 and close < ema12 and o == 3
    strategy.order("s4",strategy.short,comment="fourth order")
if c < 0 and o == 4 
    strategy.exit("Exit position4","s4",limit = 2*s4- ds4,stop= ds4,qty_percent = 50)
    strategy.exit("Exit position41","s4",stop= ds4)

if se51 and close < ema12 and o == 4
    strategy.order("s5",strategy.short,comment="fifth order")
if c < 0 and o == 5
    strategy.exit("Exit position5","s5",limit = 2*s5- ds5,stop= ds5,qty_percent = 50)
    strategy.exit("Exit position51","s5",stop= ds5)
bgcolor(se1?color.red:na)
if c < 0 and ema12 > ema144
    strategy.close_all("Exit all positions when breaking below the moving average")
kaiguan = input.bool(true,"Moving Average Switch")
plot(ema12,force_overlay=true)
plot(ema144, "EMA144", color=color.new(#008000, 0),force_overlay=true)
plot(ema169, "EMA169", color=color.red,force_overlay=true)
plot(kaiguan?ema576:na,color=color.yellow,force_overlay=true)
plot(kaiguan?ema676:na,color=color.yellow,force_overlay=true)
//plotshape(series=entrySignal,title="Buy Signal",location=location.belowbar,color=color.new(color.green, 0),style=shape.labelup,text="BUY",textcolor=color.new(color.white, 0))

```

> Detail

https://www.fmz.com/strategy/483943

> Last Modified

2025-02-27 10:20:18
