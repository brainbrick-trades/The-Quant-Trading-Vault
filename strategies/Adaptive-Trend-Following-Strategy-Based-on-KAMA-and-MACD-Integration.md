
> Name

Adaptive-Trend-Following-Strategy-Based-on-KAMA-and-MACD-Integration

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d84f912c1386464ecb08.png)
![IMG](https://www.fmz.com/upload/asset/2d82c0bb83b573432666b.png)




#### Overview
This strategy is a trend-following system that combines the Kaufman Adaptive Moving Average (KAMA) with MACD. It uses KAMA as the primary trend indicator and MACD as momentum confirmation, achieving intelligent trend tracking and precise trade timing. The strategy operates on a 4-hour timeframe with dynamic stop-loss and take-profit targets for risk management.

#### Strategy Principles
The core logic is based on the following key components:
1. KAMA Calculation: Uses a 50-period KAMA as the main trend indicator, dynamically adjusting the smoothing coefficient through efficiency ratio to better adapt to market conditions.
2. MACD Confirmation: Employs slower settings (26,52,18) for MACD as trend confirmation, ensuring trade direction aligns with overall momentum.
3. ATR Stops: Uses 3 times the 14-period ATR for calculating dynamic stop-loss and take-profit levels.
4. Trading Rules:
   - Long Entry: Price crosses above KAMA with bullish MACD
   - Exit: Price crosses below KAMA with bearish MACD
   - Risk Management: Dynamic stop-loss and take-profit based on ATR

#### Strategy Advantages
1. High Adaptability: KAMA automatically adjusts sensitivity based on market efficiency, maintaining good performance across different market conditions.
2. Reliable Signals: MACD confirmation significantly reduces false breakout risks.
3. Comprehensive Risk Management: Volatility-based dynamic stops and targets provide adaptive risk control.
4. Extensive Parameter Optimization Space: Key parameters can be adjusted for different market characteristics.

#### Strategy Risks
1. Trend Reversal Risk: May generate false signals in highly volatile markets.
2. Lag Risk: Both KAMA and MACD have inherent lag, potentially missing optimal entry points.
3. Parameter Sensitivity: Different market conditions may require parameter adjustments.
4. Transaction Cost Impact: Frequent trading may lead to high transaction costs.

#### Optimization Directions
1. Implement market volatility filter to adjust parameters or pause trading in high volatility environments.
2. Add volume analysis indicators to improve trend identification accuracy.
3. Optimize MACD parameters for better alignment with 4-hour timeframe.
4. Implement adaptive stop-loss multiplier to dynamically adjust ATR multiplier based on market volatility.
5. Include time filters to avoid trading during low liquidity periods.

#### Summary
This is an innovative trend-following strategy that combines the classic technical indicators KAMA and MACD. Through the coordination of adaptive moving averages and momentum confirmation, along with a comprehensive risk management system, the strategy demonstrates strong practicality and stability. While it faces certain risks related to lag and parameter sensitivity, the suggested optimization directions can further enhance its robustness and profitability.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-20 00:00:00
end: 2025-02-18 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © mckat

//@version=5
strategy("4-Hour KAMA Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)
// === Inputs ===
ama_length = input.int(50, title="KAMA Length for 4H")
fast_length = input.int(3, title="KAMA Fast Length")
slow_length = input.int(30, title="KAMA Slow Length")
atr_length = input.int(14, title="ATR Length")
atr_mult = input.float(3.0, title="ATR Multiplier for Stop-Loss & Take-Profit")
// === KAMA Calculation ===
var float kama = na
price_change = math.abs(close - close[ama_length])
volatility_sum = 0.0
for i = 0 to ama_length - 1
    volatility_sum := volatility_sum + math.abs(close[i] - close[i + 1])
efficiency_ratio = price_change / volatility_sum
smoothing_constant = math.pow(efficiency_ratio * (2 / (fast_length + 1) - 2 / (slow_length + 1)) + 2 / (slow_length + 1), 2)
kama := na(kama[1]) ? close : kama[1] + smoothing_constant * (close - kama[1])
// Plot KAMA
plot(kama, color=color.blue, title="KAMA (50)")
// === ATR for Stop-Loss and Take-Profit ===
atr = ta.atr(atr_length)
stop_loss = close - atr * atr_mult
take_profit = close + atr * atr_mult
// === MACD for Momentum Confirmation (Slow Settings for 4H) ===
[macd_line, signal_line, _] = ta.macd(close, 26, 52, 18)
macd_bullish = macd_line > signal_line
macd_bearish = macd_line < signal_line
// === Entry and Exit Conditions ===
buy_condition = ta.crossover(close, kama) and macd_bullish
sell_condition = ta.crossunder(close, kama) and macd_bearish
// === Execute Trades ===
if (buy_condition)
    strategy.entry("Buy", strategy.long)
if (sell_condition)
    strategy.close("Buy")
// === Dynamic Stop-Loss and Take-Profit ===
strategy.exit("Exit", "Buy", stop=stop_loss, limit=take_profit)
// === Plot Signals ===
plotshape(series=buy_condition, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
plotshape(series=sell_condition, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")
```

> Detail

https://www.fmz.com/strategy/482779

> Last Modified

2025-02-20 15:01:37
