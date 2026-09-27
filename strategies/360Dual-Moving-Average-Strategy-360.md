
> Name

360Dual-Moving-Average-Strategy-360

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1f0f44c7ab39e16b9d4.png)

## Overview  

The Dual Moving Average Strategy 360° is a quantitative trading strategy that incorporates dual moving averages and trend strength determination. By calculating moving averages over different periods, it determines price trends; meanwhile, by accumulating tangent angles, it judges the strength of trends and achieves more accurate entries and exits.

## Strategy Logic  

The core logic of the Dual Moving Average Strategy 360° is:  

1. Calculate the 1-minute and Kalman-filtered moving averages;
2. Calculate the tangent angle based on the price difference between the two moving averages; 
3. Accumulate tangent angles to determine trend strength signals;
4. Issue trading signals based on whether the accumulated tangent angles exceed preset thresholds.

Specifically, the strategy defines the raw 1-minute moving average and the Kalman-filtered moving average. The Kalman filter eliminates some noise from the moving average to make it smoother. The tangent angle between the two moving averages reflects price trend changes. For example, when the tangent angle is positive, it indicates an upward trend; conversely, a negative angle represents a downward trend.  

The strategy chooses 30 minutes as the calculation period to sum all positive and negative tangent angles within that period. When the sum exceeds 360 degrees, it signals an extremely strong trend and issues a long signal; conversely, when the sum is below -360 degrees, it indicates a trend reversal and issues a short signal.

## Advantage Analysis 

The main advantages of the Dual Moving Average Strategy 360° are:  

1. Moving averages filter out short-term market noise for more reliable trading decisions;  
2. Tangent angles quantify trend strength, avoiding the subjectivity of judging by moving average patterns alone;
3. Summing multiple tangent angles has better noise reduction effects, resulting in more reliable trading signals;  
4. Compared to single moving average strategies, the dual moving averages combined with trend strength determinations make the strategy more comprehensive and robust.

## Risk Analysis

The Dual Moving Average Strategy 360° also carries some risks:

1. Moving averages lag price changes and may miss short-term trend turning points;
2. Relying solely on the accumulated trend strength signal can be disrupted by market volatility;  
3. Improper parameter settings (such as calculation period lengths) may lead to missing trades or generating incorrect signals.  

To mitigate the above risks, measures like shortening the moving average period, optimizing parameter combinations, adding stop-loss mechanisms can be adopted.

## Optimization Directions   

The Dual Moving Average Strategy 360° can be further optimized by:  

1. Incorporating adaptive moving averages that adjust parameters based on market volatility;
2. Referencing multiple moving average periods to form optimized parameter combinations;  
3. Adding dynamic trend determination modules based on volatility, trading volumes, etc.;
4. Assisting parameter tuning or trade decisions with machine learning models.

## Summary  

The Dual Moving Average Strategy 360° utilizes moving average filtering and quantitative tangent angle trend judgments to achieve a relatively robust quantitative trading strategy. Compared to single technical indicators, this strategy forms a more comprehensive consideration and has stronger practicality. But parameter tuning and risk control are still vital, and the strategy can be further optimized for even better results going forward.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-25 00:00:00
end: 2024-01-30 08:00:00
period: 5m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
//@library=math
strategy("Strategy 360° (Test)", overlay=true)

// Definition1Minute Moving Average
ma1 = request.security(syminfo.tickerid, "1", ta.sma(close, 1)) // Used here math.sma() Function
//plot(ma1, color=color.yellow, title="Original Moving Average")

// Define the Kalman filter function, referenced here[1](https://www.tradingview.com/pine-script-docs/en/v5/language/Methods.html)and[2](https://www.tradingview.com/pine-script-docs/en/v5/language/Operators.html)Code of
kalman(x, g) => 
    kf = 0.0 
    dk = x - nz(kf[1], x) // The nz() function is used here
    smooth = nz(kf[1], x) + dk * math.sqrt(g * 2) // Used here math.sqrt() Function
    velo = 0.0 
    velo := nz(velo[1], 0) + g * dk // The nz() function is used here
    kf := smooth + velo 
    kf 

// Define the moving average after Kalman filtering
ma2 = kalman(ma1, 0.01) 
plot(ma2, color=color.blue, title="Moving average after Kalman filtering")

// Define Tangent Angle
angle = math.todegrees(math.atan(ma2 - ma2[1])) // Used here math.degrees() and math.atan() Function

// Define cumulative tangent angles
cum_angle = 0.0
cum_angle := nz(cum_angle[1], 0) + angle // The nz() function is used here

// Definition30Minute Cycle
period = 30 // You can modify this parameter according to your needs

// Define the sum of tangent angles within the period
sum_angle = 0.0
sum_angle := math.sum(angle, period) // Used here math.sum() Function, change the sum of tangent angles within the period to simply 5 Add tangent angles

// Define buy and sell conditions
buy = sum_angle > 360// Used here math.radians() Function
sell = sum_angle < -360

// Perform buy and sell operations
strategy.entry("Long", strategy.long, when=buy)
strategy.close("Short", when=buy)
strategy.entry("Short", strategy.short, when=sell)
strategy.close("Long", when=sell)

// Draw chart
plot(sum_angle, color=color.green, title="Sum of tangent angles within the period")
plot(angle, color=color.red, title="Tangent angle") // This is the code I added for you to display the real-time calculated tangent angle

```

> Detail

https://www.fmz.com/strategy/440827

> Last Modified

2024-02-02 14:29:59
