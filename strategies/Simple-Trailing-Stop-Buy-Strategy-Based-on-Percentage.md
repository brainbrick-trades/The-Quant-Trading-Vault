
> Name

Simple-Trailing-Stop-Buy-Strategy-Based-on-Percentage

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/12868ce7bcb9d7da998.png)
 
## Overview

This strategy implements a simple percentage-based trailing stop and trailing buy. By experimenting with different percentage combinations across timeframes and charts, the strategy parameters can be optimized.  

## Strategy Logic

The strategy mainly uses two metrics to achieve trailing stop loss and trailing buy:

1. Trailing Stop Line (TSL): Calculated based on recent N bars of closing prices and stop loss offset percentage set by user. Triggers stop loss when price falls below this line.

2. Trailing Buy Line (TBL): Calculated based on recent N bars of highest prices and buy offset percentage set by user. Triggers buy when price rises above this line.


By comparing price with these two metrics, the stop loss and trailing buy rules are implemented.

## Advantages

The advantages of this strategy are:

1. Simple and intuitive, easy to understand and implement.

2. Flexible stop loss and trailing buy through parameter adjustment.

3. Applicable across markets and timeframes. 

4. Allows trend following and timely stop loss.

## Risks

The risks of this strategy include:

1. Improper parameter setting may cause over-aggressive stop loss or buys.

2. Frequent trading and slippage in ranging markets.

3. Requires parameter optimization for different market characteristics.

## Enhancement Opportunities 

The strategy can be enhanced through:

1. Adaptive algorithms to auto optimize stop and buy parameters.

2. Addition of position sizing and risk management modules. 

3. Incorporation of other indicators to gauge overall trend to avoid whipsaws.


## Conclusion

In summary, this is a very simple and intuitive trend following strategy. With parameter tuning it can be adapted across markets. Further incorporation of adaptive algorithms and additional filters can improve robustness. Overall it provides a basic yet effective framework for quantitative trading.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|1.5|Stop Offset %|
|v_input_2|1.9|Trailing Buy Offset %|
|v_input_3|6|Use last x bars for calculation|
|v_input_4_close|0|Source Trailing Stop calculation: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_5_close|0|Source Trailing Buy calculation: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_6_low|0|Source Stop Trigger: low|high|close|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_7_high|0|Source Buy Trigger: high|close|low|open|hl2|hlc3|hlcc4|ohlc4|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-01-12 00:00:00
end: 2024-01-18 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
//Developed from ©Finnbo code
strategy("Simple Trailing Buy & Stop Strategy", overlay=true)
offset = input(defval=1.5, title="Stop Offset %", type=float, minval=0.1, maxval=100, step=0.1)
buyoffset = input(defval=1.9, title="Trailing Buy Offset %", type=float, minval=0.1, maxval=100, step=0.1)

sumbars = input(defval=6, title="Use last x bars for calculation",  minval=1)
srcts = input(title="Source Trailing Stop calculation",  defval=close)
srctb = input(title="Source Trailing Buy calculation",  defval=close)
srctrigger = input(title="Source Stop Trigger",  defval=low)
srctriggerbuy = input(title="Source Buy Trigger",  defval=high)
tsl = rma(srcts, sumbars)*(1-(offset/100))// = (sum(srcts,sumbars)/sumbars)*(1-(offset/100))
tbuy = rma(srctb, sumbars)*(1+(buyoffset/100))
plot(tsl, color=(srctrigger<tsl)?red:green)
plot(tbuy, color=(srctriggerbuy>tbuy)?red:green)
//plotshape(crossunder(srctrigger,tsl), text="Long Stop", style=shape.circle, color=red)
alertcondition(crossunder(srctrigger,tsl), "Long Stop alert", "SELL")
//plotshape(crossover(srctriggerbuy,tbuy), text="Long", style=shape.circle, color=green)
alertcondition(crossover(srctriggerbuy,tbuy), "Long alert", "BUY")

longCondition =  crossover(srctriggerbuy,tbuy)
if (longCondition)
    strategy.entry("Long", strategy.long)
closeCondition = crossunder(srctrigger,tsl)
if (closeCondition)
    strategy.close("Long")

```

> Detail

https://www.fmz.com/strategy/439349

> Last Modified

2024-01-19 14:30:59
