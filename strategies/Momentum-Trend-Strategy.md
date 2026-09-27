
> Name

Momentum-Trend-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/126e84c1d7dc8fdd516.png)
 
### Overview  

This strategy incorporates momentum indicators and trend tracking to identify the mid-term uptrend or downtrend of stock prices and take positions at the beginning stage of trends. The strategy firstly computes the 20-day momentum indicator of price, then processes it into a normalized momentum value ranging from 0 to 1. Meanwhile, the 20-day simple moving average is calculated as a representative of the mid-term trend. When the normalized momentum is larger than 0.5 and the price is above the mid-term trendline, go long. When the normalized momentum is less than 0.5 and the price is below the mid-term trendline, go short.

### Strategy Logic  

The core indicator of this strategy is the 20-day momentum difference of price. The momentum difference is defined as: (today's close – close 20 days ago) / close 20 days ago. This metric reflects the percentage increase or decrease of price over the last 20 days. To solve the issue of vastly different price ranges across stocks, the raw momentum difference is normalized to a 0 to 1 scale by the following process: first find the maximum and minimum values of momentum difference in the past 100 days, then calculate the percentage position of current difference within this range, resulting in a normalized momentum score between 0 and 1. The normalization can better capture the magnitude of price movement.

In addition, the 20-day simple moving average is included to determine the mid-term trend direction. Moving averages are visually intuitive tools for trend analysis. When the price is above the moving average line, it signals an uptrend. When below the line, it indicates a downtrend.   

By combining the normalized momentum indicator and mid-term trend judgment, this strategy aims to capture significant bullish and bearish stages in the mid-term horizon. The logic is: if normalized momentum is larger than 0.5, it means the price is accelerating with an uptrend recently. Meanwhile, if the price stays above 20-day MA, then the mid-term is still an uptrend. Under this condition, go long. On the contrary, if normalized momentum drops below 0.5, it signals an accelerating downtrend recently. Also, with the price below 20-day MA, the mid-term is bearish. Then we should go short.  

The above describes the core decision logic. For entries, the strategy simply enters the market when observing aligned momentum and trend signals. For stop loss, a fixed stop is set at the highest price + minimum tick size for longs, and lowest price - minimum tick size for shorts, in order to prevent inefficient floating losses.

### Advantage Analysis 

The biggest advantage of this strategy is utilizing two indicators for confirmation, which can effectively filter out some false entries in whipsaws. Relying solely on momentum signals tends to produce fake signals occasionally. By adding the condition of mid-term trend, the validity of momentum signals can be verified to avoid being trapped in ranging markets. Similarly, just following the trend may miss some opportunities at the beginning of trend accelerations, while combining momentum can capture such turns in a timely fashion. So the two indicators complement each other to form more robust decisions.  

Another advantage is the choice of 20-day period. This mid-term parameter helps reduce trading frequency compared to faster frequencies, allowing the strategy to capture larger swings over the medium-long term. Meanwhile, it can also filter out short-term market noises.

### Risk Analysis

The major risk of this strategy lies in the divergence between momentum and trend. Misalignments may lead to incorrect signals. For instance, during a downtrend, short-term bounces could push momentum upwards temporarily. If going straight long, it may encounter losses.  

In addition, the stop-loss mechanism is relatively simple and may fail to fully contain risks. In case of huge price gaps, the fixed loss size could be gapped through directly, proving inadequate reaction.

### Optimization Directions   

Here are some major optimization directions for this strategy:

1. Introduce more indicators for cross-examination, such as MACD, KD, Bollinger Bands etc. This can help verify the validity of momentum signals and avoid false signals.  

2. Dynamically adjust stop loss levels, through ATR or options pricing models for example. This may reduce the chance of stops being hit.

3. Optimize parameter periods. The current 20-day parameters can be tested for enhancements.

4. Differentiate buy and sell threshold of momentum difference. Currently 0.5 is used for both. The optimal levels may differ. 

5. Add trading volume filter to avoid false breakouts with insufficient volumes.

### Conclusion   

This strategy combines trend analysis and momentum indicators to capture trading opportunities arising from momentum changes over the medium-long term. Compared to single indicator systems, the multiple indicator approach improves accuracy and profitability. The simple stop mechanism facilitates quick risk control. Further optimizations on parameter tuning, stop-loss techniques and auxiliary conditions can enhance flexibility and adaptiveness to varying market regimes. Overall, it represents a promising quantitative strategy with expansion potential.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1_close|0|src: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|20|lookback|
|v_input_3|0|Bar color scheme: 1|2|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-29 00:00:00
end: 2024-01-28 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("Momentum Strategy, rev.2", overlay=true)

//
// Data
//
src = input(close)
lookback = input(20)
cscheme=input(1, title="Bar color scheme", options=[1,2])

//
// Functions
//
momentum(ts, p) => (ts - ts[p]) / ts[p]

normalize(src, len) =>
    hi  = highest(src, len)
    lo  = lowest(src, len)
    res = (src - lo)/(hi - lo)

//
// Main
//
price = close
mid = sma(src, lookback)
mom = normalize(momentum(price, lookback),100)

//
// Bar Colors
//
clr1 = cscheme==1?black: red
clr2 = cscheme==1?white: green
barcolor(close < open ? clr1 : clr2)

//
// Strategy
//
if (mom > .5 and price > mid )
    strategy.entry("MomLE", strategy.long, stop=high+syminfo.mintick, comment="MomLE")
else
    strategy.cancel("MomLE")

if (mom < .5 and price < mid )
    strategy.entry("MomSE", strategy.short, stop=low-syminfo.mintick, comment="MomSE")
else
    strategy.cancel("MomSE")

//plot(strategy.equity, title="equity", color=red, linewidth=2, style=areabr)
```

> Detail

https://www.fmz.com/strategy/440370

> Last Modified

2024-01-29 16:38:22
