
> Name

Multi-Indicator-Trend-Following-Strategy-with-Dynamic-Risk-Management

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1a3ae97a47ddd86becd.png)


#### Overview
This strategy is a comprehensive trend-following system that integrates multiple technical indicators, including Exponential Moving Averages (EMA), Relative Strength Index (RSI), Moving Average Convergence Divergence (MACD), and Bollinger Bands (BB). The strategy incorporates dynamic risk management with percentage-based stop-loss and risk-reward ratio-based take-profit levels, aiming to achieve stable risk-adjusted returns.

#### Strategy Principles
The core logic is based on multi-dimensional market analysis:
1. Trend Confirmation: Uses 200-day EMA for long-term trend direction, with fast EMA (20-day) and slow EMA (50-day) crossovers confirming medium-term trend changes
2. Momentum Verification: Employs dual confirmation with RSI and MACD, requiring RSI above 50 (long) or below 50 (short), along with supporting MACD signal line direction
3. Volatility Control: Utilizes Bollinger Bands for precise entry timing, seeking long opportunities at lower band support and short opportunities at upper band resistance
4. Risk Management: Implements 2% stop-loss and 1.5x risk-reward ratio take-profit levels to ensure controlled risk per trade

#### Strategy Advantages
1. Multi-dimensional Analysis: Combines trend, momentum, and volatility indicators to reduce false signals
2. Comprehensive Risk Control: Preset stop-loss and take-profit levels ensure risk manageability
3. High Adaptability: Strategy parameters can be adjusted for different market conditions
4. Clear Execution: Entry and exit conditions are well-defined and easy to monitor
5. Sound Money Management: Uses account equity percentage for position sizing to avoid excessive risk

#### Strategy Risks
1. Market Volatility Risk: May trigger frequent stop-losses during high volatility periods
2. Trend Reversal Risk: Potential for significant drawdowns at trend turning points
3. Parameter Optimization Risk: Over-optimization may lead to overfitting
4. Execution Slippage Risk: May face significant slippage in low liquidity conditions
5. Commission Cost Risk: Frequent trading may incur high transaction costs

#### Strategy Optimization Directions
1. Dynamic Parameter Adjustment: Automatically adjust indicator parameters based on market volatility
2. Add Market Sentiment Indicators: Incorporate volume indicators to enhance signal reliability
3. Optimize Stop-Loss Mechanism: Implement trailing stops to improve profit protection
4. Introduce Time Filters: Add trading time window filtering
5. Add Volatility Filters: Reduce position size or pause trading during excessive volatility

#### Summary
This strategy establishes a complete trend-following trading system through the comprehensive use of multiple technical indicators. With strict risk management and multi-dimensional market analysis, the strategy demonstrates good adaptability and stability. While there is room for optimization, the overall framework design is sound and suitable as a foundation for medium to long-term trading strategies. Successful implementation requires continuous monitoring and timely parameter adjustments to adapt to different market conditions.




> Source (PineScript)

``` pinescript
/*backtest
start: 2025-01-10 00:00:00
end: 2025-02-09 00:00:00
period: 2h
basePeriod: 2h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Altcoin Long/Short Strategy", overlay=true, initial_capital=1000, default_qty_type=strategy.percent_of_equity, default_qty_value=200, commission_type=strategy.commission.percent, commission_value=0.1)

// ------ Inputs ------
emaFastLength = input.int(20, "Fast EMA")
emaSlowLength = input.int(50, "Slow EMA")
rsiLength = input.int(14, "RSI Length")
bbLength = input.int(20, "Bollinger Bands Length")
riskRewardRatio = input.float(1.5, "Risk/Reward Ratio")
stopLossPerc = input.float(2, "Stop Loss %") / 100

// ------ Indicators ------
// Trend: EMAs
emaFast = ta.ema(close, emaFastLength)
emaSlow = ta.ema(close, emaSlowLength)
ema200 = ta.ema(close, 200)

// Momentum: RSI & MACD
rsi = ta.rsi(close, rsiLength)
[macdLine, signalLine, _] = ta.macd(close, 12, 26, 9)

// Volatility: Bollinger Bands
basis = ta.sma(close, bbLength)
dev = ta.stdev(close, bbLength)
upperBand = basis + 2 * dev
lowerBand = basis - 2 * dev

// ------ Strategy Logic ------
// Long Conditions
longCondition = 
  close > ema200 and // Long-term bullish
  ta.crossover(emaFast, emaSlow) and // EMA crossover
  rsi > 50 and // Momentum rising
  close > lowerBand and // Bounce from lower Bollinger Band
  macdLine > signalLine // MACD bullish

// Short Conditions
shortCondition = 
  close < ema200 and // Long-term bearish
  ta.crossunder(emaFast, emaSlow) and // EMA crossunder
  rsi < 50 and // Momentum weakening
  close < upperBand and // Rejection from upper Bollinger Band
  macdLine < signalLine // MACD bearish

// ------ Risk Management ------
stopLoss = strategy.position_avg_price * (1 - stopLossPerc)
takeProfit = strategy.position_avg_price * (1 + (riskRewardRatio * stopLossPerc))

// ------ Execute Trades ------
if (longCondition)
    strategy.entry("Long", strategy.long)
    strategy.exit("Exit Long", "Long", stop=stopLoss, limit=takeProfit)

if (shortCondition)
    strategy.entry("Short", strategy.short)
    strategy.exit("Exit Short", "Short", stop=stopLoss, limit=takeProfit)

// ------ Plotting ------
plot(emaFast, "Fast EMA", color=color.blue)
plot(emaSlow, "Slow EMA", color=color.orange)
plot(ema200, "200 EMA", color=color.gray)
plot(upperBand, "Upper Bollinger", color=color.red)
plot(lowerBand, "Lower Bollinger", color=color.green)
```

> Detail

https://www.fmz.com/strategy/481365

> Last Modified

2025-02-10 15:05:40
