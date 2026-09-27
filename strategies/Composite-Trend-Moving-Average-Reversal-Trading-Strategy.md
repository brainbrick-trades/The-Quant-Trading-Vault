
> Name

Composite-Trend-Moving-Average-Reversal-Trading-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d876626a959ab419cb5e.png)
![IMG](https://www.fmz.com/upload/asset/2d8a85774a5dd50871e9b.png)






#### Overview
This strategy is a trend following and reversal trading system based on composite moving averages. It identifies trading opportunities by combining moving averages of different periods and monitoring price reactions to these averages. The core concept involves observing the relationship between price and moving averages, and trading based on price reactions at specific threshold levels.

#### Strategy Principle
The strategy employs various types of moving averages (EMA, TEMA, DEMA, WMA, SMA) and combines two different periods (default 20 and 30) through weighted or arithmetic averaging to construct a composite moving average. An uptrend is identified when price is above the average, and a downtrend when below. The strategy waits for price pullbacks near the moving average (controlled by a reaction percentage parameter) after a trend is established. Specifically, in an uptrend, it opens long positions when price pulls back below a specific percentage of the average and closes above it; in a downtrend, it opens short positions when price rebounds above a specific percentage and closes below the average.

#### Strategy Advantages
1. The system demonstrates good adaptability, supporting multiple types of moving averages to suit different market characteristics.
2. The composite moving average approach effectively reduces false signals that might occur with single-period averages.
3. The inclusion of a reaction percentage concept avoids simple moving average crossover trades, improving trading reliability.
4. Waiting for pullbacks in established trends allows for better entry prices.

#### Strategy Risks
1. May generate frequent false signals in choppy markets, increasing trading costs.
2. The lag inherent in composite moving averages can delay entry and exit timing.
3. Fixed reaction percentages may need adjustment in different market environments.
4. Significant drawdowns may occur during rapid trend transitions.

#### Strategy Optimization Directions
1. Incorporate volatility indicators to dynamically adjust reaction percentages for better market adaptation.
2. Add volume factors to confirm price reversal validity.
3. Implement stop-loss and take-profit mechanisms for better risk control.
4. Add trend strength evaluation for more aggressive parameter settings in strong trends.
5. Consider market environment analysis for different parameter combinations in various market conditions.

#### Summary
This strategy combines trend following and reversal trading concepts, capturing opportunities through composite moving averages and price reaction mechanisms. Its core strengths lie in flexibility and false signal filtering capability, though parameter optimization across different market environments requires attention. With proper risk control and continuous improvement, the strategy shows potential for stable returns in practical trading.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-10-01 00:00:00
end: 2025-02-18 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Ultrajante MA Reaction Strategy", overlay=true, initial_capital=10000, 
     default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// ===== Custom Functions for DEMA and TEMA =====
dema(src, length) =>
    ema1 = ta.ema(src, length)
    ema2 = ta.ema(ema1, length)
    2 * ema1 - ema2

tema(src, length) =>
    ema1 = ta.ema(src, length)
    ema2 = ta.ema(ema1, length)
    ema3 = ta.ema(ema2, length)
    3 * ema1 - 3 * ema2 + ema3

// ===== Configuration Parameters =====

// MA Type Selection
maType = input.string(title="MA Type", defval="EMA", options=["SMA", "EMA", "WMA", "DEMA", "TEMA"])

// Parameters for composite periods
periodA = input.int(title="Period A", defval=20, minval=1)
periodB = input.int(title="Period B", defval=30, minval=1)
compMethod = input.string(title="Composite Method", defval="Average", options=["Average", "Weighted"])

// Reaction percentage (e.g., 0.5 means 0.5%)
reactionPerc = input.float(title="Reaction %", defval=0.5, step=0.1)

// ===== Composite Period Calculation =====
compPeriod = compMethod == "Average" ? math.round((periodA + periodB) / 2) : math.round((periodA * 0.6 + periodB * 0.4))

// ===== Moving Average Calculation based on selected type =====
ma = switch maType
    "SMA"  => ta.sma(close, compPeriod)
    "EMA"  => ta.ema(close, compPeriod)
    "WMA"  => ta.wma(close, compPeriod)
    "DEMA" => dema(close, compPeriod)
    "TEMA" => tema(close, compPeriod)
    => ta.ema(close, compPeriod)  // Default value

plot(ma, color=color.blue, title="MA")

// ===== Trend Definition =====
trendUp = close > ma
trendDown = close < ma

// ===== Reaction Threshold Calculation =====
// In uptrend: expect the price to retrace to or below a value close to the MA
upThreshold = ma * (1 - reactionPerc / 100)
// In downtrend: expect the price to retrace to or above a value close to the MA
downThreshold = ma * (1 + reactionPerc / 100)

// ===== Quick Reaction Detection =====
// For uptrend: reaction is detected if the low is less than or equal to the threshold and the close recovers and stays above the MA
upReaction = trendUp and (low <= upThreshold) and (close > ma)
// For downtrend: reaction is detected if the high is greater than or equal to the threshold and the close stays below the MA
downReaction = trendDown and (high >= downThreshold) and (close < ma)

// ===== Trade Execution =====
if upReaction
    // Close short position if exists and open long position
    strategy.close("Short", comment="Close Short due to Bullish Reaction")
    strategy.entry("Long", strategy.long, comment="Long Entry due to Bullish Reaction in Uptrend")

if downReaction
    // Close long position if exists and open short position
    strategy.close("Long", comment="Close Long due to Bearish Reaction")
    strategy.entry("Short", strategy.short, comment="Short Entry due to Bearish Reaction in Downtrend")

// ===== Visualization of Reactions on the Chart =====
plotshape(upReaction, title="Bullish Reaction", style=shape.arrowup, location=location.belowbar, color=color.green, size=size.small, text="Long")
plotshape(downReaction, title="Bearish Reaction", style=shape.arrowdown, location=location.abovebar, color=color.red, size=size.small, text="Short")

```

> Detail

https://www.fmz.com/strategy/482906

> Last Modified

2025-02-27 17:23:21
