
> Name

Dual-Moving-Average-Range-Breakout-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1145afbd4a5050e5992.png)
 
## Overview
This strategy identifies trend breakouts by calculating moving averages over different timeframes. It allows low-risk trend following.   

## Strategy Logic
Go long when the 10-day EMA crosses above the 200-day EMA and the 20-day EMA crosses above the 50-day EMA. Go short when the 10-day EMA crosses below the 200-day EMA and the 20-day EMA crosses below the 50-day EMA. The dual moving average design filters false breakouts effectively.  

The strategy first calculates four exponential moving averages (EMAs) over the 10-day, 20-day, 50-day and 200-day periods. The 10-day EMA represents short-term trend, 20-day intermediate, 50-day medium-term and 200-day long-term trend. When the shorter EMA crosses the longer EMA, it signals a potential trend reversal. However, using just one EMA crossover produces false signals easily.  

To improve reliability, the strategy applies two layers of filtering: the 10/200 EMA cross gauges long/short-term trend shifts while the 20/50 EMA cross gauges medium/intermediate-term shifts. Trades are triggered only when both EMA pairs align in the same direction.   

The dual EMA filtering significantly reduces false signals, generating more reliable trade entries. 

## Advantages
1. Dual EMA filtering lowers false signals substantially 
2. Multiple timeframes offer robustness 
3. Simple parameterization facilitates usage

## Risks
1. Strong trend-following but misses reversals  
2. Potentially large stops when trends shift
3. Insufficient history disadvantages new/exotic assets 

Improvements include relaxing breakout thresholds, adding volume confirmation and optimizing parameters.  

## Enhancement Opportunities
1. Add volume confirmation. Volume verifies if breakout is real or on low activity.  
2. Incorporate additional indicators like MACD, KDJ for greater stability. 
3. Optimize parameters like 10/20-day EMA durations for changing markets.  

In summary, the dual moving average core supplemented with optimization, volume and more indicators can build a steady trend tracking system.  

## Conclusion
A simple but practical trend following strategy. The dual EMA core filters false breakouts reliably for quality signals. Easy parameterization also facilitates adoption. Further improvements in risk management and optimization can boost performance. Overall an accessible introductory quant strategy underpinned by simplicity.




> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-12 00:00:00
end: 2023-12-13 02:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("Advancing Our Basic Strategy", overlay=true)

ema10 = ema(close, 10)
ema20 = ema(close, 20)
ema50 = ema(close, 50)
ema200 = ema(close, 200)

long = ema10 > ema200 and ema20 > ema50
short = ema10 < ema200 and ema20 < ema50
longcondition = long and long[10] and not long[11]
shortcondition = short and short[10] and not short[11]

closelong = ema10 < ema200 or ema20 < ema50 and not long[11]
closeshort = ema10 > ema200 or ema20 > ema50 and not short[11]

plot(ema10, title="10", color=green, linewidth=2)
plot(ema20, title="20", color=red, linewidth=3)
plot(ema50, title="50", color=purple, linewidth=2)
plot(ema200, title="200", color=blue, linewidth=3)

testPeriodStart = timestamp(2018,8,1,0,0)
testPeriodStop = timestamp(2038,8,30,0,0)

if time >= testPeriodStart and time <= testPeriodStop
    strategy.entry("Long", strategy.long, 1, when=longcondition)
    strategy.entry("Short", strategy.short, 1, when=shortcondition)
    

strategy.close("Long", when = closelong)
strategy.close("Short", when = closeshort)
```

> Detail

https://www.fmz.com/strategy/435955

> Last Modified

2023-12-20 13:59:38
