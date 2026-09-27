
> Name

Adaptive-Multi-Strategy-Dynamic-Switching-System-A-Quantitative-Trading-Strategy-Combining-Trend-Following-and-Range-Oscillation

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/6002d07812dc78fa36.png)


#### Overview
This strategy is an adaptive trading system that combines multiple technical analysis indicators and switches between different trading strategies by dynamically identifying market conditions. The system is primarily based on Moving Average (MA), Bollinger Bands (BB), and Relative Strength Index (RSI), automatically selecting the most suitable trading method according to market trends and range oscillation characteristics. The strategy implements differentiated risk management solutions for trending and ranging markets by setting different take-profit and stop-loss parameters.

#### Strategy Principle
The strategy uses 50-period and 20-period moving averages to determine market trends, combined with Bollinger Bands and RSI to identify overbought and oversold areas. In trending markets, the system mainly trades based on price relationship with the slow moving average and crossovers between fast and slow lines; in ranging markets, it primarily trades on Bollinger Bands breakouts and RSI overbought/oversold signals. The system automatically adjusts take-profit levels according to market conditions, using 6% for trending markets and 4% for ranging markets, with a uniform 2% stop-loss for risk control.

#### Strategy Advantages
1. Strong market adaptability: Automatically switches trading strategies based on different market environments, improving system stability
2. Comprehensive risk management: Applies different take-profit ratios for trending and ranging markets, better matching market characteristics
3. Multi-dimensional signal verification: Improves trading signal reliability through cross-validation of multiple technical indicators
4. High degree of automation: Fully automated operation without manual intervention, reducing errors from subjective judgment

#### Strategy Risks
1. Parameter sensitivity: Strategy performance is affected by the selection of multiple technical indicator parameters, requiring thorough parameter optimization
2. Market transition lag: Market state identification may have latency, affecting strategy performance
3. False signal risk: May generate false trading signals in volatile markets
4. Transaction cost considerations: Frequent strategy switching may result in high trading costs

#### Strategy Optimization Directions
1. Incorporate volume indicators: Add volume analysis to existing technical indicators to improve signal reliability
2. Optimize market state identification: Consider introducing trend strength indicators like ATR and ADX to improve market state judgment accuracy
3. Dynamic parameter adjustment: Automatically adjust take-profit and stop-loss parameters based on market volatility to improve strategy adaptability
4. Add filtering mechanisms: Design stricter trading conditions to reduce false signals

#### Summary
This strategy builds an adaptive trading system capable of adapting to different market environments by combining multiple classic technical indicators. While maintaining operational simplicity, the system achieves dynamic market state identification and automatic trading strategy switching, demonstrating strong practicality. Through differentiated take-profit and stop-loss settings, the strategy maintains good profitability while controlling risks. Strategy stability and reliability can be further enhanced by introducing more technical indicators and optimizing parameter adjustment mechanisms.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-17 00:00:00
end: 2025-01-16 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT","balance":49999}]
*/

//@version=6
strategy("Supply & Demand Test 1 - Enhanced", overlay=true)

// Inputs
ma_length = input.int(50, title="50-period Moving Average Length", minval=1)
ma_length_fast = input.int(20, title="20-period Moving Average Length", minval=1)
bb_length = input.int(20, title="Bollinger Bands Length", minval=1)
bb_std_dev = input.float(2.0, title="Bollinger Bands Std Dev", step=0.1)
rsi_length = input.int(14, title="RSI Length", minval=1)
stop_loss_percent = input.float(0.02, title="Stop Loss Percent", step=0.001, minval=0.001)
take_profit_trend = input.float(0.06, title="Take Profit Percent (Trend)", step=0.001, minval=0.001)
take_profit_range = input.float(0.04, title="Take Profit Percent (Range)", step=0.001, minval=0.001)

// Moving Averages
ma_slow = ta.sma(close, ma_length)
ma_fast = ta.sma(close, ma_length_fast)

// Bollinger Bands
bb_basis = ta.sma(close, bb_length)
bb_dev = ta.stdev(close, bb_length)
bb_upper = bb_basis + bb_std_dev * bb_dev
bb_lower = bb_basis - bb_std_dev * bb_dev

