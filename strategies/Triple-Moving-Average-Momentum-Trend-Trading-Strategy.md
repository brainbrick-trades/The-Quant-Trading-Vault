
> Name

Triple-Moving-Average-Momentum-Trend-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/167f5b47f7de70a374a.png)


#### Overview
This is a triple moving average trend following strategy based on Oliver Valez's trading methodology. The strategy utilizes 20-period, 50-period, and 200-period moving averages to identify market trends and trading opportunities. The 200-period MA serves as the primary trend filter, while crossovers between the 20-period and 50-period MAs generate specific trading signals. The strategy includes built-in risk management features with stop-loss and take-profit settings.

#### Strategy Principles
The core logic consists of three key aspects:
1. Trend Identification: Uses the 200-period MA as a trend boundary. When price is above the 200 MA, an uptrend is confirmed; when below, a downtrend is confirmed.
2. Trading Signals: In uptrends, long entries are triggered when the 20-period MA crosses above the 50-period MA; in downtrends, short entries occur when the 20-period MA crosses below the 50-period MA.
3. Risk Control: The strategy implements a default 2% stop-loss and 4% take-profit, with automatic position closure on reverse crossover signals.

#### Strategy Advantages
1. Multiple Confirmation System: The combination of three moving averages provides more reliable trading signals.
2. Trend Filtering: The 200 MA trend filter effectively reduces false breakout risks.
3. High Flexibility: Supports switching between SMA and EMA, with adjustable parameters for different market characteristics.
4. Comprehensive Risk Management: Built-in stop-loss and take-profit mechanisms protect capital.
5. Visual Enhancement: Trend status is intuitively displayed through background color changes.

#### Strategy Risks
1. Lag Effect: Moving averages are inherently lagging indicators, potentially causing delayed entries or exits.
2. Poor Performance in Ranging Markets: Frequent MA crossovers during consolidation periods may generate false signals.
3. Fixed Stop-Loss Risk: Using fixed percentage stops may not suit all market conditions.
4. Parameter Sensitivity: Different MA period settings can produce significantly different results.

#### Optimization Directions
1. Incorporate Volume Analysis: Add volume confirmation indicators to improve signal reliability.
2. Dynamic Stop-Loss: Consider using ATR or volatility indicators for dynamic stop-loss adjustment.
3. Add Trend Strength Filtering: Introduce ADX or other trend strength indicators to filter weak trend environments.
4. Optimize Entry Timing: Integrate price patterns and support/resistance levels for more precise entries.
5. Include Time Filtering: Set trading time windows to avoid highly volatile periods.

#### Summary
This is a well-structured trend following strategy with clear logic. The coordination of triple moving averages ensures accurate trend identification while providing definitive trading signals. While the strategy's risk management mechanisms are relatively comprehensive, there is room for optimization. Traders are advised to conduct thorough backtesting before live implementation and adjust parameters according to specific trading instrument characteristics.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-10 00:00:00
end: 2025-02-08 08:00:00
period: 2d
basePeriod: 2d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Oliver Valez Triple MA Strategy", overlay=true, margin_long=100, margin_short=100)

// Inputs
ma20_length = input.int(20, "20-period MA Length", minval=1)
ma50_length = input.int(50, "50-period MA Length", minval=1)
ma200_length = input.int(200, "200-period MA Length", minval=1)
use_ema = input.bool(false, "Use EMA Instead of SMA")
sl_percent = input.float(2.0, "Stop Loss %", minval=0.0)
tp_percent = input.float(4.0, "Take Profit %", minval=0.0)

// Calculate MAs
ma20 = use_ema ? ta.ema(close, ma20_length) : ta.sma(close, ma20_length)
ma50 = use_ema ? ta.ema(close, ma50_length) : ta.sma(close, ma50_length)
ma200 = use_ema ? ta.ema(close, ma200_length) : ta.sma(close, ma200_length)

// Plot MAs
plot(ma20, "MA 20", color=color.new(color.blue, 0), linewidth=2)
plot(ma50, "MA 50", color=color.new(color.orange, 0), linewidth=2)
plot(ma200, "MA 200", color=color.new(color.red, 0), linewidth=2)

// Trend Filter
bullish_trend = close > ma200
bearish_trend = close < ma200

// Entry Conditions
long_condition = ta.crossover(ma20, ma50) and bullish_trend
short_condition = ta.crossunder(ma20, ma50) and bearish_trend

// Exit Conditions
exit_long = ta.crossunder(ma20, ma50)
exit_short = ta.crossover(ma20, ma50)

// Risk Management
stop_loss = strategy.position_avg_price * (1 - sl_percent/100)
take_profit = strategy.position_avg_price * (1 + tp_percent/100)

// Execute Trades
if (long_condition)
    strategy.entry("Long", strategy.long)
    strategy.exit("XL", "Long", stop=stop_loss, limit=take_profit)

if (short_condition)
    strategy.entry("Short", strategy.short)
    strategy.exit("XS", "Short", stop=stop_loss, limit=take_profit)

// Close trades on opposite signals
if (exit_long)
    strategy.close("Long")

if (exit_short)
    strategy.close("Short")

// Plot Signals
plotshape(long_condition, "Buy", shape.labelup, location.belowbar, color=color.green, text="BUY", textcolor=color.white)
plotshape(short_condition, "Sell", shape.labeldown, location.abovebar, color=color.red, text="SELL", textcolor=color.white)

// Background Color for Trend
bgcolor(bullish_trend ? color.new(color.green, 90) : bearish_trend ? color.new(color.red, 90) : na)
```

> Detail

https://www.fmz.com/strategy/481350

> Last Modified

2025-02-10 14:37:15
