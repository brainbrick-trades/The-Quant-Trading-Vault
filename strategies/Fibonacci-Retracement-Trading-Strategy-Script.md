
> Name

Fibonacci-Retracement-Trading-Strategy-Script

> Author

Zer3192



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|50|Fibonacci cycle length|
|v_input_2|0.236|Fibonacci levels1|
|v_input_3|0.382|Fibonacci levels2|
|v_input_4|0.618|Fibonacci levels3|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-10-27 00:00:00
end: 2023-11-02 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Fibonacci retracement trading strategy", overlay=true, initial_capital=10000)

// Parameters
length = input(50, title="Fibonacci cycle length")
fib1 = input(0.236, title="Fibonacci levels1")
fib2 = input(0.382, title="Fibonacci levels2")
fib3 = input(0.618, title="Fibonacci levels3")

// Calculate Fibonacci levels
highLevel = ta.highest(high, length)
lowLevel = ta.lowest(low, length)
range1 = highLevel - lowLevel
fibLevel1 = highLevel - range1 * fib1
fibLevel2 = highLevel - range1 * fib2
fibLevel3 = highLevel - range1 * fib3

// condition
longCondition = ta.crossover(close, fibLevel3)
shortCondition = ta.crossunder(close, fibLevel1)

// Place Order
strategy.entry("Buy", strategy.long, when=longCondition)
strategy.close("Buy", when=shortCondition)

// Chart Marker
plot(fibLevel1, title="Fib 0.236", color=color.red)
plot(fibLevel2, title="Fib 0.382", color=color.orange)
plot(fibLevel3, title="Fib 0.618", color=color.green)

```

> Detail

https://www.fmz.com/strategy/430984

> Last Modified

2023-11-03 15:30:58
