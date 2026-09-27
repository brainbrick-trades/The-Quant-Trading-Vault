
> Name

Dual-EMA-Crossover-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1889edd98f9a1e91cc2.png)




## Overview

The double EMA breakout trading strategy is a trend following strategy that uses two EMA moving averages of different periods to judge buying and selling signals. This strategy also combines additional EMA indicators to filter trading signals, which can obtain better entry opportunities in trending markets.

## Principle

This strategy uses the golden cross of the fast EMA (9 periods) and the slow EMA (21 periods) to determine the timing of buying and selling. When the fast line crosses the slow line, a buy signal is generated, and when the fast line crosses below the slow line, a sell signal is generated. In order to filter out false signals, the strategy also introduces an auxiliary EMA (5 periods) and two other EMAs (1 period, 4 periods). Only when a golden cross occurs on the fast and slow lines, the auxiliary EMA is between the fast and slow lines, and the 1-period EMA is higher than the 4-period EMA, will the real trading signal be triggered. 

When the trading signal is triggered, the strategy will set the stop loss and take profit levels based on the ATR value. TP1 is 6 times of ATR and is used to obtain part of the profits at a faster speed. If the price does not trigger TP1, when the fast EMA crosses the auxiliary EMA again, the position will be closed directly and TP2 take profit will be realized.

## Advantage

- Use double EMA combinations to filter false signals and improve trading signal quality
- The auxiliary EMA indicator can further verify trend direction and reduce the risk of contrarian operations
- Dual take-profit design allows for quick profits and sustainable trend tracking for profit
- ATRDynamic stop-loss and take-profit can be adjusted according to market volatility to reduce risk

## Risks and Optimization

- EMAIndicators are prone to curve fitting, trading signals may lag
- Short-period EMA combinations may produce more noise trading signals
- Short-term operations are easily affected by unexpected events, stop-loss risk is high

Optimization Direction:

- Test multiple EMA parameter combinations to find better parameters
- Add other indicator verification, such as trading volume, volatility, etc.
- Appropriately relax the stop loss range and reduce the probability of the stop loss being triggered.
- Optimize the ratio of double take-profit settings to balance profit speed and capital utilization efficiency

## Summary

The double EMA breakout trading strategy uses the intersection of two EMAs to determine the trend, supplemented by multiple EMA filtering and ATR dynamic take-profit and stop-loss, which can effectively track the trend and make profits. However, issues such as EMA curve fitting and stop loss risk need to be paid attention to. Through parameter optimization, risk management and other measures, more stable trading performance can be obtained. This strategy is suitable for traders with a certain foundation to use in trending markets to obtain higher capital utilization efficiency.




## Overview

The dual EMA crossover trading strategy utilizes two EMA lines of different periods to generate buy and sell signals by identifying trend direction. It also incorporates additional EMA indicators for signal filtering, allowing better entry timing in trending markets. 

## Principles

The strategy uses a fast EMA line (9 periods) and a slow EMA line (21 periods) to determine entries. A golden cross where the fast EMA crosses above the slow EMA generates a buy signal, while a death cross with the fast EMA crossing below the slow EMA produces a sell signal. To filter out false signals, the strategy also employs an auxiliary EMA (5 periods) and two more EMAs (1 period, 4 periods). A real trading signal is only triggered when the fast and slow EMAs cross while the auxiliary EMA is between the two, and the 1-period EMA is above the 4-period EMA.

Once a trading signal is triggered, the strategy utilizes ATR values to set stop loss and take profit levels. TP1 is set at 6 x ATR for faster profit taking. If price doesn't hit TP1, the strategy will close the position directly when the fast EMA crosses back over the auxiliary EMA, realizing TP2.

## Advantages

- Dual EMA design filters false signals and improves signal quality 
- Auxiliary EMA adds trend direction verification, reducing reverse trade risks
- Dual take profit allows fast profit and sustained trend following  
- Dynamic ATR stop loss/take profit adjusts to market volatility

## Risks and Improvements 

- EMAs can lag prices and generate late signals 
- Shorter EMA combos may produce more noise
- Tighter stops face larger sudden event risks

Improvement directions:

- Test multiple EMA combos for better parameters
- Add other confirmation indicators like volume, volatility etc.  
- Widen stop loss to lower stop out odds
- Optimize take profit ratios for profit vs capital efficiency

## Conclusion

The dual EMA crossover strategy leverages EMA crosses for trend direction, along with multiple EMA filtering and dynamic ATR stop loss/profit taking. This allows effective trend following and profit harvesting. However, EMA fitting limitations and stop loss risks require caution. Proper optimization, risk management etc. can lead to more robust performance. The strategy suits experienced traders to achieve high capital efficiency in trending markets.



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|9|Fast EMA|
|v_input_2|21|Slow EMA|
|v_input_3|5|Exit EMA|
|v_input_4|true|FastConf EMA|
|v_input_5|4|SlowConf EMA|
|v_input_6|0|What trades should be taken : : BOTH|SHORT|LONG|NONE|
|v_input_7|true|Stop Loss (ATR)|
|v_input_8|6|Take Profit 1 (ATR)|
|v_input_9|timestamp(01 Sep 2002 13:30 +0000)|Backtesting Start Time|
|v_input_10|timestamp(30 Sep 2099 19:30 +0000)|Backtesting End Time|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-10-09 00:00:00
end: 2023-04-13 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// @author ADHDCRYPT0

