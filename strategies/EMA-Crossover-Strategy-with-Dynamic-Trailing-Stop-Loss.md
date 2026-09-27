
> Name

EMA-Crossover-Strategy-with-Dynamic-Trailing-Stop-Loss

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d941a2e772f625502ae9.png)
![IMG](https://www.fmz.com/upload/asset/2d87196ff768d91869125.png)




#### Overview
This strategy is a trend-following trading system based on the 68-period Exponential Moving Average (EMA) combined with a dynamic stop-loss mechanism. It identifies market trends through price-EMA crossovers while employing initial and trailing stop-losses for risk management, enabling robust trading in trending markets.

#### Strategy Principles
The strategy utilizes a 68-period EMA as its core indicator for trend determination. Long positions are initiated when price crosses above the EMA, while short positions are taken when price crosses below. Risk management is implemented through a dual stop-loss mechanism: an initial stop-loss and a trailing stop-loss. The initial stop-loss is set at 20 points from the entry price, and when price moves favorably beyond the initial stop-loss distance, the stop-loss price adjusts by 10 points to lock in partial profits.

#### Strategy Advantages
1. Strong trend-following capability: 68-period EMA effectively filters market noise and captures medium to long-term trends.
2. Comprehensive risk control: Dual stop-loss mechanism protects capital while securing profits.
3. Flexible parameters: EMA period and stop-loss points can be adjusted according to different market characteristics.
4. Clear strategy logic: Well-defined entry and exit conditions facilitate live trading and monitoring.
5. High automation level: Strategy can be fully automated, reducing manual intervention.

#### Strategy Risks
1. Sideways market risk: Frequent stop-losses may be triggered in range-bound markets.
Recommended solution: Add trend confirmation indicators like ADX.

2. Gap risk: Large market gaps may cause actual stop-loss prices to deviate from expected levels.
Recommended solution: Consider options hedging or position size adjustment.

3. Parameter optimization risk: Over-optimization may lead to strategy failure.
Recommended solution: Implement out-of-sample testing to ensure parameter stability.

#### Strategy Optimization Directions
1. Trend confirmation mechanism: Suggest incorporating trend strength indicators (such as ADX, MACD) to improve trend identification accuracy.

2. Dynamic parameter adjustment: Automatically adjust EMA period and stop-loss parameters based on market volatility.

3. Position management optimization: Introduce volatility-based dynamic position sizing system.

4. Multi-timeframe correlation: Incorporate longer-term trend analysis to improve trade direction accuracy.

#### Summary
This strategy builds a complete trading system by combining EMA trend following with dynamic stop-loss management. Its core strengths lie in clear trading logic and comprehensive risk control mechanisms. Through the suggested optimization directions, the strategy's stability and profitability can be further enhanced. The strategy is suitable for medium to long-term investors seeking steady returns.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-10-01 00:00:00
end: 2025-02-18 08:00:00
period: 2d
basePeriod: 2d
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("EMA 68 with Trailing Stop-Loss", overlay=true)

// Inputs for customization
length_ema = input(68, title="EMA Length")
initial_stop_loss_points = input(20, title="Initial Stop Loss in Points")
trail_distance = input(10, title="Trailing Stop Adjustment in Points")

ema68 = ta.ema(close, length_ema)

// Plot EMA
plot(ema68, color=color.blue, title="68-Day EMA")

var float entry_price = na // Store entry price
var bool is_long = false // Track if we are in a long trade
var bool is_short = false // Track if we are in a short trade

// Buy Condition: Close above 68-day EMA
if ta.crossover(close, ema68)
    strategy.entry("Long", strategy.long)
    entry_price := close
    is_long := true
    is_short := false

// Sell Condition: Close below 68-day EMA
if ta.crossunder(close, ema68)
    strategy.entry("Short", strategy.short)
    entry_price := close
    is_long := false
    is_short := true

// Long Exit Conditions
if is_long
    stop_loss = entry_price - initial_stop_loss_points
    trail_price = entry_price + initial_stop_loss_points
    if close >= trail_price
        stop_loss := entry_price + trail_distance
    strategy.exit("LongExit", "Long", stop=stop_loss, when=close < ema68)

// Short Exit Conditions
if is_short
    stop_loss = entry_price + initial_stop_loss_points
    trail_price = entry_price - initial_stop_loss_points
    if close <= trail_price
        stop_loss := entry_price - trail_distance
    strategy.exit("ShortExit", "Short", stop=stop_loss, when=close > ema68)

```

> Detail

https://www.fmz.com/strategy/482840

> Last Modified

2025-02-20 14:17:56
