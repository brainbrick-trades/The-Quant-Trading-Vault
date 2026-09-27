
> Name

Dual-Moving-Average-Crossover-Strategy-427487

> Author

ChaoZhang

> Strategy Description




## Overview

This strategy is designed based on the principle of golden cross and death cross of two moving averages. When the short-term moving average crosses above the long-term moving average, go long; when the short-term moving average crosses below the long-term moving average, close the position. This strategy is simple and easy to understand, suitable for beginners to learn.

## Strategy Principle

This strategy is mainly based on the two moving averages, sma(close, 14) and sma(close, 28). indicator.

First define long and short moving averages:

```pine
short_ma = sma(close, 14)
long_ma = sma(close, 28)
```

Then use the Golden Cross and Death Cross to decide when entering or exiting:

```pine  
longCondition = crossover(short_ma, long_ma)
shortCondition = crossunder(short_ma, long_ma)
```

Go long when the short-term moving average crosses above the long-term moving average:

```pine
strategy.entry("Buy", strategy.long, when = longCondition) 
```

Close positions when the short-term moving average crosses below the long-term moving average:

```pine
strategy.close_all(when = shortCondition)
```

The strategy principle is simple and clear: it uses double moving average golden and death cross for judgment and has certain trend-following capability.

## Advantage Analysis

- The strategy principles are simple and easy to understand, and even novices can use it easily
- Use golden cross and death cross of moving averages to judge trends, with certain trend-following capabilities
- Moving average periods can be customized to optimize strategy parameters
- Stop-loss points can be set to control individual losses

## Risk Analysis

- The double moving average strategy is sensitive to market fluctuations and may result in multiple losing transactions.
- The moving average is lagging and may miss the price reversal point
- Opening positions near the moving average crossover point is easily trapped
- It is necessary to optimize the moving average cycle parameters, and the effects of different cycles may be different.
- Unable to stop losses quickly when the trend changes violently

## Optimization Direction

This strategy can be optimized from the following aspects:

1. Optimize the moving average cycle parameters and find the best parameter combination

You can try different short-term and long-term moving average periods to find the best combination. For example, (5, 10), (10, 20), (20, 60) and other parameter comparison tests.

2. Added filtering conditions to avoid false signals

Additional filters such as trading volume and price spread can be applied when moving averages cross to avoid excessive trades in choppy markets.

3. Add stop-loss strategy

Set a stop-loss point or use the moving average as a stop-loss line to control the loss of a single trade.

4. Combine with other indicators

You can add MACD, KDJ and other auxiliary indicators for combined trading to improve the strategy effect.

5. Optimize entry points

Find a better entry point near the moving average instead of establishing a position close to the moving average. For example, enter the market at a point where the moving average deviates.

## Summary

The concept of the double moving average strategy is simple, making it easy for beginners to use. However, this strategy is sensitive to market fluctuations and carries a certain risk of loss. We can improve the strategy's effectiveness by optimizing parameters, adding filtering conditions, setting stop-losses, and incorporating other indicators. In strong trends, this strategy can achieve good results. But during volatile market periods, it is recommended to use it cautiously or control risk with stop-losses.



||


## Overview

This strategy is designed based on the golden cross and death cross of dual moving averages. It goes long when the short period moving average crosses above the long period moving average, and closes position when the short period moving average crosses below the long period moving average. The strategy is simple and easy to understand, suitable for beginners to learn.

## Strategy Logic

The strategy is mainly based on the sma(close, 14) and sma(close, 28) indicators. 

First define the short and long moving averages:

```pine
short_ma = sma(close, 14)  
long_ma = sma(close, 28)
```

Then determine entry and exit based on golden cross and death cross:

```pine
longCondition = crossover(short_ma, long_ma)
shortCondition = crossunder(short_ma, long_ma) 
```

Go long when the short MA crosses above the long MA:

```pine
strategy.entry("Buy", strategy.long, when = longCondition)
```

Close position when the short MA crosses below the long MA:

```pine
strategy.close_all(when = shortCondition) 
```

The logic is simple and clear, utilizing the crossovers of dual MAs to determine entries and exits. It has some trend following capacity.


## Advantage Analysis 

- Simple logic, easy for beginners to use
- Utilizes MA crossovers to determine trends
- Customizable MA periods for parameter optimization
- Allows stop loss to control single trade loss

## Risk Analysis

- Sensitive to market fluctuation, may generate multiple losing trades
- Lagging nature of MAs, may miss price reversal points
- Prone to being trapped near MA crossover points
- Need to optimize MA periods, different periods may lead to different results
- Unable to quickly cut loss when trend changes violently

## Optimization Directions

The strategy can be optimized in the following aspects:

1. Optimize MA periods to find the best combination

Test different short and long MA periods, such as (5, 10), (10, 20), (20, 60) etc to find the optimal combination.

2. Add filters to avoid false signals 

Add filters like trading volume, price gap etc. near MA crossovers to avoid excessive trades in ranging markets.

3. Incorporate stop loss 

Set stop loss price or use MA as stop loss line to control single trade loss.

4. Combine with other indicators

Add auxiliary indicators like MACD, KDJ etc. to improve strategy performance. 

5. Optimize entry points

Find better entry points near MAs instead of entering right at the crossover. For example, enter on MA divergence points.

## Summary

The dual MA strategy is simple for beginners to use. But it is sensitive to market fluctuations and has risks of losses. We can improve it by optimizing parameters, adding filters, incorporating stop loss, combining other indicators etc. It can perform well in strong trends but should be used with caution or proper stop loss in ranging markets.  


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|0.6|minGainPercent|
|v_input_2|true|avg_protection|
|v_input_3|true|gain_protection|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-08-21 00:00:00
end: 2023-09-20 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*/

//@version=2
// strategy("Tester", pyramiding = 50, default_qty_type = strategy.cash, default_qty_value = 20, initial_capital = 2000, commission_type = strategy.commission.percent, commission_value = 0.25)

minGainPercent = input(0.6)
gainMultiplier = minGainPercent * 0.01 + 1


longCondition = crossover(sma(close, 14), sma(close, 28))
shortCondition = crossunder(sma(close, 14), sma(close, 28))


avg_protection = input(1)
gain_protection = input(1)


strategy.entry("Buy", strategy.long, when = longCondition    and (avg_protection >= 1 ? (na(strategy.position_avg_price) ? true : close <= strategy.position_avg_price) : true))
strategy.close_all(when = shortCondition  and (gain_protection >=1 ? (close >= gainMultiplier * strategy.position_avg_price) : true))
```

> Detail

https://www.fmz.com/strategy/427487

> Last Modified

2023-09-21 16:40:01