//@version=4
strategy(title = "EMA double crossover", shorttitle = "(TEST) double cross over", overlay = true, default_qty_value = 100, initial_capital = 1000,default_qty_type=strategy.percent_of_equity, pyramiding=0, process_orders_on_close=true)


// Variables
ema_len1 = input(9 , title="Fast EMA")
ema_len2 = input(21, title="Slow EMA")
ema_len3 = input(5, title="Exit EMA")
ema_len4 = input(1, title="FastConf EMA")
ema_len5 = input(4, title="SlowConf EMA")

fastEMA = ema(open, ema_len1)
slowEMA = ema(open, ema_len2)
exitEMA = ema(open, ema_len3)
conf1EMA = ema(open, ema_len4)
conf2EMA = ema(open, ema_len5)
plot(fastEMA, title='fastEMA', transp=0, color=color.green)
plot(slowEMA, title='slowEMA', transp=0, color=color.red  )
plot(exitEMA, title='exitEMA', transp=0, color=color.orange)
plot(conf1EMA, title='conf1EMA', transp=0, color=color.blue)
plot(conf2EMA, title='conf2EMA', transp=0, color=color.black)

vol = volume 
volma = sma(volume,7)
vol_cond = vol>volma

atr = atr(5)


// Entry Conditions and vol_cond
long = crossover(fastEMA, slowEMA) and (conf1EMA > conf2EMA) and (fastEMA < exitEMA)
short= crossunder(fastEMA, slowEMA) and (conf1EMA < conf2EMA) and (fastEMA > exitEMA)

tradeType = input("BOTH", title="What trades should be taken : ", options=["LONG", "SHORT", "BOTH", "NONE"])

pos = 0.0

if tradeType=="BOTH"
    pos:= long? 1 : short? -1 : pos[1]
if tradeType=="LONG"
    pos:= long? 1 : pos[1]
if tradeType=="SHORT"
    pos:=short? -1 : pos[1]

longCond  = long  and (pos[1]!= 1 or na(pos[1]))
shortCond = short and (pos[1]!=-1 or na(pos[1]))

// EXIT FUNCTIONS //
sl  = input(1, title="Stop Loss (ATR)", minval=0)
tp  = input(6, title="Take Profit 1 (ATR)", minval=0)

// Simple Stop Loss + 2 Take Profits
sl_long   =  valuewhen(longCond , low - atr * sl, 0)
sl_short  =  valuewhen(shortCond, high+ atr * sl, 0)

tp_long  = valuewhen(longCond , high + atr * tp, 0)
tp_short = valuewhen(shortCond, low  - atr * tp, 0)


long_exit = crossover(fastEMA, exitEMA) and pos[1]==1
short_exit= crossover(exitEMA, fastEMA) and pos[1]==-1

if long_exit or short_exit
	pos:=0


// Position Adjustment
long_sl  = low <sl_long [1] and pos[1]==1
short_sl = high>sl_short[1] and pos[1]==-1

if long_sl or short_sl
    pos:=0
    
//  Strategy Backtest Limiting Algorithm
i_startTime = input(defval = timestamp("01 Sep 2002 13:30 +0000"), title = "Backtesting Start Time", type = input.time)
i_endTime = input(defval = timestamp("30 Sep 2099 19:30 +0000"), title = "Backtesting End Time", type = input.time)
timeCond = true


// Make sure we are within the bar range, Set up entries and exit conditions
if strategy.equity >0
    strategy.entry("long" , strategy.long , when=longCond  and timeCond and tradeType!="SHORT" , alert_message="INSERT MESSAGE HERE")
    strategy.entry("short", strategy.short, when=shortCond and timeCond and tradeType!="LONG" , alert_message="INSERT MESSAGE HERE")
    
    strategy.exit("SL/TP1", from_entry = "long" , stop=sl_long , limit=tp_long , alert_message="INSERT MESSAGE HERE")
    strategy.exit("SL/TP1", from_entry = "short", stop=sl_short, limit=tp_short, alert_message="INSERT MESSAGE HERE")

    strategy.exit("SL", from_entry = "long" , stop=sl_long, alert_message="INSERT MESSAGE HERE")
    strategy.exit("SL", from_entry = "short", stop=sl_short, alert_message="INSERT MESSAGE HERE")
    
    strategy.close("long", when=long_exit , comment="TP2", alert_message="INSERT MESSAGE HERE")
    strategy.close("short", when=short_exit, comment="TP2", alert_message="INSERT MESSAGE HERE")

```

> Detail

https://www.fmz.com/strategy/429391

> Last Modified

2023-10-16 16:24:00
