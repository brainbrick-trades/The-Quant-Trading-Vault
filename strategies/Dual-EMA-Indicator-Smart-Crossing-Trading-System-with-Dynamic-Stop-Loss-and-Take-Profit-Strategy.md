
> Name

Dual-EMA-Indicator-Smart-Crossing-Trading-System-with-Dynamic-Stop-Loss-and-Take-Profit-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/12799ae70b811cbab66.png)


#### Overview
This strategy is an intelligent trading system based on dual moving average crossovers, utilizing 9-period and 21-period Exponential Moving Averages (EMA) as core indicators. The strategy incorporates a dynamic stop-loss and take-profit mechanism, automatically executing trading orders by monitoring EMA crossover signals in real-time. The system employs percentage-based trailing stops and fixed-ratio take-profit levels, ensuring both trading safety and profit potential.

#### Strategy Principles
The core logic operates on the crossover relationship between the fast EMA (9-period) and slow EMA (21-period). When the fast line crosses above the slow line, the system recognizes a bullish signal, automatically closes any short positions and opens long positions. When the fast line crosses below the slow line, the system identifies a bearish signal, closes any long positions and opens short positions. Additionally, the system implements dynamic stop-loss and take-profit mechanisms: for long positions, the stop-loss is set 5% below the entry price and take-profit 10% above; for short positions, the stop-loss is set 5% above the entry price and take-profit 10% below.

#### Strategy Advantages
1. Scientific indicator selection: EMA responds more sensitively to market changes, effectively capturing market trends
2. Comprehensive stop-loss and take-profit mechanism: Percentage-based settings allow flexible adjustment to different market conditions
3. High degree of automation: Fully automated from signal detection to trade execution, minimizing human intervention
4. Effective risk control: Clear stop-loss and take-profit levels for each trade
5. Clear code structure: Standardized variable naming and logical hierarchy, facilitating maintenance and optimization

#### Strategy Risks
1. Sideways market risk: Frequent crossover signals may occur in ranging markets, leading to excessive trading
2. Slippage risk: Potential discrepancies between theoretical and actual execution prices during high volatility
3. Money management risk: Fixed-ratio position sizing may lack flexibility in certain market conditions
4. Systemic risk: Stop-loss or take-profit orders may not execute timely in extreme market conditions

#### Optimization Directions
1. Implement trend filters: Add ADX or ATR indicators to assess trend strength and avoid frequent trading in ranging markets
2. Optimize stop-loss and take-profit mechanisms: Consider using ATR for dynamic adjustment of stop-loss and take-profit distances
3. Add time filters: Implement specific trading time restrictions to avoid highly volatile periods
4. Improve position sizing: Dynamically adjust position sizes based on market volatility
5. Add market sentiment indicators: Incorporate RSI or MACD for trade confirmation

#### Summary
This strategy represents a complete and logically sound automated trading system. Through EMA crossover signals combined with dynamic stop-loss and take-profit mechanisms, it can perform well in trending markets. However, users need to monitor market conditions, adjust parameters accordingly, and maintain proper risk control. Through continuous optimization and refinement, this strategy has the potential to become a stable and reliable trading tool.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-28 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("EMA Cross Strategy", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

// Add strategy parameter settings
var showLabels = input.bool(true, "Show Labels")
var stopLossPercent = input.float(5.0, "Stop Loss Percentage", minval=0.1, maxval=20.0, step=0.1)
var takeProfitPercent = input.float(10.0, "Take profit percentage", minval=0.1, maxval=50.0, step=0.1)

// CalculationEMA
ema9 = ta.ema(close, 9)
ema21 = ta.ema(close, 21)

// DrawEMALine
plot(ema9, "EMA9", color=color.blue, linewidth=2)
plot(ema21, "EMA21", color=color.red, linewidth=2)

// Detect Cross
crossOver = ta.crossover(ema9, ema21)  
crossUnder = ta.crossunder(ema9, ema21)

// Format time display (UTC+8)
utc8Time = time + 8 * 60 * 60 * 1000
timeStr = str.format("{0,date,MM-dd HH:mm}", utc8Time)

// Calculate stop loss and take profit prices
longStopLoss = strategy.position_avg_price * (1 - stopLossPercent / 100)
longTakeProfit = strategy.position_avg_price * (1 + takeProfitPercent / 100)
shortStopLoss = strategy.position_avg_price * (1 + stopLossPercent / 100)
shortTakeProfit = strategy.position_avg_price * (1 - takeProfitPercent / 100)

// Transaction logic
if crossOver
    if strategy.position_size < 0  // If holding a short position
        strategy.close("go short")     // Close Short Position First
    strategy.entry("go long", strategy.long)  // Open long position
    if showLabels
        label.new(bar_index, high, text="Long Entry\n" + timeStr, color=color.green, textcolor=color.white, style=label.style_label_down, yloc=yloc.abovebar)

if crossUnder
    if strategy.position_size > 0  // If holding a long position
        strategy.close("go long")     // Close Long Position First
    strategy.entry("go short", strategy.short)  // Open short position
    if showLabels
        label.new(bar_index, low, text="Short Entry\n" + timeStr, color=color.red, textcolor=color.white, style=label.style_label_up, yloc=yloc.belowbar)

// Set stop loss and take profit
if strategy.position_size > 0  // Stop loss and take profit for long position
    strategy.exit("Stop loss and take profit for long position", "go long", stop=longStopLoss, limit=longTakeProfit)
    
if strategy.position_size < 0  // Stop loss and take profit for a short position
    strategy.exit("Stop loss and take profit for a short position", "go short", stop=shortStopLoss, limit=shortTakeProfit) 
```

> Detail

https://www.fmz.com/strategy/473396

> Last Modified

2024-11-29 16:33:21
