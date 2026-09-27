
> Name

Multi-Period-Moving-Average-and-RSI-Momentum-Cross-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/17beca50a5fda298267.png)


#### Overview
This strategy is a quantitative trading system that combines Simple Moving Averages (SMA) and Relative Strength Index (RSI). It determines trading opportunities by observing the crossover signals of short-term and long-term moving averages while considering RSI overbought and oversold levels. The strategy is written in Pine Script for the TradingView platform, enabling automated trading and graphical display.

#### Strategy Principles
The core logic is based on the combination of two main technical indicators. First, the system calculates 50-period and 200-period Simple Moving Averages (SMA), using their crossovers as primary trend signals. Second, it incorporates a 14-period RSI indicator with 70 and 30 as overbought and oversold thresholds to filter trading signals. A long position is initiated when the short-term MA crosses above the long-term MA and RSI is below the overbought level. The position is closed when the short-term MA crosses below the long-term MA and RSI is above the oversold level.

#### Strategy Advantages
1. High Signal Reliability: By combining trend (SMA) and momentum (RSI) indicators, the strategy effectively reduces false breakout risks.
2. Strong Parameter Adaptability: The strategy offers multiple adjustable parameters, including MA periods, RSI period, and thresholds, facilitating optimization for different market conditions.
3. Clear Visual Feedback: Trading signals are clearly displayed on the chart, including different colored moving averages and text-annotated buy/sell markers.
4. High Automation Level: Supports fully automated trading without manual intervention.

#### Strategy Risks
1. Trend Reversal Risk: The lagging nature of moving averages may lead to significant drawdowns during sharp market reversals.
2. Sideways Market Risk: Frequent MA crossovers during consolidation periods may generate excessive false signals.
3. Parameter Sensitivity: Different parameter settings can significantly affect strategy performance, requiring thorough historical testing.

#### Strategy Optimization Directions
1. Add Trend Strength Filter: Incorporate indicators like ADX to open positions only during clear trends.
2. Implement Stop Loss: Set stop-loss conditions based on ATR or fixed percentages to control individual trade risk.
3. Optimize Exit Mechanism: Consider early exits when RSI reaches extreme values or combine with other technical indicators.
4. Include Volume Confirmation: Integrate volume analysis to enhance signal reliability when generating trade signals.

#### Summary
This strategy constructs a relatively robust trading system through the dual filtering mechanism of MA crossovers and RSI overbought/oversold levels. It is suitable for trending markets but requires parameter adjustment based on specific market characteristics. The strategy's stability can be further enhanced by adding more filtering conditions and risk control mechanisms. Before live trading, it is recommended to conduct thorough backtesting and optimize parameters according to actual market conditions.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-27 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Chỉ báo Giao dịch Cắt SMA với RSI", overlay=true)

// Định nghĩa các tham số
short_period = input.int(50, title="Thời gian SMA ngắn")
long_period = input.int(200, title="Thời gian SMA dài")
rsi_period = input.int(14, title="Thời gian RSI")
rsi_overbought = input.int(70, title="Ngưỡng RSI Mua Quá Mức")
rsi_oversold = input.int(30, title="Ngưỡng RSI Bán Quá Mức")

// Tính toán các SMA
sma_short = ta.sma(close, short_period)
sma_long = ta.sma(close, long_period)

// Tính toán RSI
rsi = ta.rsi(close, rsi_period)

// Điều kiện vào lệnh Mua (Cắt lên và RSI không quá mua)
long_condition = ta.crossover(sma_short, sma_long) and rsi < rsi_overbought

// Điều kiện vào lệnh Bán (Cắt xuống và RSI không quá bán)
short_condition = ta.crossunder(sma_short, sma_long) and rsi > rsi_oversold

// Vẽ các đường SMA và RSI lên biểu đồ
plot(sma_short, color=color.blue, title="SMA Ngắn")
plot(sma_long, color=color.red, title="SMA Dài")
hline(rsi_overbought, "Overbought", color=color.red)
hline(rsi_oversold, "Oversold", color=color.green)
plot(rsi, color=color.orange, title="RSI")

// Hiển thị tín hiệu vào lệnh
plotshape(series=long_condition, location=location.belowbar, color=color.green, style=shape.labelup, title="Tín hiệu Mua", text="MUA")
plotshape(series=short_condition, location=location.abovebar, color=color.red, style=shape.labeldown, title="Tín hiệu Bán", text="BÁN")

// Giao dịch tự động bằng cách sử dụng cấu trúc if
if (long_condition)
    strategy.entry("Long", strategy.long)

if (short_condition)
    strategy.close("Long")



```

> Detail

https://www.fmz.com/strategy/473245

> Last Modified

2024-11-28 15:39:23
