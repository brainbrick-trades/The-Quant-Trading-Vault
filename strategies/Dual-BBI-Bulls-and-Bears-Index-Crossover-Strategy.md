
> Name

Dual-BBI-Bulls-and-Bears-Index-Crossover-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/f30bf2b8b373577fc0.png)


This strategy is based on the crossover signals between two groups of Bulls and Bears Index (BBI) with different periods. It captures market trend changes by comparing the crossover of short-period and long-period BBIs for trading decisions.

#### Strategy Overview
The strategy employs two groups of BBI indicators, each consisting of 4 Simple Moving Averages (SMA) with different periods. Group A uses shorter periods (12/24/48/80) to capture short-term price trends, while Group B uses longer periods (120/240/480/600) to confirm long-term trends. Long positions are opened when the short-period BBI crosses above the long-period BBI and closed when it crosses below.

#### Strategy Principle
1. Calculate two groups of BBI indicators, each derived from 4 SMAs with different periods
2. Group A BBI = (SMA12 + SMA24 + SMA48 + SMA80) / 4
3. Group B BBI = (SMA120 + SMA240 + SMA480 + SMA600) / 4
4. Enter long positions when Group A BBI crosses above Group B BBI, indicating short-term trend becoming stronger than long-term trend
5. Exit positions when Group A BBI crosses below Group B BBI, indicating short-term trend weakening

#### Strategy Advantages
1. Reduces false signals through the use of multiple moving average combinations
2. Improves signal reliability by combining short-term and long-term trend analysis
3. Simple and clear strategy logic, easy to understand and execute
4. Good trend-following characteristics, capable of capturing significant trending movements

#### Strategy Risks
1. May generate frequent crossover signals in ranging markets, leading to overtrading
2. Entry and exit signals have inherent lag, potentially missing optimal prices
3. Lacks risk control measures such as stop-loss and take-profit settings
4. May experience significant drawdowns in highly volatile markets

#### Strategy Optimization Directions
1. Add trend confirmation indicators like RSI or MACD to filter false signals
2. Implement stop-loss and take-profit mechanisms to control single-trade risk
3. Optimize BBI period parameters based on different market characteristics
4. Consider incorporating volume indicators to improve signal reliability
5. Add volatility filters to reduce trading frequency during high volatility periods

#### Summary
This strategy captures market trends by comparing BBI indicators with different periods, featuring clear logic and easy execution. However, it needs additional risk control measures and parameter optimization for different market conditions to improve stability and reliability. It is recommended to conduct thorough backtesting and combine with other technical indicators before live trading.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-10 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// @version=6
strategy("BBI Long strategy", overlay=true)

// Custom parameter settings
input_ma1_a = input(12, title="AGroup MA1 period")
input_ma2_a = input(24, title="AGroup MA2 period")
input_ma3_a = input(48, title="AGroup MA3 Period")
input_ma4_a = input(80, title="AGroup MA4 Period")
input_ma1_b = input(120, title="BGroup MA1 period")
input_ma2_b = input(240, title="BGroup MA2 period")
input_ma3_b = input(480, title="BGroup MA3 Period")
input_ma4_b = input(600, title="BGroup MA4 Period")

// Settings A Group BBI
ma1_a = ta.sma(close, input_ma1_a)
ma2_a = ta.sma(close, input_ma2_a)
ma3_a = ta.sma(close, input_ma3_a)
ma4_a = ta.sma(close, input_ma4_a)
bbi_a = (ma1_a + ma2_a + ma3_a + ma4_a) / 4

// Settings B Group BBI
ma1_b = ta.sma(close, input_ma1_b)
ma2_b = ta.sma(close, input_ma2_b)
ma3_b = ta.sma(close, input_ma3_b)
ma4_b = ta.sma(close, input_ma4_b)
bbi_b = (ma1_b + ma2_b + ma3_b + ma4_b) / 4

// Appropriate A Group BBI Break above B Group BBI , execute the long strategy
long_condition = ta.crossover(bbi_a, bbi_b)
if (long_condition)
    strategy.entry("Long", strategy.long)

// Appropriate A Group BBI Break below B Group BBI , close the position
close_condition = ta.crossunder(bbi_a, bbi_b)
if (close_condition)
    strategy.close("Long")

// Draw BBI Indicator
plot(bbi_a, color=color.blue, title="BBI A")
plot(bbi_b, color=color.red, title="BBI B")

```

> Detail

https://www.fmz.com/strategy/474806

> Last Modified

2024-12-12 11:16:45
