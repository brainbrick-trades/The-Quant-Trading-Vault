
> Name

Intraday-Trading-Strategy-for-Stocks-Based-on-Renko-Low-Point-Retracement

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/137b66f89e4219e3859.png)
 
### Overview

This strategy mainly utilizes the intraday renko low point retracement characteristics of stocks to determine the new trend direction, and thus establishes an intraday trading strategy. When there is an obvious pullback of the renko intraday low point, it is judged as a new bullish signal and a long position will be taken. When there is a significant decline in the renko closing price, it is regarded as a bearish signal and existing position will be closed.

### Strategy Logic

The main criteria of this strategy are: the intraday renko low point retracement exceeds the upper rail and lower rail. The upper rail is calculated as the 20-day average + 2 standard deviations of the renko intraday low point retracement over the past 20 days; The lower rail is calculated as 85% of the highest point of the renko intraday low point retracement over the past 50 days. When the renko intraday low point retracement exceeds the upper rail or lower rail, it is regarded as a buy signal, otherwise the position will be cleared. The specific process is as follows:

1. Calculate the standard deviation DesviaccionTipica of the difference between the highest price and the lowest price of the most recent 22 renko bars over the past 20 days 
2. Calculate the 20-day moving average Media of the difference between the highest price and the lowest price of the most recent 22 renko bars
3. Upper rail Rango11 = Media + DesviaccionTipica * 2  
4. Lower rail Rango22 = highest point of the most recent 50 renko bars * 0.85
5. When today's renko satisfies low/highest(low,22)>Rango11 or Rango22, go long; when today's renko satisfies close<open, close position

The above is the main judgment rules and trading logic of this strategy.  

### Advantage Analysis 

1. Utilizing the noise filtering capability of renko, renko is used as an assistant judgment to effectively filter out false signals in range-bound markets
2. Judging the trend based on renko intraday low point retracement features avoids the misjudgment caused by using a single moving average 
3. The double rail judgment rules can determine the trend direction more accurately  
4. The strategy judgment rules are simple and easy to understand and implement
5. The strategy is easy to parameter tuning and optimization, which can significantly improve strategy performance

### Risk Analysis

1. The repainting characteristics of renko may have some impact on actual trading
2. Improper settings of double rail distances may miss or misjudge signals  
3. The strategy uses a single indicator for judgment, which may miss important signals provided by other indicators  
4. No stop loss setting may lead to greater losses  

Risk Mitigations:
1. Properly relax double rail parameters to ensure more signals are captured  
2. Incorporate judgments of more indicators such as moving averages and energy indicators to ensure accurate judgments 
3. Add moving stop loss to control risks

### Optimization Directions

1. Parameter Tuning, optimize double rail parameter settings  
2. Incorporate judgments of more technical indicators  
3. Add stop loss mechanism  
4. Expand trading varieties to increase trading opportunities  

### Summary  

The overall idea of this strategy is clear and easy to implement. It utilizes the renko intraday low point retracement to determine the new trend direction. The advantages of this strategy are that it uses renko characteristics for filtration to avoid misjudgment, and adopts double rail judgment to improve accuracy. At the same time, there are also some rooms for improvement of this strategy. The keys are parameter optimization, stop loss setting, and integration of multiple indicator judgments. In general, this is an easy to understand and effective intraday trading strategy for stocks.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|false|Rango 1|
|v_input_2|false|Rango 2|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// @version=2
strategy("Renko Stock Daily")


Rango1 = input(false, title="Rango 1")
Rango2 = input(false, title="Rango 2")

Situacion = ((highest(close, 22)-low)/(highest(close, 22)))*100

DesviaccionTipica = 2 * stdev(Situacion, 20)
Media = sma(Situacion, 20)

Rango11 = Media + DesviaccionTipica

Rango22 = (highest(Situacion, 50)) * 0.85


advertir = Situacion >= Rango11 or Situacion >= Rango22 ? green : red    



if (Situacion[1] >= Rango11[1] or Situacion[1] >= Rango22[1]) and (Situacion[0] < Rango11[0] and Situacion[0] < Rango22[0])and (close>open)
    strategy.entry("Entrar", strategy.long,comment= "Entrar",when=strategy.position_size <= 0)


strategy.close_all(when=close<open)



plot(Rango1 and Rango22 ? Rango22 : na, title="Rango22", style=line, linewidth=4, color=orange)
plot(Situacion, title="Rengo Stock Daily", style=histogram, linewidth = 4, color=advertir)
plot(Rango2 and Rango11 ? Rango11 : na, title="Upper Band", style=line, linewidth = 3, color=aqua)


```

> Detail

https://www.fmz.com/strategy/440507

> Last Modified

2024-01-31 10:53:17
