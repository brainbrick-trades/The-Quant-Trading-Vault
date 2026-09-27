
> Name

Bull-and-Bear-Power-Moving-Average-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/ac2c04fb85b614ee58.png)
 
## Overview

This strategy was developed by Dr. Alexander Elder based on his theory of bull and bear power moving averages to measure buying and selling pressure in the market. It is commonly used together with the Triple Screen trading system but can also be used on its own. Dr. Elder uses a 13-day exponential moving average (EMA) to reflect the market consensus of value. Bull power reflects the ability of buyers to drive prices above the consensus of value. Bear power reflects the sellers' ability to drive prices below the average consensus of value.  

Bull power is calculated by subtracting the 13-day EMA from the day's high. Bear Power subtracts the 13-day EMA from the day's low.  

## Strategy Logic

This strategy is based on Dr. Alexander Elder's theory of bull and bear power. It judges market trends and power by calculating bull and bear power indicators. Specifically, the bull power indicator reflects the power of buyers, which is calculated by subtracting the 13-day EMA from the highest price. The bear power indicator reflects the power of sellers, which is calculated by subtracting the 13-day EMA from the lowest price. When the bull power drops to a certain threshold, a short signal is generated. When the bear power rises to a certain threshold, a long signal is generated. Thus, we can judge the market trend and beat the market by comparing the relative strength of buying and selling power.

In the code, we use highs, lows and 13-day EMA to calculate the bull and bear power indicators. Set trigger thresholds so that corresponding long or short positions are opened when the indicators are triggered. At the same time, set stop loss and take profit logic to manage positions. Overall, this strategy compares the relative power of buyers and sellers to determine the strength of market trends for trading.

## Advantage Analysis 

The advantages of this strategy include:

1. Effective in judging market trends and backtesting using buying and selling power  
2. Clear buy and sell signals that are easy to judge
3. Reliable stop loss mechanism to control risk 
4. Works even better when combined with the Triple Screen trading system

## Risk Analysis

Some risks of this strategy include:

1. Subjective parameter settings that need adjusting for different markets
2. Bull and bear power indicators may produce misleading signals
3. Improper stop loss placement may increase losses
4. Performance depends on trading instruments and timeframes

Countermeasures:

1. Optimize parameters for different markets 
2. Add filters using other indicators 
3. Optimize stop loss logic to strictly control risk
4. Select suitable trading instruments and timeframes

## Optimization Directions

This strategy can be optimized in the following aspects:

1. Optimize moving average parameters for different timeframes  
2. Add other indicators like MACD to filter signals
3. Optimize stop loss and take profit logic, such as trail stop loss
4. Use machine learning to automatically optimize parameters  
5. Incorporate deep learning to predict buy/sell signals  

In summary, this strategy has much room for optimization in aspects like parameters, signals, risk control etc. to make it more robust and reliable.  

## Conclusion  

This strategy judges market trends and power using the bull and bear power indicators developed by Dr. Elder based on buying/selling power theory. The signal rules are relatively simple and clear. Advantages include judging trends via power and controlling risk through stop loss. It also has risks like subjective parameters and misleading signals. We can improve stability and profitability through optimizing parameters, adding signal filters and strict stop loss. This strategy suits aggressive quant traders.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_float_1|7|Take Profit %|
|v_input_float_2|7|Stop Loss %|
|v_input_int_1|14|Length|
|v_input_float_3|-200|Trigger|
|v_input_bool_1|true|Trade reverse|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-12 00:00:00
end: 2023-12-19 00:00:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version = 5
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 06/10/2022
// Developed by Dr Alexander Elder, the Elder-ray indicator measures buying 
// and selling pressure in the market. The Elder-ray is often used as part 
// of the Triple Screen trading system but may also be used on its own.
// Dr Elder uses a 13-day exponential moving average (EMA) to indicate the 
// market consensus of value. Bull Power measures the ability of buyers to 
// drive prices above the consensus of value. Bear Power reflects the ability 
// of sellers to drive prices below the average consensus of value.
// Bull Power is calculated by subtracting the 13-day EMA from the day's High. 
// Bear power subtracts the 13-day EMA from the day's Low.
// WARNING:
// - For purpose educate only
// - This script to change bars colors. 
////////////////////////////////////////////////////////////
strategy(title="Elder Ray (Bull Power) TP and SL", shorttitle = "Bull Power", overlay = true)
Profit = input.float(7, title='Take Profit %', minval=0.01)
Stop = input.float(7, title='Stop Loss %', minval=0.01)
Length = input.int(14, minval=1)
Trigger = input.float(-200)
reverse = input.bool(true, title="Trade reverse")
xPrice = close
xMA = ta.ema(xPrice,Length)
var DayHigh = high
DayHigh := dayofmonth != dayofmonth[1]? high: math.max(high, nz(DayHigh[1]))
nRes = DayHigh - xMA
pos = 0
pos := nRes < Trigger ? 1:  0 
possig = reverse and pos == 1 ? -1 :
          reverse and pos == -1 ? 1 : pos	   
if (possig == 1) and strategy.position_size == 0
    strategy.entry('Long', strategy.long, comment='Market Long')
    strategy.exit("ExitLong", 'Long', stop=close - close * Stop / 100 , limit = close + close * Profit / 100 , qty_percent = 100)  
if (possig == -1) and strategy.position_size == 0
    strategy.entry('Short', strategy.short, comment='Market Long')
    strategy.exit("ExitShort", 'Short', stop=close + close * Stop / 100 , limit = close - close * Profit / 100 , qty_percent = 100)  
barcolor(strategy.position_size == -1 ? color.red: strategy.position_size == 1 ? color.green : color.blue )
```

> Detail

https://www.fmz.com/strategy/435993

> Last Modified

2023-12-20 16:30:02
