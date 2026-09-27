
> Name

Dual-Moving-Average-Pressure-Rebound-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/106cd1e0c6d8a25a411.png)

### Overview

The dual moving average pressure rebound strategy is a very simple hedge strategy for stock indices. It only conducts long positions. When the price approaches the pressure level during an uptrend, it opens positions to avoid entering the market after a major breakthrough of the pressure level and lock in a better purchase price.

### Strategy Principle  

The strategy uses both the long-term 200-day moving average and the short-term 10-day moving average. Positions can only be opened when the closing price is above the 200-day line, that is, the long-term trend is up. When the closing price is below the 10-day line, it means that the stock index is in a pressure zone. At this time, if the RSI indicator is less than 30, it indicates that stock prices may rebound. Then go long to open a position.

Once the position is opened, set a 5% stop loss and 10% take profit to exit the trade. In addition, if the price breaks through the 10-day line upwards, take profit proactively.

### Advantage Analysis

The biggest advantage of the dual moving average pressure rebound strategy is its strong trend-following capability. By adopting dual short and long moving averages, it can effectively judge the direction of the long-term trend. Long positions will only be considered when the long-term trend is up. This avoids the risks of blindly going long.

Secondly, the timing of entry this strategy chooses is very precise. It takes advantage of the pressure brought by the moving average zone and judges the overbought and oversold indicator to select the optimal timing for a rebound. This enables a relatively superior entry price and allows more room for profit.

### Risk Analysis  

The biggest risk of the dual moving average pressure rebound strategy is that it is prone to multiple small stop losses. When the price oscillates back and forth in the pressure zone, it is very likely to trigger stop loss repeatedly. In this case, there is a risk of multiple small losses.

In addition, if the long-term trend is incorrectly judged, which leads to a major break-out upon entry, the stop loss here may be larger, posing greater risks.

To control risks, properly loosening the stop loss range and increasing the holding period can be adopted. At the same time, the long-term trend must be judged prudently to avoid risks brought by incorrect long positions.

### Optimization

The strategy can be optimized in the following aspects:

1. Add more factors to judge the long-term trend. In addition to simple moving averages, more indicators such as fundamentals and trading volume changes can be introduced to make more accurate judgments on long-term trends.

2. Optimize entry timing. Judging whether there is a significant amplification of energy before breaking through the pressure level is beneficial for judging the intensity and amplitude of the rebound.  

3. Optimize the take profit method. The existing take profit method is relatively passive and cannot continuously capture the increase. More dynamic take profit methods such as trail stops can be studied. While ensuring controllable risks, more gains can be obtained.

4. Optimize position management. The position size can be adjusted in real-time according to the fluctuation range of the broader market. This can reduce P&L fluctuations and achieve more stable returns.

### Summary  

The dual moving average pressure rebound strategy is a simple and practical hedging strategy. It can effectively track long-term trends and choose high-quality rebound timing to open positions. By setting stop loss and take profit to lock in profits, risks can be avoided. The theoretical basis of this strategy is simple and suitable for most people. It is a good hedging strategy.

There is still great potential for the strategy to be improved in aspects like optimizing entry timing, dynamic take profit methods and position management. It is worthwhile to investigate further.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|200|(?パラメータ)Long-term moving averageBASE200/period of long term sma|
|v_input_int_2|10|Long-term moving averageBASE10/period of short term sma|
|v_input_int_3|5|Stop loss ratio％/stoploss percentages|
|v_input_int_4|20|Take profit ratio％/take profit percentages|
|v_input_1|timestamp(01 Jan 2000 13:30 +0000)|(?(Period) Start date for backtesting/start trade day|
|v_input_2|timestamp(1 Jan 2099 19:30 +0000)|バックテスをFinal day/finish date day|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-22 00:00:00
end: 2024-02-21 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © tsujimoto0403

//@version=5
strategy("simple pull back", overlay=true,default_qty_type=strategy.percent_of_equity,
     default_qty_value=100)

//input value 
malongperiod=input.int(200,"Long-term moving averageBASE200/period of long term sma",group = "パラメータ")
mashortperiod=input.int(10,"Long-term moving averageBASE10/period of short term sma",group = "パラメータ")
stoprate=input.int(5,title = "Stop loss ratio％/stoploss percentages",group = "パラメータ")
profit=input.int(20,title = "Take profit ratio％/take profit percentages",group = "パラメータ")
startday=input(title="バックテストをThe day to open/start trade day", defval=timestamp("01 Jan 2000 13:30 +0000"), group="period")
endday=input(title="バックテスをFinish date day", defval=timestamp("1 Jan 2099 19:30 +0000"), group="Period")


//polt indicators that we use 
malong=ta.sma(close,malongperiod)
mashort=ta.sma(close,mashortperiod)

plot(malong,color=color.aqua,linewidth = 2)
plot(mashort,color=color.yellow,linewidth = 2)

//date range 
datefilter = true

//open conditions
if close>malong and close<mashort and strategy.position_size == 0 and datefilter and ta.rsi(close,3)<30 
    strategy.entry(id="long", direction=strategy.long)
    
//sell conditions 
strategy.exit(id="cut",from_entry="long",stop=(1-0.01*stoprate)*strategy.position_avg_price,limit=(1+0.01*profit)*strategy.position_avg_price)


if close>mashort and close<low[1] and strategy.position_size>0
    strategy.close(id ="long")
        



```

> Detail

https://www.fmz.com/strategy/442514

> Last Modified

2024-02-22 15:29:04
