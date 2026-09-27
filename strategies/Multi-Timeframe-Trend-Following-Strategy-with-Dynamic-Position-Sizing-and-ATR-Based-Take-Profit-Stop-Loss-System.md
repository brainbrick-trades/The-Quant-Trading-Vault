
> Name

Multi-Timeframe-Trend-Following-Strategy-with-Dynamic-Position-Sizing-and-ATR-Based-Take-Profit-Stop-Loss-System

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8acbf7377d67bce5a37.png)
![IMG](https://www.fmz.com/upload/asset/2d81806c0774e5ee9575c.png)




#### Overview
This strategy is a comprehensive trading system that combines multi-timeframe analysis, trend following, and dynamic position sizing. It uses EMA as the primary trend indicator, MACD as a secondary confirmation indicator, and incorporates ATR for risk control and take profit/stop loss settings. The strategy's uniqueness lies in its use of 8-hour timeframe volume-price analysis for signal filtering and dynamic position sizing based on trend strength.

#### Strategy Principles
The strategy employs a layered design approach with the following core components:
1. Trend Identification System: Uses 7-period and 90-period EMA crossovers and relative positions to determine trend direction
2. Signal Confirmation System: Uses MACD indicator's golden and death crosses as entry signal confirmation
3. Multi-timeframe Validation: Ensures larger timeframe support through 8-hour period EMA and volume analysis
4. Dynamic Position Management: Adjusts position size based on trend strength (calculated through EMA difference to ATR ratio)
5. Risk Control System: Sets stop loss at 1.5x ATR and take profit at 3x ATR

#### Strategy Advantages
1. Multi-level Signal Filtering: Significantly improves signal quality through multi-timeframe analysis and multiple indicator confirmation
2. Intelligent Position Management: Automatically adjusts position size based on trend strength, increasing profit potential in strong trends while controlling risk in weak trends
3. Comprehensive Risk Control: Uses ATR to dynamically adjust stop loss and take profit levels, adapting to market volatility changes
4. Systematic Design: Strong logical correlation between strategy components, forming a complete trading system

#### Strategy Risks
1. Trend Reversal Risk: Multiple stop losses may occur at trend turning points
2. Slippage Risk: Actual stop loss prices may deviate from expectations during highly volatile periods
3. Parameter Sensitivity: Strategy involves multiple timeframe parameters, excessive optimization may lead to overfitting
4. Market Environment Dependency: May generate frequent false signals in ranging markets

#### Strategy Optimization Directions
1. Enhanced Signal Filtering: Add trend strength filter to trade only when trend strength exceeds specific thresholds
2. Dynamic Stop Loss Optimization: Adjust stop loss multiplier based on market volatility and holding time
3. Position Management Improvement: Incorporate more market state indicators to optimize position calculation logic
4. Market Environment Recognition: Add market type identification to use different parameter combinations in different market environments

#### Summary
The strategy builds a complete trend following trading system through multi-timeframe analysis and dynamic position management. Its strengths lie in its systematic design approach and comprehensive risk control mechanisms, while attention needs to be paid to market environment adaptability and parameter optimization issues. Through the suggested optimization directions, the strategy can further enhance its stability and profit potential.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-22 00:00:00
end: 2025-02-19 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=6
strategy('Optimized Trend Strategy', overlay = true, initial_capital = 10000, default_qty_type = strategy.cash, default_qty_value = 50, commission_value = 0.1)

// ? Core Indicators
ema7 = ta.ema(close, 7)
ema90 = ta.ema(close, 90)
atr = ta.atr(14)
[macdLine, signalLine, _] = ta.macd(close, 12, 26, 9)

// ? 8 Hours multi-time frame confirmation
h8Close = request.security(syminfo.tickerid, '480', close)
h8Volume = request.security(syminfo.tickerid, '480', volume)
h8Ema7 = ta.ema(h8Close, 7)
h8Signal = h8Close > h8Ema7 and h8Volume > ta.sma(h8Volume, 50)

// ? Dynamic Risk Control
stopLoss = close - 1.5 * atr
takeProfit = close + 3 * atr

// ? Trading Signals
longCondition = close > ema7 and ema7 > ema90 and ta.crossover(macdLine, signalLine) and h8Signal
shortCondition = close < ema7 and ema7 < ema90 and ta.crossunder(macdLine, signalLine) and h8Signal

// ? Position management (according to trend strength))
trendStrength = (ema7 - ema90) / (atr / close)

var float positionSize = na

if trendStrength > 2
    positionSize := strategy.equity * 0.7 / close
    positionSize
else if trendStrength < 0.5
    positionSize := strategy.equity * 0.3 / close
    positionSize
else
    positionSize := strategy.equity * 0.5 / close
    positionSize

// ? Order Execution
if longCondition
    strategy.entry('Long', strategy.long, qty = positionSize)
    strategy.exit('Long Exit', from_entry = 'Long', stop = stopLoss, limit = takeProfit)

if shortCondition
    strategy.entry('Short', strategy.short, qty = positionSize)
    strategy.exit('Short Exit', from_entry = 'Short', stop = stopLoss, limit = takeProfit)

```

> Detail

https://www.fmz.com/strategy/483088

> Last Modified

2025-02-27 17:02:23
