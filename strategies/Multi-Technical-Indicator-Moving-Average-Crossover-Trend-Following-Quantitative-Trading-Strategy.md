
> Name

Multi-Technical-Indicator-Moving-Average-Crossover-Trend-Following-Quantitative-Trading-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d91cc78368b4a22d1e9f.png)
![IMG](https://www.fmz.com/upload/asset/2d84d87efd4458e512e10.png)





#### Overview
This strategy is a trend-following trading system based on multiple technical indicators, integrating Moving Average (MA), Relative Strength Index (RSI), Bollinger Bands (BB), Moving Average Convergence Divergence (MACD), and Stochastic oscillator. It identifies market trends and trading opportunities through cross-confirmation between indicators. The strategy employs percentage-based position management, using 1% of funds for each trade by default.

#### Strategy Principle
The strategy determines trading signals through the following dimensions:
1. Uses 14-period Simple Moving Average (SMA) as trend indicator baseline
2. RSI indicator for overbought/oversold conditions, with 30 and 70 as key thresholds
3. Bollinger Bands for price volatility range, with 20-period
4. MACD indicator (12,26,9) for trend confirmation
5. Stochastic oscillator (14,3) for momentum judgment

Long conditions must simultaneously satisfy:
- RSI below 30 (oversold)
- MACD line crosses above signal line
- Stochastic K value below 20
- Closing price above Bollinger Band middle line
- Previous closing price below Bollinger Band lower line

Short conditions must simultaneously satisfy:
- RSI above 70 (overbought)
- MACD line crosses below signal line
- Stochastic K value above 80
- Closing price below Bollinger Band middle line
- Previous closing price above Bollinger Band upper line

#### Strategy Advantages
1. Multiple technical indicator cross-confirmation effectively filters false signals
2. Combines trend-following and oscillating indicators, suitable for both trending and reversal markets
3. Percentage-based position management effectively controls risk
4. Adjustable indicator parameters provide good adaptability
5. Clear trading signals, easy to execute and backtest

#### Strategy Risks
1. Multiple indicators may lead to signal lag, affecting entry timing
2. Frequent trading in oscillating markets increases costs
3. Fixed parameters perform differently in various market environments
4. Technical indicators may contradict each other, causing signal confusion
Suggested risk mitigation measures:
- Dynamically adjust parameters based on different market characteristics
- Set stop-loss and take-profit levels to control risk
- Combine with other indicators like volume for signal confirmation
- Regularly evaluate strategy performance and adjust timely

#### Strategy Optimization Directions
1. Introduce adaptive parameter mechanism to dynamically adjust indicator parameters based on market volatility
2. Add volume indicators as auxiliary confirmation
3. Optimize position management, consider gradual position building and reduction
4. Add market environment recognition module to adopt different strategies in different market conditions
5. Introduce machine learning algorithms to optimize signal generation logic

#### Summary
This strategy establishes a relatively complete trend-following trading system through the comprehensive use of multiple technical indicators. The strategy features reliable signals and controllable risk, but still needs continuous parameter and logic optimization in live trading based on market conditions. Through continuous improvement and refinement, this strategy has the potential to achieve stable returns in different market environments.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-21 00:00:00
end: 2025-02-18 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"TRB_USDT"}]
*/

//@version=5
strategy("TradingBot Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=1)

// Input parameters
lotSize = input.float(0.1, title="Lot Size")
maPeriod = input.int(14, title="MA Period")
rsiPeriod = input.int(14, title="RSI Period")
bbPeriod = input.int(20, title="Bollinger Bands Period")
macdFast = input.int(12, title="MACD Fast EMA")
macdSlow = input.int(26, title="MACD Slow EMA")
macdSignal = input.int(9, title="MACD Signal SMA")
stochK = input.int(14, title="Stochastic %K")
stochD = input.int(3, title="Stochastic %D")

// Indicators
ma = ta.sma(close, maPeriod)
rsi = ta.rsi(close, rsiPeriod)
[bbUpper, bbMiddle, bbLower] = ta.bb(close, bbPeriod, 2)
[macdLine, signalLine, _] = ta.macd(close, macdFast, macdSlow, macdSignal)
k = ta.stoch(close, high, low, stochK)
d = ta.sma(k, stochD)

// Plot indicators
plot(ma, color=color.blue, title="MA", linewidth=1)
hline(70, "RSI Overbought", color=color.red)
hline(30, "RSI Oversold", color=color.green)
plot(rsi, color=color.purple, title="RSI", linewidth=1)
plot(bbUpper, color=color.orange, title="Bollinger Bands Upper", linewidth=1)
plot(bbMiddle, color=color.gray, title="Bollinger Bands Middle", linewidth=1)
plot(bbLower, color=color.orange, title="Bollinger Bands Lower", linewidth=1)
hline(0, "MACD Zero", color=color.gray)
plot(macdLine, color=color.blue, title="MACD Line", linewidth=1)
plot(signalLine, color=color.red, title="MACD Signal Line", linewidth=1)
hline(80, "Stochastic Overbought", color=color.red)
hline(20, "Stochastic Oversold", color=color.green)
plot(k, color=color.blue, title="Stochastic %K", linewidth=1)
plot(d, color=color.red, title="Stochastic %D", linewidth=1)

// Trading logic
longCondition = rsi < 30 and macdLine > signalLine and k < 20 and close > bbMiddle and close[1] < bbLower
shortCondition = rsi > 70 and macdLine < signalLine and k > 80 and close < bbMiddle and close[1] > bbUpper

if (longCondition)
    strategy.entry("Buy", strategy.long, qty=lotSize)
    label.new(bar_index, low, text="BUY", style=label.style_label_up, color=color.green, textcolor=color.white, size=size.small, yloc=yloc.belowbar)
if (shortCondition)
    strategy.entry("Sell", strategy.short, qty=lotSize)
    label.new(bar_index, high, text="SELL", style=label.style_label_down, color=color.red, textcolor=color.white, size=size.small, yloc=yloc.abovebar)
```

> Detail

https://www.fmz.com/strategy/482897

> Last Modified

2025-02-20 16:56:38
