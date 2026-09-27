
> Name

Logarithmic-Price-Forecasting-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1765dd89f4fbd5b67f1.png)
 
## Overview

This strategy uses logarithmic functions to model price changes based on the standard deviation and mean of trading volume to calculate z-score as input parameters to the logarithmic function for predicting future prices.

## Strategy Principles  

1. Calculate ROC value of closing price, accumulate positive values into volume_pos and negative values into volume_neg
2. Calculate the difference between volume_pos and volume_neg as net_volume 
3. Calculate standard deviation net_std and mean net_sma of net_volume
4. Calculate z-score by dividing net_sma by net_std
5. Use closing price, 20-day standard deviation of closing price and z-score as parameters into the logistic function to predict next period's price
6. Long when predicted price is above current actual price * 1.005, close position when below * 0.995

## Advantage Analysis

This strategy combines statistical information of trading volume and price prediction using logarithmic functions.

Advantages are:

1. Utilizes long-short difference in trading volume to gauge market sentiment
2. Logarithmic function fits price change curve well for prediction
3. Simple and straightforward strategy, easy to implement

## Risk Analysis  

Some risks also exist in this strategy:

1. Trading volume indicators have lag, cannot timely reflect market changes
2. Logarithmic prediction not always accurate, can be misleading  
3. Lack of stop loss measures inability to control losses

Risks can be reduced by:

1. Combine other indicators to judge reliability of volume signals  
2. Optimize parameters of logarithmic function to improve prediction accuracy 
3. Set stop loss lines to limit maximum loss per trade and overall

## Optimization Directions

This strategy can be further optimized by:

1. Adopt machine learning to dynamically optimize logarithmic function  
2. Incorporate volatility indicators to adjust position sizing  
3. Add Bayesian filtering to filter out invalid signals
4. Combine with breakout strategies to enter on breakout points
5. Use association rules to detect volume-price divergence signals  

Combining multiple methods can further improve stability and profitability.

## Conclusion  

This strategy integrates statistical indicators of trading volume and logarithmic prediction into a unique quantitative trading methodology. With continuous optimization, it can become an efficient and stable automated trading system. By leveraging machine learning and portfolio optimization theories, we are confident to further improve its trading performance.




> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-19 00:00:00
end: 2023-12-10 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Logistic", overlay=true )

volume_pos = 0.0
volume_neg = 0.0
roc = roc(close, 1)

for i = 0 to 100
    if (roc > 0)
        volume_pos := volume
    else
        volume_neg := volume
    
volume_net = volume_pos - volume_neg
net_std    = stdev(volume_net, 100)
net_sma    = sma(volume_net, 10)
z          =  net_sma / net_std
std        = stdev(close, 20)

logistic(close, std, z) =>
    m = (close + std)
    a = std / close
    pt = m / ( 1 + a*exp(-z))
    pt
    
    
pred = logistic(close, std, z)

buy = pred > close * 1.005
sell = pred < close * 0.995

color = strategy.position_size > 0? #3BB3E4 : strategy.position_size == 0? #FF006E : #6b6b6b
barcolor(color)


if (buy == true)
    strategy.entry("Long", strategy.long, comment="Open L")
    
if (sell == true)
    strategy.close("Long", comment="Close L")

```

> Detail

https://www.fmz.com/strategy/435966

> Last Modified

2023-12-20 14:40:23
