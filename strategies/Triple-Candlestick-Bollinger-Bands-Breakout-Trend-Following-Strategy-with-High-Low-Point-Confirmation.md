
> Name

Triple-Candlestick-Bollinger-Bands-Breakout-Trend-Following-Strategy-with-High-Low-Point-Confirmation

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/9232be7eb2d2f5ae38.png)


#### Overview
This strategy is a trend-following trading system based on Bollinger Bands breakouts and candlestick patterns. It identifies trading signals through three consecutive candles breaking the Bollinger Bands, combined with the position of closing prices within the candlestick bodies. The system employs a fixed 1:1 risk-reward ratio for managing stop-loss and take-profit levels.

#### Strategy Principles
The core logic is based on the following key elements:
1. Uses 20-period Bollinger Bands as the primary indicator with a standard deviation multiplier of 2.0
2. Long entry conditions: three consecutive candles closing above the upper band, all being bullish with closes in the upper half of their ranges
3. Short entry conditions: three consecutive candles closing below the lower band, all being bearish with closes in the lower half of their ranges
4. Stop-loss is set at the extreme point of the earliest signal candle
5. Take-profit is set based on a 1:1 risk-reward ratio

#### Strategy Advantages
1. Employs multiple confirmation mechanisms through consecutive breakout candles, effectively reducing false breakout risks
2. Enhances trend confirmation reliability by considering closing price positions within candle bodies
3. Uses fixed risk-reward ratio for position management, facilitating risk control
4. Clear and easy-to-understand strategy logic
5. Intuitive signal visualization through markers for backtest analysis

#### Strategy Risks
1. May generate frequent false signals in ranging markets
2. Fixed risk-reward ratio might not fully capture strong trends
3. Strict three-candle requirement may miss potential opportunities
4. Stop-loss placement at signal candle extremes may be too wide in volatile conditions
Risk management suggestions:
- Adjust Bollinger Bands parameters based on market volatility cycles
- Dynamically adjust risk-reward ratio according to market characteristics
- Add trend confirmation indicators
- Optimize stop-loss placement method

#### Strategy Optimization Directions
1. Parameter Optimization:
- Dynamically adjust Bollinger Bands period and standard deviation multiplier based on market characteristics
- Consider changing three-candle requirement to dynamic judgment

2. Signal Optimization:
- Add trend confirmation indicators like ADX or trendlines
- Introduce volume confirmation mechanism
- Consider adding oscillators as auxiliary indicators

3. Position Management Optimization:
- Implement dynamic risk-reward ratio settings
- Add money management module
- Consider scaled entry and exit mechanisms

4. Stop-Loss Optimization:
- Introduce trailing stop mechanism
- Set stop-loss distance based on ATR
- Consider time-based stops

#### Summary
This is a well-structured trend-following strategy with clear logic. Through multiple confirmation mechanisms using Bollinger Bands breakouts and candlestick patterns, it effectively reduces false signal risks. The fixed risk-reward ratio simplifies trade management but limits strategy flexibility. There is significant room for improvement through parameter optimization, additional confirmation indicators, and improved position management. Overall, it provides a practical basic strategy framework that can be further refined based on specific requirements.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-20 00:00:00
end: 2025-02-17 08:00:00
period: 12h
basePeriod: 12h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("Bollinger Band Strategy (Close Near High/Low Relative to Half Range)", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=200, pyramiding=0)

// Bollinger Bands
length = input.int(20, "BB Length")
mult = input.float(2.0, "BB StdDev")
basis = ta.sma(close, length)
upper_band = basis + mult * ta.stdev(close, length)
lower_band = basis - mult * ta.stdev(close, length)

// Plot Bollinger Bands
plot(upper_band, "Upper Band", color.blue)
plot(lower_band, "Lower Band", color.red)

// Buy Condition: 
// 1. Last 3 candles close above upper band AND close > open for all 3 candles
// 2. Close is in the top half of the candle's range (close > (high + low) / 2)
buyCondition =    close[2] > upper_band[2] and     close[1] > upper_band[1] and     close > upper_band and    close[2] > open[2] and close[2] > (high[2] + low[2]) / 2 and    close[1] > open[1] and close[1] > (high[1] + low[1]) / 2 and    close > open and close > (high + low) / 2

// Sell Condition: 
// 1. Last 3 candles close below lower band AND close < open for all 3 candles
// 2. Close is in the bottom half of the candle's range (close < (high + low) / 2)
sellCondition =    close[2] < lower_band[2] and    close[1] < lower_band[1] and   close < lower_band and   close[2] < open[2] and close[2] < (high[2] + low[2]) / 2 and    close[1] < open[1] and close[1] < (high[1] + low[1]) / 2 and    close < open and close < (high + low) / 2

// Initialize variables
var float stop_loss = na
var float target_price = na

// Buy Logic
if buyCondition and strategy.position_size == 0
    stop_loss := low[2] // Low of the earliest candle in the 3-candle sequence
    target_price := close + (close - stop_loss) // Risk-to-reward 1:1
    strategy.entry("Buy", strategy.long)
    strategy.exit("Exit Buy", "Buy", stop=stop_loss, limit=target_price)
    label.new(bar_index, low, "▲", color=color.green, style=label.style_label_up, yloc=yloc.belowbar)

// Sell Logic
if sellCondition and strategy.position_size == 0
    stop_loss := high[2] // High of the earliest candle in the 3-candle sequence
    target_price := close - (stop_loss - close) // Risk-to-reward 1:1
    strategy.entry("Sell", strategy.short)
    strategy.exit("Exit Sell", "Sell", stop=stop_loss, limit=target_price)
    label.new(bar_index, high, "▼", color=color.red, style=label.style_label_down, yloc=yloc.abovebar)

// Plotting
plot(upper_band, "Upper Band", color.blue)
plot(lower_band, "Lower Band", color.red)
plot(strategy.position_size > 0 ? stop_loss : na, "Buy SL", color.red, 2, plot.style_linebr)
plot(strategy.position_size > 0 ? target_price : na, "Buy Target", color.green, 2, plot.style_linebr)
plot(strategy.position_size < 0 ? stop_loss : na, "Sell SL", color.red, 2, plot.style_linebr)
plot(strategy.position_size < 0 ? target_price : na, "Sell Target", color.green, 2, plot.style_linebr)
```

> Detail

https://www.fmz.com/strategy/482595

> Last Modified

2025-02-19 11:05:11