// RSI
rsi = ta.rsi(close, rsi_length)

// Market Conditions
is_trending_up = close > ma_slow
is_trending_down = close < ma_slow
is_range_bound = not (is_trending_up or is_trending_down)

// Entry Conditions
long_trend_entry = is_trending_up and close >= ma_slow * 1.02
short_trend_entry = is_trending_down and close <= ma_slow * 0.98
long_ma_crossover = ta.crossover(ma_fast, ma_slow)
short_ma_crossover = ta.crossunder(ma_fast, ma_slow)
long_range_entry = is_range_bound and close <= bb_lower * 0.97
short_range_entry = is_range_bound and close >= bb_upper * 1.03
long_rsi_entry = is_range_bound and rsi < 30
short_rsi_entry = is_range_bound and rsi > 70

// Entry and Exit Logic
if long_trend_entry
    strategy.entry("Long Trend", strategy.long)
    strategy.exit("Exit Long Trend", from_entry="Long Trend", stop=close * (1 - stop_loss_percent), limit=close * (1 + take_profit_trend))
    alert("Entered Long Trend", alert.freq_once_per_bar)

if short_trend_entry
    strategy.entry("Short Trend", strategy.short)
    strategy.exit("Exit Short Trend", from_entry="Short Trend", stop=close * (1 + stop_loss_percent), limit=close * (1 - take_profit_trend))
    alert("Entered Short Trend", alert.freq_once_per_bar)

if long_ma_crossover
    strategy.entry("Long MA Crossover", strategy.long)
    strategy.exit("Exit Long MA Crossover", from_entry="Long MA Crossover", stop=close * (1 - stop_loss_percent), limit=close * (1 + take_profit_trend))
    alert("Entered Long MA Crossover", alert.freq_once_per_bar)

if short_ma_crossover
    strategy.entry("Short MA Crossover", strategy.short)
    strategy.exit("Exit Short MA Crossover", from_entry="Short MA Crossover", stop=close * (1 + stop_loss_percent), limit=close * (1 - take_profit_trend))
    alert("Entered Short MA Crossover", alert.freq_once_per_bar)

if long_range_entry
    strategy.entry("Long Range", strategy.long)
    strategy.exit("Exit Long Range", from_entry="Long Range", stop=close * (1 - stop_loss_percent), limit=close * (1 + take_profit_range))
    alert("Entered Long Range", alert.freq_once_per_bar)

if short_range_entry
    strategy.entry("Short Range", strategy.short)
    strategy.exit("Exit Short Range", from_entry="Short Range", stop=close * (1 + stop_loss_percent), limit=close * (1 - take_profit_range))
    alert("Entered Short Range", alert.freq_once_per_bar)

if long_rsi_entry
    strategy.entry("Long RSI", strategy.long)
    strategy.exit("Exit Long RSI", from_entry="Long RSI", stop=close * (1 - stop_loss_percent), limit=close * (1 + take_profit_range))
    alert("Entered Long RSI", alert.freq_once_per_bar)

if short_rsi_entry
    strategy.entry("Short RSI", strategy.short)
    strategy.exit("Exit Short RSI", from_entry="Short RSI", stop=close * (1 + stop_loss_percent), limit=close * (1 - take_profit_range))
    alert("Entered Short RSI", alert.freq_once_per_bar)

// Plotting
plot(ma_slow, color=color.blue, title="50-period MA")
plot(ma_fast, color=color.orange, title="20-period MA")
plot(bb_upper, color=color.red, title="Bollinger Upper")
plot(bb_lower, color=color.green, title="Bollinger Lower")
plot(bb_basis, color=color.gray, title="Bollinger Basis")
hline(70, "Overbought (RSI)", color=color.red, linestyle=hline.style_dotted)
hline(30, "Oversold (RSI)", color=color.green, linestyle=hline.style_dotted)

```

> Detail

https://www.fmz.com/strategy/478725

> Last Modified

2025-01-17 16:02:23
