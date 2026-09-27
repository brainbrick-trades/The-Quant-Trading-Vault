
> Name

Dynamic-Dual-Moving-Average-Breakthrough-Trading-System-Dynamic-Dual-Moving-Average-Breakthrough-Trading-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/6201eca6ab89694b39.png)


#### Overview
This is an automated trading strategy system based on dual moving average crossover. The system utilizes 9-period and 21-period Exponential Moving Averages (EMA) as core indicators, generating trading signals through their crossovers. It incorporates stop-loss and take-profit management, along with a visual interface that displays trading signals and key price levels.

#### Strategy Principle
The strategy employs a fast EMA (9-period) and a slow EMA (21-period) to construct the trading system. Long signals are generated when the fast EMA crosses above the slow EMA, while short signals occur when the fast EMA crosses below the slow EMA. The system automatically sets stop-loss and take-profit levels based on preset percentages for each trade. Position sizing uses a percentage-based approach, defaulting to 100% of account equity.

#### Strategy Advantages
1. Clear Signals: Uses moving average crossovers as trading signals, which are clear and easy to understand
2. Risk Control: Integrated stop-loss and take-profit management system for every trade
3. Visual Support: Provides trade label display featuring entry time, price, stop-loss, and take-profit levels
4. Flexible Parameters: Allows adjustment of EMA periods and risk management parameters to adapt to different market conditions
5. Complete Exit Mechanism: Automatically closes positions on contrary signals to avoid position offsetting

#### Strategy Risks
1. Choppy Market Risk: May generate frequent false breakout signals in sideways markets, leading to consecutive losses
2. Slippage Risk: Actual execution prices may deviate from intended levels during high volatility periods
3. Position Sizing Risk: Default 100% equity allocation may expose the account to excessive risk
4. Signal Lag: EMAs inherently lag price action, potentially missing optimal entry points or causing delayed exits
5. Single Indicator Dependency: Reliance solely on moving average crossovers may ignore other important market information

#### Optimization Directions
1. Add Trend Confirmation: Consider incorporating ADX or trend strength indicators to filter false signals
2. Improve Money Management: Add dynamic position sizing based on market volatility
3. Enhanced Stop-Loss Mechanism: Consider implementing trailing stops to better protect profits
4. Market Environment Filtering: Add volatility indicators to suspend trading in unfavorable conditions
5. Optimize Signal Confirmation: Consider adding volume confirmation or complementary technical indicators

#### Summary
This is a well-designed, logically sound moving average crossover strategy system. By combining EMA crossover signals with risk management mechanisms, the strategy can capture profits in trending markets. While inherent risks exist, the suggested optimizations can further enhance the strategy's stability and reliability. This strategy is particularly suitable for tracking medium to long-term trends and represents a solid choice for patient traders.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-04 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
//
//  ██╗         █████╗         ██████╗     ██████╗     ██╗   ██╗    ██╗
//  ██║        ██╔══██╗       ██╔═══██╗    ██╔══██╗    ██║   ██║    ██║
//  ██║        ███████║       ██║   ██║    ██║  ██║    ██║   ██║    ██║
//  ██║        ██╔══██║       ██║   ██║    ██║  ██║    ██║   ██║    ██║
//  ███████╗   ██║  ██║       ╚██████╔╝    ██████╔╝    ╚██████╔╝    ██║
//  ╚══════╝   ╚═╝  ╚═╝        ╚═════╝     ╚═════╝      ╚═════╝     ╚═╝
//
//  BTC-EMALong Strategy(5Minute Confirmation Version) - Author:LAODUI
//  Version:2.0
//  Last Update:2024
// ═══════════════════════════════════════════════════════════════════════════

strategy("EMA Cross Strategy", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

// Add strategy parameter settings
var showLabels = input.bool(true, "Show Labels", group="Display Settings")
var stopLossPercent = input.float(5.0, "Stop Loss Percentage", minval=0.1, maxval=20.0, step=0.1, group="Risk Management")
var takeProfitPercent = input.float(10.0, "Take profit percentage", step=0.1, group="Risk Management")

// EMAParameter Settings
var emaFastLength = input.int(9, "FastEMAtimeframe", minval=1, maxval=200, group="EMASettings")
var emaSlowLength = input.int(21, "SlowEMAtimeframe", minval=1, maxval=200, group="EMASettings")

// CalculationEMA
ema_fast = ta.ema(close, emaFastLength)
ema_slow = ta.ema(close, emaSlowLength)

// DrawEMALine
plot(ema_fast, "FastEMA", color=color.blue, linewidth=2)
plot(ema_slow, "SlowEMA", color=color.red, linewidth=2)

// Detect Cross
crossOver = ta.crossover(ema_fast, ema_slow)  
crossUnder = ta.crossunder(ema_fast, ema_slow)

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
    if strategy.position_size < 0  
        strategy.close("go short")     
    strategy.entry("go long", strategy.long)  
    if showLabels
        label.new(bar_index, high, text="Long Entry\n" + timeStr + "\nEntry price: " + str.tostring(close) + "\nStop loss price: " + str.tostring(longStopLoss) + "\nTake-profit price: " + str.tostring(longTakeProfit), color=color.green, textcolor=color.white, style=label.style_label_down, yloc=yloc.abovebar)

if crossUnder
    if strategy.position_size > 0  
        strategy.close("go long")     
    strategy.entry("go short", strategy.short)  
    if showLabels
        label.new(bar_index, low, text="Short Entry\n" + timeStr + "\nEntry price: " + str.tostring(close) + "\nStop loss price: " + str.tostring(shortStopLoss) + "\nTake-profit price: " + str.tostring(shortTakeProfit), color=color.red, textcolor=color.white, style=label.style_label_up, yloc=yloc.belowbar)

// Set stop loss and take profit
if strategy.position_size > 0  // Stop loss and take profit for long position
    strategy.exit("Stop loss and take profit for long position", "go long", stop=longStopLoss, limit=longTakeProfit)
    
if strategy.position_size < 0  // Stop loss and take profit for a short position
    strategy.exit("Stop loss and take profit for a short position", "go short", stop=shortStopLoss, limit=shortTakeProfit) 
```

> Detail

https://www.fmz.com/strategy/474051

> Last Modified

2024-12-05 16:22:32
