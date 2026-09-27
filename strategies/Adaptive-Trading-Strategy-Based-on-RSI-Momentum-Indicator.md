
> Name

Adaptive-Trading-Strategy-Based-on-RSI-Momentum-Indicator

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8a58eec47c3d2c4a861.png)
![IMG](https://www.fmz.com/upload/asset/2d7f315021c7ac4f1f628.png)





#### Overview
This strategy is a momentum trading system based on the Relative Strength Index (RSI), which executes trades by identifying overbought and oversold market conditions. The strategy employs fixed percentage stop-loss and take-profit targets for automated risk-reward management. The system operates on a 15-minute timeframe and is suitable for instruments with good liquidity.

#### Strategy Principles
The core of the strategy utilizes the RSI indicator to identify overbought and oversold market conditions. When RSI falls below 30, indicating potential oversold conditions, the system opens a long position; when RSI rises above 70, indicating potential overbought conditions, it opens a short position. Each trade is managed with fixed percentage-based stop-loss (0.2%) and take-profit (0.6%) levels, automating risk management.

#### Strategy Advantages
1. Clear Operating Rules: Uses the widely recognized RSI indicator, providing clear trading signals that are easy to understand and execute
2. Comprehensive Risk Management: Employs fixed-ratio stop-loss and take-profit settings, effectively controlling risk for each trade
3. High Automation Level: The entire trading process from entry to exit is automated, reducing human intervention
4. Strong Adaptability: Strategy can be applied to different trading instruments with good universality
5. High Computational Efficiency: Uses basic technical indicators, minimizing computational load for real-time trading

#### Strategy Risks
1. Sideways Market Risk: May generate frequent false signals in range-bound markets
2. Trend Breakout Risk: Fixed stop-loss levels may be easily triggered during strong trends
3. Parameter Sensitivity: Strategy performance is highly dependent on RSI period and threshold settings
4. Slippage Risk: Actual execution prices may deviate from expected levels during high volatility
5. Systematic Risk: May incur significant losses during extreme market conditions

#### Optimization Directions
1. Introduce Trend Filters: Incorporate moving averages or other trend indicators to reduce false signals
2. Dynamic Stop-Loss Setting: Automatically adjust stop-loss levels based on market volatility
3. Optimize Entry Timing: Add volume and other auxiliary indicators to improve entry accuracy
4. Money Management Optimization: Implement dynamic position sizing based on account equity and market volatility
5. Add Time Filters: Avoid trading during high-volatility periods such as major news releases

#### Summary
This is a well-structured, logically sound automated trading strategy. It captures market overbought and oversold opportunities through the RSI indicator, coupled with fixed-ratio risk management for complete trading automation. The strategy's main advantages lie in its clear operational rules and controllable risk, though market conditions significantly impact its performance. Through the suggested optimization directions, there is room for further strategy enhancement.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-24 00:00:00
end: 2025-02-22 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Binance","currency":"SOL_USDT"}]
*/

//@version=5
strategy("MultiSymbol Smart Money EA without Lot Sizes or Pairs", overlay=true)

// Strategy Parameters for RSI
RSI_Period = input.int(14, title="RSI Period", minval=1)
RSI_Overbought = input.float(70, title="RSI Overbought")
RSI_Oversold = input.float(30, title="RSI Oversold")

// Fixed values for Stop Loss and Take Profit in percentage
FIXED_SL = input.float(0.2, title="Stop Loss in %", minval=0.0) / 100
FIXED_TP = input.float(0.6, title="Take Profit in %", minval=0.0) / 100

// RSI Calculation
rsi = ta.rsi(close, RSI_Period)

// Buy and Sell Conditions based on RSI
longCondition = rsi <= RSI_Oversold
shortCondition = rsi >= RSI_Overbought

// Entry Price
longPrice = close
shortPrice = close

// Execute the trades
if (longCondition)
    strategy.entry("Buy", strategy.long)

if (shortCondition)
    strategy.entry("Sell", strategy.short)

// Set Stop Loss and Take Profit based on entry price and percentage
if (strategy.position_size > 0)  // If there is a long position
    longStopLoss = longPrice * (1 - FIXED_SL)
    longTakeProfit = longPrice * (1 + FIXED_TP)
    strategy.exit("Exit Buy", from_entry="Buy", stop=longStopLoss, limit=longTakeProfit)

if (strategy.position_size < 0)  // If there is a short position
    shortStopLoss = shortPrice * (1 + FIXED_SL)
    shortTakeProfit = shortPrice * (1 - FIXED_TP)
    strategy.exit("Exit Sell", from_entry="Sell", stop=shortStopLoss, limit=shortTakeProfit)


```

> Detail

https://www.fmz.com/strategy/483518

> Last Modified

2025-02-27 16:47:25
