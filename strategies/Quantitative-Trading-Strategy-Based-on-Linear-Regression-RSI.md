
> Name

Quantitative-Trading-Strategy-Based-on-Linear-Regression-RSI

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1c1ff16aca3e389119a.png)
 
## Overview  

This strategy is designed based on the linear regression RSI indicator. It generates buy and sell signals by calculating the crossover between the linear regression RSI and EMA. The strategy also provides two options for the buy logic that can be selected as needed.  

## Strategy Logic  

The strategy first calculates a 200-period linear regression, then computes a 21-period RSI based on the linear regression result. After that, a 50-period EMA is calculated. When the RSI crosses above the EMA, a buy signal is generated. When the RSI crosses below the EMA, a sell signal is triggered to close the position.

The strategy offers two types of buy logic:  

1. Buy when RSI crosses above EMA
2. Buy when RSI is above EMA and also above the overbought line

The appropriate buy logic can be selected based on market conditions.

## Advantage Analysis   

This strategy combines the strengths of both linear regression RSI and EMA, which effectively filters out some price noise and generates more reliable trading signals.  

The linear regression RSI better captures the trend, and the EMA helps identify turning points. The combination of the two can find mean reversion opportunities within trends.  

The strategy provides two optional buy logics for more flexibility to adapt to different market stages. For example, the first logic can be used in strong trends, while the second logic fits better for ranging markets.

## Risk Analysis  

The main risk of this strategy lies in the potential change of relationship between the RSI and EMA, which may lead to incorrect trade signals.  

In addition, the lagging nature of RSI and EMA as indicators can also cause certain delays in entries and exits, failing to perfectly capture turning points. This introduces some degree of practical risks.

To mitigate the risks, parameters like the lengths of RSI and EMA may be optimized for better coordination between the two. Also, proper position sizing is necessary to limit losses on single trades.

## Improvement Directions

The strategy can be improved from the following aspects:

1. Optimize lengths of linear regression RSI and EMA to find best parameter combinations  
2. Add other indicators like MACD, Bollinger Bands etc. for signal quality enhancement
3. Incorporate volatility metrics to adjust position sizing  
4. Utilize machine learning techniques to automatically optimize parameters  

## Conclusion  

This strategy designs a mean reversion strategy based on linear regression RSI and EMA, identifying reversal opportunities within ranges by looking at RSI-EMA crosses. It also provides two optional buy logics for flexibility to adapt to varying markets. Overall, by combining multiple indicators, the strategy can effectively discover reversal chances. With parameter tuning and additional filters, it has the potential for better performance.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|2017|Start Year|
|v_input_2|12|Month|
|v_input_3|17|Day|
|v_input_4|9999|End Year|
|v_input_5|true|Month|
|v_input_6|true|Day|
|v_input_7|200|LR length|
|v_input_8|21|RSI length|
|v_input_9|50|EMA|
|v_input_10|50|overBought|
|v_input_11|50|overSold|
|v_input_12|true|Use first logic?|
|v_input_13|false|Use second logic?|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-01-17 00:00:00
end: 2024-01-23 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Linear RSI")

startP = timestamp(input(2017, "Start Year"), input(12, "Month"), input(17, "Day"), 0, 0)
end   = timestamp(input(9999, "End Year"),   input(1, "Month"),   input(1, "Day"),   0, 0)
_testPeriod() => true

//inputs
length = input(defval=200, minval=1, title="LR length")
length2 = input(defval=21, minval=1, title="RSI length")
ema_fast = input(defval=50, minval=1, title="EMA")
lag = 0

overBought = input(50)
overSold = input(50)


//rsi
src = close
Lr = linreg(src, length, lag)
rsi = rsi(Lr, length2)
ema = ema(rsi, ema_fast)

plot(rsi, color = rsi > overBought ? color.green : rsi < overSold ? color.red : color.silver)
plot(overBought, color=color.purple)
plot(overSold, color=color.purple)
plot(ema, color=color.blue)

first_type = input(true, title="Use first logic?")
second_type =  input(false, title="Use second logic?")

long_condition = (first_type ? crossover(rsi, ema) and _testPeriod() : false) or (second_type ? rsi > ema and rsi > overBought and _testPeriod() : false)
strategy.entry('BUY', strategy.long, when=long_condition)  
 
short_condition = crossunder(rsi, ema)
strategy.close('BUY', when=short_condition)
```

> Detail

https://www.fmz.com/strategy/439839

> Last Modified

2024-01-24 11:35:19
