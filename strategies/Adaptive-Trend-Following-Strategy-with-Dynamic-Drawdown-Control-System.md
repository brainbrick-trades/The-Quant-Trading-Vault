
> Name

Adaptive-Trend-Following-Strategy-with-Dynamic-Drawdown-Control-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1351ef9e99eaaf385ef.png)


#### Overview
This strategy is a comprehensive trading system that combines trend following with risk control. It utilizes a 200-period Exponential Moving Average (EMA) as a trend filter, Relative Strength Index (RSI) as entry signals, while integrating stop-loss, take-profit, and maximum drawdown control mechanisms. The strategy's main feature is maintaining trend following advantages while strictly controlling risk through dynamic drawdown tracking.

#### Strategy Principle
The core logic includes several key components:
1. Trend Identification: Uses 200-period EMA as the primary trend indicator, only considering long positions when price is above EMA.
2. Momentum Confirmation: Uses RSI as a momentum confirmation tool, allowing entry only when RSI exceeds the set threshold (default 50).
3. Risk Management:
   - Percentage-based stop-loss (default 20%) and take-profit (default 40%)
   - Dynamic drawdown tracking system, automatically closing all positions when total strategy drawdown exceeds the set limit (default 30%)
4. Position Management: Uses account equity percentage (default 10%) for position control

#### Strategy Advantages
1. Strong Adaptability: Through EMA and RSI combination, the strategy can adapt to different market environments
2. Comprehensive Risk Control: Multi-level risk control mechanisms including stop-loss, take-profit, and drawdown limits
3. Scientific Capital Management: Uses account equity percentage for position management, avoiding risks from fixed position sizing
4. Strong Execution: Clear strategy logic and signals, easy to automate
5. Good Scalability: Core components can be adjusted independently, facilitating further optimization

#### Strategy Risks
1. Trend Reversal Risk: EMA as a lagging indicator may not respond timely to trend reversals
2. Choppy Market Risk: May generate frequent false signals in sideways markets
3. Parameter Sensitivity: Strategy performance is sensitive to parameter settings, requiring careful tuning
4. Slippage Impact: Stop-loss and take-profit orders may face slippage risk in volatile markets
Solutions:
- Enhanced trend confirmation mechanisms
- Introduction of market environment recognition system
- Adaptive parameter optimization
- Smart order execution strategies

#### Strategy Optimization Directions
1. Market Environment Recognition: Add volatility indicators to adjust strategy parameters based on different market conditions
2. Dynamic Parameter Optimization: Introduce machine learning algorithms for adaptive parameter adjustment
3. Signal Filter Optimization: Add volume and other auxiliary indicators to improve signal quality
4. Enhanced Risk Control: Introduce dynamic stop-loss mechanisms to adjust stop positions based on market volatility
5. Multi-timeframe Analysis: Integrate signals from multiple timeframes to improve trading decision accuracy

#### Summary
This strategy builds a complete trading system by combining trend following with strict risk control. Its core advantages lie in the completeness of risk management and clarity of strategy logic. Through multi-level risk control mechanisms, the strategy can effectively control drawdown while pursuing returns. Although there are some inherent risks, the strategy still has significant room for improvement through the suggested optimization directions.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-11-19 00:00:00
end: 2024-12-19 00:00:00
period: 2h
basePeriod: 2h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy(title="Disruptor Trend-Following (Drawdown < 30%)", shorttitle="DisruptorStrategyDD", overlay=true)

//-----------------------------------------------------
// User Inputs
//-----------------------------------------------------
emaLen         = input.int(200,  "Long EMA Length",    minval=1)
rsiLen         = input.int(14,   "RSI Length",         minval=1)
rsiThreshold   = input.float(50, "RSI Buy Threshold",  minval=1, maxval=100)
stopLossPerc   = input.float(20, "Stop-Loss %",        minval=0.1, step=0.1)
takeProfitPerc = input.float(40, "Take-Profit %",      minval=0.1, step=0.1)
ddLimit        = input.float(30, "Max Drawdown %",     minval=0.1, step=0.1)

//-----------------------------------------------------
// Indicators
//-----------------------------------------------------
emaValue       = ta.ema(close, emaLen)
rsiValue       = ta.rsi(close, rsiLen)

//-----------------------------------------------------
// Conditions
//-----------------------------------------------------
longCondition  = close > emaValue and rsiValue > rsiThreshold
exitCondition  = close < emaValue or rsiValue < rsiThreshold

//-----------------------------------------------------
// Position Tracking
//-----------------------------------------------------
var bool inTrade = false

if longCondition and not inTrade
    strategy.entry("Long", strategy.long)

if inTrade and exitCondition
    strategy.close("Long")

inTrade := strategy.position_size > 0

//-----------------------------------------------------
// Stop-Loss & Take-Profit
//-----------------------------------------------------
if inTrade
    stopPrice       = strategy.position_avg_price * (1 - stopLossPerc / 100)
    takeProfitPrice = strategy.position_avg_price * (1 + takeProfitPerc / 100)
    strategy.exit("Exit", from_entry="Long", stop=stopPrice, limit=takeProfitPrice)

//-----------------------------------------------------
// Dynamic Drawdown Handling
//-----------------------------------------------------
var float peakEquity = strategy.equity
peakEquity := math.max(peakEquity, strategy.equity)

currentDrawdownPerc = (peakEquity - strategy.equity) / peakEquity * 100
if currentDrawdownPerc > ddLimit
    strategy.close_all("Max Drawdown Exceeded")

//-----------------------------------------------------
// Plotting
//-----------------------------------------------------
plot(emaValue, title="EMA 200", color=color.yellow, linewidth=2)
plotchar(rsiValue, title="RSI", char='•', location=location.bottom, color=color.new(color.teal, 60))

```

> Detail

https://www.fmz.com/strategy/475634

> Last Modified

2024-12-20 16:59:37
