
> Name

Volume-Weighted-Dual-Trend-Detection-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/16a437a7db7c39470ff.png)


#### Overview
This is a trend detection system that combines trading volume weighting and price movement. The system calculates the difference between opening and closing prices (Delta value), weighted by trading volume, to form a unique trend indicator. The system also integrates a Simple Moving Average (SMA) for signal confirmation, determining market trends by comparing the Delta value with its SMA. Additionally, the system incorporates EMA as an auxiliary indicator, forming a multi-dimensional analytical framework.

#### Strategy Principles
1. Delta Value Calculation: Uses the difference between opening and closing prices within a specific period, weighted by trading volume
2. Signal Generation Mechanism:
   - When Delta crosses above its SMA, the system identifies a bearish signal
   - When Delta crosses below its SMA, the system identifies a bullish signal
3. EMA Integration:
   - System uses 20-period EMA for trend confirmation
   - EMA color changes based on Delta value's position relative to its SMA
4. Volume Filter: Sets volume threshold to ensure trading occurs under sufficient liquidity conditions

#### Strategy Advantages
1. Multi-dimensional Analysis: Combines price, volume, and moving average systems for a more comprehensive market perspective
2. Signal Reliability: Reduces random price fluctuation effects through volume weighting
3. Strong Adaptability: Operates effectively across multiple timeframes, including 4-hour and daily
4. Parameter Flexibility: Offers multiple adjustable parameters for optimization across different market characteristics
5. Risk Control: Built-in volume filtering mechanism effectively avoids low liquidity environments

#### Strategy Risks
1. Trend Reversal Risk: May generate false signals in volatile markets
2. Parameter Sensitivity: Different parameter combinations may lead to significant strategy performance variations
3. Time Lag Risk: Inherent lag in moving average systems may delay entry timing
4. Market Environment Dependency: May generate frequent trading signals in sideways markets

#### Strategy Optimization Directions
1. Introduce Dynamic Parameters:
   - Automatically adjust Delta calculation period based on market volatility
   - Dynamically adjust volume threshold based on volume changes
2. Enhance Signal Filtering:
   - Add trend strength confirmation indicators
   - Integrate price pattern recognition systems
3. Improve Risk Management:
   - Establish dynamic stop-loss mechanism
   - Introduce position management system

#### Summary
This is a systematic strategy that organically combines price momentum, trading volume, and trend indicators. Through multi-dimensional analysis and strict trading condition screening, the strategy maintains high reliability while demonstrating good adaptability and scalability. The core advantage lies in its three-dimensional judgment of market trends, while its greatest development potential lies in dynamic parameter optimization and risk management system improvement.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-09 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Volume-Weighted Delta Strategy", overlay=true)

// Input-parametrit
length_delta = input.int(5, minval=1, title="Delta Length")
length_ma = input.int(5, minval=1, title="MA Length")
length_sma = input.int(5, minval=1, title="MA Length")
volume_threshold = input.float(100000, title="Volume Threshold")

// Funktio delta-arvojen laskemiseksi ja volyymin mukaan painottamiseksi
calculate_volume_weighted_delta(delta_length) =>
    delta_sum = 0.0
    for i = 0 to delta_length - 1
        delta_sum := delta_sum + ((close[i] - open[i]) * volume[i])
    delta_sum







// Laskenta
delta_value = calculate_volume_weighted_delta(length_delta)
ma_value = ta.sma(delta_value, length_sma)


ema20 = ta.ema(close, 20)
// EMA:n värin määrittely
ema_color = delta_value  > ma_value ? color.green : color.red

positive = ta.crossover(delta_value, ma_value)
negative = ta.crossunder(delta_value, ma_value)

// Piirretään graafit

plot(ema20, color=ema_color, title="20 EMA")


BullishCond = ta.crossover(ma_value, delta_value)
BearishCond = ta.crossunder(ma_value, delta_value)


if (BullishCond)
    strategy.entry("Sell", strategy.short)




if (BearishCond)
    strategy.entry("Buy", strategy.long)
```

> Detail

https://www.fmz.com/strategy/474711

> Last Modified

2024-12-11 17:41:23
