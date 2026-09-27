
> Name

Dual-Direction-SMMA-Crossover-Strategy-with-ATR-Based-Risk-Management-and-Fixed-Take-Profit

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/cd8b0f81437a916c1a.png)


#### Overview
This is a dual-direction trend-following strategy based on SMMA (Smoothed Moving Average). The strategy generates long and short signals through price-SMMA crossovers, combining ATR-based dynamic stop-loss and fixed take-profit targets for risk and reward management. The strategy design is concise and effective, suitable for trend following across different timeframes.

#### Strategy Principles
The core mechanism relies on price crossovers with a 17-period SMMA to capture trend changes. Long positions are initiated when price crosses above SMMA, while short positions are taken when price crosses below SMMA. Exit management employs a triple mechanism: 1) ATR-based dynamic stop-loss set at 0.75 times ATR above/below SMMA; 2) Fixed take-profit targets of 1150 points for longs and 1500 points for shorts; 3) Reverse crossover signals for position closure. This combination both protects profits and allows trends to develop fully.

#### Strategy Advantages
1. Stable signal system: SMMA provides smoother signals compared to simple moving averages, effectively reducing false signals
2. Comprehensive risk management: Combines ATR-based dynamic stops with fixed profit targets, adapting to market volatility while securing reasonable profits
3. Dual-direction trading: Fully captures bilateral market opportunities, improving capital efficiency
4. High scalability: Clear strategy framework, easily implementable across different markets and timeframes
5. Clear operational rules: Objective entry and exit conditions minimize subjective interference

#### Strategy Risks
1. Choppy market risk: Frequent trades in ranging markets may lead to losses
2. Slippage risk: Fixed point profit targets may face slippage in fast markets
3. Trend reversal risk: ATR stops may not react quickly enough to sudden trend reversals
4. Parameter dependency: Strategy performance heavily relies on SMMA period and ATR multiplier choices
5. Money management risk: Fixed percentage position sizing may lack flexibility during volatility changes

#### Optimization Directions
1. Introduce trend strength filtering: Add indicators like ADX to screen for strong trends, reducing false signals in ranging markets
2. Dynamic profit targets: Consider using ATR to dynamically adjust profit targets for better market adaptation
3. Improved position sizing: Implement volatility-weighted position calculation for optimized capital efficiency
4. Multi-timeframe confirmation: Add longer timeframe trend confirmation to improve trade quality
5. Market environment adaptation: Include market type classification logic to adjust strategy parameters under different market conditions

#### Summary
This is a well-designed trend-following strategy that captures trends through SMMA crossovers, implements risk control using ATR, and manages profits with fixed targets. The strategy logic is clear, implementation is straightforward, with good operability and extensibility. While performance may suffer in ranging markets, the suggested optimization directions can further enhance strategy stability and adaptability. For traders who prefer trend following, this represents a noteworthy strategy framework.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-20 00:00:00
end: 2025-02-17 08:00:00
period: 4h
basePeriod: 4h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("SMMA 17 Crossover Strategy (Long & Short, ATR SL & Fixed TP)", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=200)

// ? SMMA Calculation
smmaLength = 17
smma = 0.0
smma := na(smma[1]) ? ta.sma(close, smmaLength) : (smma[1] * (smmaLength - 1) + close) / smmaLength

// ? ATR Calculation (For Dynamic Stop-Loss)
atrLength = 14
atr = ta.rma(ta.tr(true), atrLength)

// ? Long Entry Condition
longCondition = ta.crossover(close, smma)  // ✅ Price crosses above SMMA

// ? Long Exit Condition
longExit = ta.crossunder(close, smma)  // ✅ Price crosses below SMMA

// ? ATR-Based Stop-Loss (Dynamic) for Long
longStopLoss = smma - (atr * 0.75)  // ✅ Stop Loss below SMMA

// ? Fixed Take Profit for Long (1150 Points)
var float longEntryPrice = na
var float longTakeProfit = na
if longCondition
    longEntryPrice := close
    longTakeProfit := longEntryPrice + 1150  // ✅ TP 1150 points above entry

// ? Short Entry Condition
shortCondition = ta.crossunder(close, smma)  // ✅ Price crosses BELOW SMMA (Short trade)

// ? Short Exit Condition
shortExit = ta.crossover(close, smma)  // ✅ Price crosses ABOVE SMMA (Close Short trade)

// ? ATR-Based Stop-Loss (Dynamic) for Short
shortStopLoss = smma + (atr * 0.75)  // ✅ Stop Loss above SMMA

// ? Fixed Take Profit for Short (1500 Points) - Updated from 2000
var float shortEntryPrice = na
var float shortTakeProfit = na
if shortCondition
    shortEntryPrice := close
    shortTakeProfit := shortEntryPrice - 1500  // ✅ TP 1500 points below entry (Updated)

// ? Plot SMMA (For Visualization)
plot(smma, title="SMMA (17)", color=color.blue)

// ? Long Entry (Allow Multiple)
if longCondition
    strategy.entry("Long", strategy.long)

// ? Long Exit Conditions (Whichever Comes First)
strategy.exit("Long TP/SL", from_entry="Long", stop=longStopLoss, limit=longTakeProfit)
if longExit
    strategy.close("Long")

// ? Short Entry (Allow Multiple)
if shortCondition
    strategy.entry("Short", strategy.short)

// ? Short Exit Conditions (Whichever Comes First)
strategy.exit("Short TP/SL", from_entry="Short", stop=shortStopLoss, limit=shortTakeProfit)
if shortExit
    strategy.close("Short")

```

> Detail

https://www.fmz.com/strategy/482592

> Last Modified

2025-02-19 10:59:14
