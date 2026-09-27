
> Name

Eight-Day-Extended-Run-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/f84799697d3ba9f989.png)
 
### Overview

This strategy is inspired by Linda Bradford Raschke and specially designed for the US T-Note futures (ZN1!). It tracks the 5-day simple moving average (SMA) to find price moves that can sustain above or below the average for over 8 days, in order to capture longer-term price trends.  

### Strategy Logic   

The core indicator of this strategy is the 5-day SMA. Through extensive testing and research, Linda proves this indicator to be very effective for trend identification. She finds that in each market, prices tend to have around 9-10 exceptionally large outlier moves per year in the direction of the trend. If the trend persists, these outliers often lead to extended price runs. That's why the 5-day SMA is chosen as the core indicator.

Specifically, the strategy logic is designed as follows:  

1. Use the 5-day SMA to determine the price trend direction. When price is above 5-day SMA, the trend is up. When price is below 5-day SMA, the trend is down.

2. Detect if price can sustain above/below the 5-day SMA for over 8 days after breaking through it. If it's an upward trend but price breaks below the SMA and runs for over 8 days (TriggerBuy variable), go long when price turns back up after the first pullback (Buy variable). If it's a downward trend but price breaks above the SMA and runs for over 8 days (TriggerSell variable), go short when price turns back down after the first pullback (Sell variable). 

3. Hold the position for 10 days after entering.

By doing so, the strategy aims to capture longer-term price trends and achieve excess returns.

### Advantage Analysis

The advantages of this strategy include:

1. It adopts the validated 5-day SMA indicator for trend identification, which provides solid theoretical ground for price breakout judgment and trade signals.

2. The trade logic is designed around the exceptional phenomenon of persistent price breakout against the trend direction. These outliers usually imply an extended price run afterwards. Capturing such runs presents high-probability profit opportunities.

3. Entry signals are clear cut, which is the pullback after the first declining/rising leg. This helps filter out some false breakouts. 

4. The 10-day holding period is comparatively long, which also facilitates capturing longer price runs.

### Risk Analysis   

There are also some risks associated with this strategy:

1. The 5-day SMA has some lagging effect, which may result in incorrect trend judgments, causing wrong long/short decisions.

2. Even if the price run sustains for over 8 days, it could still turn out to be a false breakout. If the trend quickly reverses, it poses the risk of losses.

3. The 10-day holding period is relatively long, leading to larger losses if stopped out.

Counter measures:

1. Test adding other indicators to help determine trends, e.g. MACD, to improve accuracy.

2. Adjust parameters based on specific markets, such as lowering the price run days to 6-7 days.  

3. Experiment with moving stop loss to control maximum losses.

### Optimization Directions   

The strategy can be further optimized in the following aspects:

1. Test adding other indicators to aid trend determination, e.g. MACD, KDJ etc. This can improve trend accuracy.

2. Optimize parameters like minimum price run days, holding days after entry etc, to find the optimal parameter combinations.

3. Try setting up moving stop loss after entry to control risks and optimize the stop loss percentage. This balances capturing big trends and limiting per trade losses.

4. Test setting up price targets after entry for actively taking profits. This allows locking in some profits along the way.  

5. Consider closing the strategy during high volatility regimes to avoid being caught in whipsaws. Can be achieved by setting volatility or market benchmark conditions to control strategy activation.


### Summary   

This strategy is inspired by famous trader Linda Raschke. It tracks the 5-day SMA indicator to determine price trends, and designs trade logic based on exceptional price runs to capture big trends. The advantages like solid indicator basis, clear signal generation, long holding periods etc make it suitable for catching longer-term price moves. Meanwhile, certain risks like lagging effect and holding risks do exist. Further optimizations can be done from multiple dimensions to improve the strategy's profit factor.




> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-18 00:00:00
end: 2023-12-18 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Marcuscor

//@version=4

// Inpsired by Linda Bradford Raschke: a strategy  for the T-note futures (ZN1!) that finds 8 day extended runs above/ below the 5sma and buys/ sells the first pullback below/ above the 5sma
// as of 01/10/2021 the t-test score is 4.06

strategy("8DayRun", overlay=true)


SMA = sma(close,5)

TrendUp = close > SMA

TrendDown = close < SMA

//logic to long

TriggerBuy = barssince(close < SMA) > 8

Buy = TriggerBuy[1] and TrendDown

strategy.entry("EL", strategy.long, when = Buy)
strategy.close(id = "EL", when = barssince(Buy) >10)

bgcolor(TriggerBuy ? color.red : na)
bgcolor(Buy ? color.blue : na)

// logic to short 

TriggerSell = barssince(close > SMA) > 8

Sell = TriggerSell[1] and TrendUp

strategy.entry("ES", strategy.short, when = Sell)
strategy.close(id = "ES", when = barssince(Sell) > 10)

bgcolor(TriggerSell ? color.white : na)
bgcolor(Sell ? color.fuchsia : na)




```

> Detail

https://www.fmz.com/strategy/435852

> Last Modified

2023-12-19 12:01:49
