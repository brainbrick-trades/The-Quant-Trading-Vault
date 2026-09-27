
> Name

Double-7-Days-Breakout-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/7e386c5da6e9c5261e.png)
 
### Overview  

The Double 7 Days Breakout Strategy is a very simple short-term trading strategy. It has only 3 trading rules:

1. Price must be above the 200-day Simple Moving Average  
2. Go long when price closes below the lowest price of the past 7 days
3. Close position when price closes above the highest price of the past 7 days

Although the rules are very simple, this strategy performs very well in some stocks and time periods, even outperforming many RSI strategies.

### Strategy Principles

The Double 7 Days Breakout Strategy trades based on price supports and resistances. When price breaks below the lowest price of the past 7 days, it indicates the price may enter an adjustment period and it is time to go long. When price breaks above the highest price of the past 7 days, it indicates the momentum may strengthen and it is time to close position and take profit.

This is a typical short-term trading strategy. It judges the price action over the past 7 days and utilizes ultra short-term breakout signals to enter positions. Meanwhile, it also requires the price to be above the 200-day Moving Average to avoid trading in long-term downtrends.

### Advantage Analysis 

The biggest advantage of the Double 7 Days Breakout Strategy is that it is simple and easy to implement. There are only 3 trading rules which makes it very straightforward to follow. Also due to the very short lookback period, trading frequency is high making it suitable for short-term trading.

In addition, the strategy effectively utilizes price supports and resistances to trade. Such breakout signals tend to be more reliable with higher winning rates. This is also why this strategy has good performance.

### Risk Analysis

As a short-term trading strategy, the main risks come from two aspects:  

1. Wrong signal risk. Wrong breakouts will produce losses.

2. Systemic market risk. When market has sharp corrections, correlations between stocks increase. Since this strategy may hold positions in multiple stocks, it faces larger market risk.

To mitigate these risks, parameters can be adjusted to shorten holding period or add filters with other indicators. Also reduce position sizes when market fluctuation increases.

### Optimization Directions  

There is room for further optimization of the Double 7 Days Breakout Strategy:

1. Test different parameters for long-term moving average to find more suitable ones.

2. Test different periods for the breakout to optimize the short-term indicator.  

3. Add stop loss mechanism to further control single trade loss.

4. Combine with other indicators to filter signals and improve accuracy.

Through optimizing parameters and strategy structure, there is potential to further improve stability and efficiency of the strategy.

### Conclusion

The Double 7 Days Breakout Strategy is a simple yet efficient short-term trading strategy. It trades based on support/resistance breakouts generating high frequency signals suitable for short-term trading. Also by requiring price to be above long-term moving average, it effectively avoids systemic risks in long-term corrections. With further optimization on parameters and modules, there is potential for even better performance.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|7|Quantity of day low|
|v_input_2|7|Quantity of day high|
|v_input_3|2009|Backtest Start Year|
|v_input_4|true|Backtest Start Month|
|v_input_5|2|Backtest Start Day|
|v_input_6|2020|Backtest Stop Year|
|v_input_7|12|Backtest Stop Month|
|v_input_8|30|Backtest Stop Day|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Double 7's Strategy", overlay=true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100)

value1=input(7, title="Quantity of day low")
value2=input(7, title="Quantity of day high")
entry=lowest(close[1],value1)
exit=highest(close[1],value2)


mma200=sma(close,200)

// Test Period
testStartYear = input(2009, "Backtest Start Year")
testStartMonth = input(1, "Backtest Start Month")
testStartDay = input(2, "Backtest Start Day")
testPeriodStart = timestamp(testStartYear,testStartMonth,testStartDay,0,0)

testStopYear = input(2020, "Backtest Stop Year")
testStopMonth = input(12, "Backtest Stop Month")
testStopDay = input(30, "Backtest Stop Day")
testPeriodStop = timestamp(testStopYear,testStopMonth,testStopDay,0,0)

testPeriod() => true

if testPeriod()
    if (close>mma200) and (close<entry)
        strategy.entry("RsiLE", strategy.long , comment="Open")

    if (close>exit)
        strategy.close_all()

```

> Detail

https://www.fmz.com/strategy/440451

> Last Modified

2024-01-30 16:49:01
