
> Name

Trend-Following-Strategy-Based-on-Hull-Moving-Average-and-True-Range

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/14952cbb0a04ee6a4cf.png)
 
## Overview

The core idea of this strategy is to identify market trend directions by combining Hull moving average and average true range (ATR), and enter positions after the trend direction is confirmed. Specifically, it calculates the difference between the Hull moving averages of a certain period and the previous period. When the difference rises, it indicates a bullish trend; when the difference declines, it indicates a bearish trend. At the same time, the ATR index is used to determine the amplitude. It enters positions when the trend direction is confirmed and the amplitude keeps expanding.

## Strategy Logic

This strategy mainly relies on two types of indicators: Hull moving average and ATR.

The Hull moving average is a trend-following indicator developed by American futures trader Alan Hull. Similar to moving averages, the Hull moving average has higher sensitivity and can capture price changes and trends faster. The strategy sets an adjustable parameter hullLength to control the period of the Hull moving average. By calculating the difference between the current period's Hull MA and previous period's, it determines the current price trend direction.

ATR stands for Average True Range. It reflects the amplitude of daily price fluctuations. When volatility increases, ATR rises; when volatility declines, ATR falls. The strategy sets parameters like atrLength and atrSmoothing to control the ATR calculation. And ATR is plotted on the chart as one reference for entries.

Specifically, the strategy logic is:  

1. Calculate current period Hull MA (hullLength) and previous period Hull MA. 
2. Calculate the difference: hullDiff = currentHullMA - previousHullMA
3. When hullDiff > 0, it indicates a bullish trend. When hullDiff < 0, it indicates a bearish trend.
4. Calculate ATR (atrLength) of a period as an amplitude benchmark.
5. When bullish trend is identified and ATR > price > price of atrLength periods ago, go long. When bearish and ATR < price < price of atrLength periods ago, go short.  
6. Use the positive/negative of hullDiff to determine close signals.

## Advantage Analysis 

The advantages of this strategy:

1. Combining trend judgment and volatility index, it can enter positions when price trend is clear and volatility rises to avoid whipsaws in range-bound markets.
2. Hull MA responds faster to price changes and can quickly identify new trend directions.
3. ATR reflects market volatility and heat, providing guidance for entry timings.  
4. Multiple adjustable parameters can be optimized for best parameter combinations.

## Risk Analysis

Some risks of this strategy:

1. Both Hull MA and ATR cannot completely avoid false breakouts and thus holds the risk of being trapped.
2. Improper parameter settings may lead to over-trading or insufficient sensitivity, undermining strategy efficacy. 
3. It cannot handle violent price actions like sharp spikes or crashes effectively.

Solutions:

1. Set proper stop loss to avoid being trapped by false breakouts.
2. Test and optimize parameters to fit different market environments.
3. Suspend strategy when facing violent volatility.  

## Optimization Directions 

There is still large room for optimization:

1. Test different hullLength parameters to find the optimal settings for current markets.
2. Test ATR period combinations to grasp market heat the best.  
3. Try different ATR smoothing methods to see which performs the best.
4. Optimize entry conditions with other volatility indicators like Reaction combined with ATR. 
5. Optimize stop loss to avoid being trapped.

## Conclusion

This strategy integrates the trend following capacity of Hull MA and the heat judgment ability of ATR. It enters positions when trend is confirmed and volatility rises to filter out some invalid signals. Further enhancement can be achieved by parameter optimization and better risk management. In summary, this strategy combines multiple factors of trend tracking and heat judgment. When parameters are fine-tuned, it can deliver good results.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|50|Hull Length|
|v_input_2|50|ATR Length|
|v_input_3|0|ATR Smoothing: RMA|SMA|EMA|WMA|
|v_input_4_ohlc4|0|Price data: ohlc4|high|low|open|hl2|hlc3|hlcc4|close|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-07 00:00:00
end: 2024-01-14 00:00:00
period: 10m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
//                                                Hull cross and ATR
strategy("Hull cross and ATR", shorttitle="H&ATR", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100, calc_on_order_fills=true, calc_on_every_tick=true, pyramiding=0)
keh=input(title="Hull Length",defval=50)
length = input(title="ATR Length", defval=50, minval=1)
smoothing = input(title="ATR Smoothing", defval="RMA", options=["RMA", "SMA", "EMA", "WMA"])
p=input(ohlc4,title="Price data")
n2ma=2*wma(p,round(keh/2))
nma=wma(p,keh)
diff=n2ma-nma
sqn=round(sqrt(keh))
n2ma1=2*wma(p[1],round(keh/2))
nma1=wma(p[1],keh)
diff1=n2ma1-nma1
sqn1=round(sqrt(keh))
n1=wma(diff,sqn)
n2=wma(diff1,sqn)
ma_function(source, length) => 
    if smoothing == "RMA"
        rma(p, length)
    else
        if smoothing == "SMA"
            sma(p, length)
        else
            if smoothing == "EMA"
                ema(p, length)
            else
                wma(p, length)
plot(ma_function(tr(true), length), title = "ATR", color=black, transp=50)
closelong = n1<n2
if (closelong)
    strategy.close("buy")
closeshort = n1>n2
if (closeshort)
    strategy.close("sell")
if (ma_function(tr(true), length)<p and p>p[length] and n1>n2)
    strategy.entry("buy", strategy.long, comment="BUY")
if (ma_function(tr(true), length)>p and p<p[length] and n1<n2)
    strategy.entry("sell", strategy.short, comment="SELL")
```

> Detail

https://www.fmz.com/strategy/438824

> Last Modified

2024-01-15 15:26:08
