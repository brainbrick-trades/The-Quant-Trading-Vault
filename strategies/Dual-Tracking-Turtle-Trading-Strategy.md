
> Name

Dual-Tracking-Turtle-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/16dc7b218868e2f7d7e.png)
 
### Overview

This strategy utilizes two tracking stop loss points based on the turtle trading rules to limit losses, while setting different parameters to filter out market noise and enter on more pronounced trends.

### Strategy Logic  

The strategy primarily relies on two tracking stop loss points, long_1 and long_2, to determine entry signals. Long_1 tracks the longer term trend while long_2 tracks the shorter term. Profit1 and profit2 act as the stop loss points.   

If price is above long_1, the market is in a longer term uptrend. If price then drops below long_2, it indicates a short term pullback providing good entry opportunity to go long. If price is below long_1, there is no confirmed longer term trend. But if price then surpasses long_2, it signals a short term bounce and can also take long position.

After entering, two tracking stop losses stoploss1 and stoploss2 are set and compared with profit1 and profit2 to take the maximum value, in order to lock in profits.

### Advantage Analysis

- Dual tracking stop loss effectively controls risks and locks in profits
- Combining both long term and short term indicators filters out some noise and enters on more pronounced trends  
- Flexibility to adjust conservatism of strategy by tuning parameters

### Risk Analysis  

- Strategy is conservative and could miss some opportunities 
- Improper stop loss setting may prematurely exit  
- Less trades so single losing trade impact could be big

Can make strategy more aggressive by adjusting long and profit parameters for more trades. Also optimize stop loss algorithms for adaptive adjustments.

### Optimization Directions   

- Find optimal parameter combinations for long and profit
- Experiment with zigzag or shadow stop losses to reduce unnecessary stops
- Add more entry filters to detect stronger established trends 
- Incorporate volume indicators to catch true breakouts 

### Summary

This is an overall conservative strategy suited for investors seeking steady growth. By tuning parameters and optimizing stop loss algorithms, aggression can be increased. Adding mechanisms to filter out market noise is also a direction for further optimizations.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|55|entry_1|
|v_input_2|20|profit_1|
|v_input_3|20|entry_2|
|v_input_4|10|profit_2|
|v_input_5|true|stop_1|
|v_input_6|2|stop_2|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-19 00:00:00
end: 2023-12-19 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Turtle Project",overlay= true)
//-----------------------------------------------------------
entry_1 =  input(55) 
profit_1 =  input(20)             

long_1 = float(na)                                                             
long_1:= if high[entry_1] >= highest(high,entry_1)                   
    high[entry_1]                                                            
else                                                                              
    long_1[1]                                                                   


profit1 = float(na)                                                            
profit1:= if low[profit_1] <= lowest(low,profit_1)                   
    low[profit_1]                                                            
else                                                                            
    profit1[1]                      
//-----------------------------------------------------------
entry_2 =  input(20) 
profit_2 =  input(10)             

long_2 = float(na)                                                             
long_2:= if high[entry_2] >= highest(high,entry_2)                   
    high[entry_2]                                                            
else                                                                              
    long_2[1]                                                                   


profit2 = float(na)                                                            
profit2:= if low[profit_2] <= lowest(low,profit_2)                   
    low[profit_2]                                                            
else                                                                           
    profit2[1]                      
//------------------------------------------------------------
stoploss_1= lowest(low,1) < long_1 and highest(high,1) > long_1
stoploss_2= lowest(low,1) < long_2 and highest(high,1) > long_2 

stop_1 = input(1)/100
stop_2 = input(2)/100

plotchar(stoploss_1, "high1", "▲",location.top,color=color.red )
plotchar(stoploss_2, "high2", "▲",location.top,color=color.blue)


//------------------------------------------------------------
if strategy.position_size == 0
    if low < long_1
        if high < long_1 
            strategy.entry("longlong_4",strategy.long, stop=long_1)

if strategy.position_size == 0    
    if low > long_1
        if high < long_2 
            strategy.entry("longlong_3",strategy.long, stop=long_2)

stoploss1 = float(na)
stoploss1:= stoploss_1 ? strategy.position_avg_price * (1 - stop_1) : stoploss1[1]
stoploss__1 = max(stoploss1,profit1)

if high > long_1 and strategy.position_size > 0
    strategy.exit("exit_1 ","longlong_4",stop=stoploss__1)

stoploss2 = float(na)
stoploss2:= stoploss_2 ? strategy.position_avg_price * (1 - stop_2) : stoploss2[1]
stoploss__2 = max(stoploss2,profit2)

if high > long_2 and strategy.position_size > 0
    strategy.exit("exit_2 ","longlong_3",stop=stoploss__2)
//--------------------------------------------------------------
plot(long_1,color=color.red ,linewidth=3)
plot(long_2,color=color.blue,linewidth=3)

plot(profit1,color=color.red,   linewidth=1)
plot(profit2,color=color.blue,  linewidth=1)

//plot(stoploss__1,style=plot.style_circles, color=color.yellow) 
//plot(stoploss__2,style=plot.style_circles, color=color.yellow) 

plot(stoploss1,style=plot.style_circles, color=color.blue) 
plot(stoploss2,style=plot.style_circles, color=color.red) 
//--------------------------------------------------------------
```

> Detail

https://www.fmz.com/strategy/435949

> Last Modified

2023-12-20 13:37:31
