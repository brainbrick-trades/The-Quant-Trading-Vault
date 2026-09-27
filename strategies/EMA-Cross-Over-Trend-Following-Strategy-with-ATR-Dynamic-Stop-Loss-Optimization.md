
> Name

EMA-Cross-Over-Trend-Following-Strategy-with-ATR-Dynamic-Stop-Loss-Optimization

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d87fb46a3c5c58760515.png)
![IMG](https://www.fmz.com/upload/asset/2d8310f9e5be05625826c.png)





#### Overview
This strategy is a trend-following system based on moving average crossovers and dynamic stop-loss management. The core logic is to capture the beginning of uptrends through the golden cross of fast moving average (EMA5) and slow moving average (EMA200), combined with ATR-based dynamic stop-loss for profit protection. The strategy also incorporates a fixed percentage take-profit target to balance risk and reward.

#### Strategy Principles
The strategy operates on the following core mechanisms:
1. Entry signals are triggered when EMA5 crosses above EMA200, indicating short-term momentum breakthrough
2. Dynamic stop-loss is calculated based on the ATR indicator, set at close price minus ATR value multiplied by a factor
3. Take-profit target is set at a fixed percentage (default 5%) above entry price
4. During position holding, ATR stop-loss moves up with price movement, forming a trailing stop
5. The strategy automatically closes positions when price hits either stop-loss or take-profit levels

#### Strategy Advantages
1. Strong trend capture capability - EMA crossover system effectively identifies early trend stages
2. Flexible risk management - ATR dynamic stop-loss adapts to market volatility
3. Stable execution - Systematic entry and exit rules avoid emotional interference
4. High parameter adaptability - Moving average periods, ATR multiplier, and take-profit percentage can be optimized
5. Clear operational logic - Strategy rules are simple and easy to understand and execute

#### Strategy Risks
1. False breakout risk - Ranging markets may produce multiple invalid cross signals
2. Drawdown risk - Sudden trend reversals may lead to significant drawdowns
3. Slippage risk - Stop-loss or take-profit orders may face slippage in volatile markets
4. Parameter sensitivity - Optimal parameters may vary significantly across different market conditions
5. Money management risk - Fixed position sizing may be too risky in certain situations

#### Strategy Optimization Directions
1. Add trend filters - Incorporate trend strength indicators like ADX to filter weak trends
2. Optimize stop-loss mechanism - Consider combining support levels or volatility percentages
3. Dynamic take-profit adjustment - Adjust take-profit targets based on market volatility or trend strength
4. Add time filters - Avoid highly volatile time periods
5. Improve position management - Introduce dynamic position sizing based on market risk levels

#### Summary
This is a trend-following strategy combining classic technical indicators with modern risk management. It captures trends through moving average crossovers and protects profits using ATR dynamic stop-loss, performing well in trending markets. While there are risks of false signals, strategy stability can be significantly improved through parameter optimization and additional filters. The core advantages lie in its systematic operational logic and flexible risk management mechanism, making it suitable as a foundation framework for medium to long-term trend trading.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-21 00:00:00
end: 2025-02-18 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

// -----------------------------------------------------------
//  Title:    EMA5 Cross-Up EMA200 with ATR Trailing Stop & Take-Profit
//  Author:   ChatGPT
//  Version:  1.1 (Pine Script v6)
//  Notes:    Enter Long when EMA(5) crosses above EMA(200).
//            Exit on either ATR-based trailing stop or
//            specified % Take-Profit.
// -----------------------------------------------------------

//@version=6
strategy(title="EMA5 Cross-Up EMA200 ATR Stop", shorttitle="EMA5x200_ATRStop_v6", overlay=true, initial_capital=100000, default_qty_type=strategy.percent_of_equity,default_qty_value=100)

// -- 1) Inputs
emaFastLength   = input.int(5,    "Fast EMA Length")
emaSlowLength   = input.int(200,  "Slow EMA Length")
atrPeriod       = input.int(14,   "ATR Period")
atrMult         = input.float(2.0,"ATR Multiplier", step=0.1)
takeProfitPerc  = input.float(5.0,"Take-Profit %", step=0.1)

// -- 2) Indicator Calculations
emaFast   = ta.ema(close, emaFastLength)
emaSlow   = ta.ema(close, emaSlowLength)
atrValue  = ta.atr(atrPeriod)

// -- 3) Entry Condition: EMA5 crosses above EMA200
emaCrossUp = ta.crossover(emaFast, emaSlow)

// -- 4) Determine a dynamic ATR-based stop loss (for trailing)
longStopPrice = close - (atrValue * atrMult)

// -- 5) Take-Profit Price
//    We store it in a variable so we can update it when in position.
var float takeProfitPrice = na
var float avgEntryPrice   = na

if strategy.position_size > 0
    // If there is an open long, get the average fill price:
    avgEntryPrice   := strategy.position_avg_price
    takeProfitPrice := avgEntryPrice * (1 + takeProfitPerc / 100)
else
    // If no open position, reset
    takeProfitPrice := na
    avgEntryPrice   := na

// -- 6) Submit Entry Order
if emaCrossUp
    strategy.entry(id="Long", direction=strategy.long)

// -- 7) Submit Exit Orders (Stop or Take-Profit)
strategy.exit(id         = "Exit Long",stop       = longStopPrice,limit      = takeProfitPrice)

// -- 8) (Optional) Plotting for Visuals
plot(emaFast, color=color.new(color.yellow, 0), linewidth=2, title="EMA Fast")
plot(emaSlow, color=color.new(color.blue,   0), linewidth=2, title="EMA Slow")
plot(longStopPrice, color=color.red, linewidth=2, title="ATR Trailing Stop")
```

> Detail

https://www.fmz.com/strategy/482774

> Last Modified

2025-02-27 17:51:17
