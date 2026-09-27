
> Name

Multi-Moving-Average-Trend-Following-Strategy-Long-term-Investment-Signal-System-Based-on-EMA-and-SMA-Indicators

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1747b5469d5e60898d1.png)


#### Overview
This strategy is a trend following system based on multiple moving averages combination, mainly utilizing the crossover and position relationships between Weekly EMA20, Daily SMA100, Daily SMA50, and Daily EMA20 to capture medium to long-term investment opportunities. The strategy identifies potential long entry points by observing the relationship between price and moving averages, combined with duration requirements.

#### Strategy Principles
The core logic of the strategy is based on the following key conditions:
1. Uses 20-period Weekly Exponential Moving Average (EMA1W20) as the primary trend indicator
2. Combines with 100-day Simple Moving Average (SMA1D100) for secondary trend confirmation
3. Employs 50-day Simple Moving Average (SMA1D50) as medium-term trend reference
4. Utilizes 20-day Exponential Moving Average (EMA1D20) for short-term trend confirmation
The system generates a long signal when the price maintains above EMA1W20 and SMA1D100 for 14 consecutive days and then falls below SMA1D50. This design combines trend confirmation across multiple timeframes to enhance signal reliability.

#### Strategy Advantages
1. Multi-timeframe validation: Combines weekly and daily moving averages for more comprehensive trend assessment
2. Strict entry conditions: Requires price to maintain above major moving averages for sufficient duration, effectively filtering false signals
3. Reasonable risk control: Uses multiple moving average crossovers and positions for clear risk boundaries
4. High adaptability: Strategy parameters can be adjusted for different market environments
5. Clear execution: Trading signals are well-defined and suitable for programmatic implementation

#### Strategy Risks
1. Lag risk: Moving averages inherently have some lag, potentially causing delayed entries
2. Sideways market risk: May generate frequent false breakout signals in ranging markets
3. Parameter sensitivity: Optimal parameters may vary in different market environments
4. Drawdown risk: May experience significant drawdowns during sudden trend reversals
5. Execution risk: Requires stable system operation to avoid signal loss or execution delays

#### Strategy Optimization Directions
1. Incorporate volume indicators: Add volume confirmation mechanism to improve signal reliability
2. Optimize parameter adaptation: Develop dynamic parameter adjustment mechanisms
3. Add filtering conditions: Consider adding market environment indicators
4. Improve stop-loss mechanism: Design more detailed stop-loss and profit-taking rules
5. Enhance signal confirmation: Consider adding other technical indicators for auxiliary confirmation

#### Summary
This strategy establishes a relatively comprehensive trend following system through multiple moving average combinations, suitable for medium to long-term investors. While it has certain lag and parameter sensitivity risks, the strategy has practical value through proper risk control and continuous optimization. Investors are advised to make appropriate adjustments based on their risk preferences and market conditions.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-11-12 00:00:00
end: 2024-12-11 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © petitepupu

//@version=5

ema20wTemp = ta.ema(close, 20)
ema20w = request.security(syminfo.tickerid, "1W", ema20wTemp, barmerge.gaps_on, barmerge.lookahead_off)
sma100d = ta.sma(close, 100)
sma50d = ta.sma(close, 50)
ema20d = ta.ema(close, 20)
daysAbove = input.int(14, title="Days", minval=1)
plot(ema20w, color=color.blue)
plot(sma100d, color=color.yellow)
plot(sma50d, color=color.red)
plot(ema20d, color=color.green)

longCondition = true
clean = true
for i = 0 to daysAbove
    if close[i] < ema20w or close[i] < sma100d or close > sma50d
        longCondition := false
        clean := false
        break

//TODO: 
if clean != true
    longCondition := true
    for i = 0 to daysAbove
        if close[i] > ema20w or close[i] > sma100d or close >= ema20d or -100 * (close - ema20d)/ema20d < 5.9
            longCondition := false
            break


// plotshape(series=longCondition, location=location.belowbar, color=color.green, style=shape.triangleup, title="Buy Signal", size = size.small)

if (longCondition)
    strategy.entry("Long", strategy.long)

    
strategy(title="LT Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=800)
```

> Detail

https://www.fmz.com/strategy/474956

> Last Modified

2024-12-13 10:28:02
