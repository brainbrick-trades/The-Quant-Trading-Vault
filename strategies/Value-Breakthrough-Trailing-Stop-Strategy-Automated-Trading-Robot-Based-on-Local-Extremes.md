
> Name

Value-Breakthrough-Trailing-Stop-Strategy-Automated-Trading-Robot-Based-on-Local-Extremes

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8430dd10f8ec1050280.png)
![IMG](https://www.fmz.com/upload/asset/2d84c5409b5685c85c542.png)




## Overview

The Value Breakthrough Trailing Stop Strategy is a quantitative trading system designed specifically for digital asset trading, which captures market breakouts by placing pending orders (BuyStop and SellStop) at local price extreme positions. The strategy also implements a trailing stop mechanism that activates a protection mechanism to lock in profits once a position reaches a preset profit level. This approach combines the advantages of price breakthrough trading and risk management, providing traders with an automated trading solution.

## Strategy Principles

The strategy is based on price action and dynamic risk management principles, with its core logic divided into the following key components:

1. **Local Extremes Identification**: The strategy calculates local highs and lows using a defined time window (BarsN parameter) as potential breakthrough points. Specifically, it uses (BarsN * 2 + 1) candles to determine local maximum and minimum prices.

2. **Pending Order Setup**:
   - BuyStop: When the current price is lower than the local high minus an order distance buffer, a buy stop order is placed at the local high position.
   - SellStop: When the current price is higher than the local low plus an order distance buffer, a sell stop order is placed at the local low position.

3. **Time Filtering**: The strategy allows traders to set trading sessions, only trading within specified hour ranges, which helps avoid unwanted time periods.

4. **Profit and Loss Level Calculation**:
   - Take Profit (TP): Calculated as a certain percentage (TPasPctBTC) of the current price.
   - Stop Loss (SL): Calculated as a certain percentage (SLasPctBTC) of the current price.
   - Order Distance Buffer: Set to half of the take profit point, preventing orders from triggering too early.

5. **Trailing Stop Mechanism**:
   - Trigger Point (TslTriggerPoints): When profit reaches this level, the trailing stop becomes effective.
   - Trailing Distance (TslPoints): The distance maintained between the trailing stop and the current price.
   - For long positions, when profit exceeds the trigger point, the stop price is set at the current price minus the trailing distance.
   - For short positions, when profit exceeds the trigger point, the stop price is set at the current price plus the trailing distance.

## Strategy Advantages

After in-depth code analysis, the strategy demonstrates the following significant advantages:

1. **Automatic Breakout Capture**: By setting pending orders at key price levels, the strategy can automatically capture price breakouts without the need for manual market monitoring.

2. **Dynamic Risk Management**: Using take profit and stop loss settings based on current price percentages makes risk management more flexible, adapting to different price levels.

3. **Profit Protection Mechanism**: Through the trailing stop function, the strategy can effectively lock in profits already gained while preserving upside potential, reducing drawdowns.

4. **Time Filtering Capability**: Allows traders to select optimal trading sessions based on market characteristics, avoiding trading during periods of low volatility or unpredictable behavior.

5. **High Adaptability**: Strategy parameters can be adjusted according to market conditions, such as adjusting the calculation window for local extremes, take profit and stop loss percentages, enabling adaptation to different market environments.

6. **Strict Execution Discipline**: As an automated strategy, it eliminates the impact of emotional factors on trading decisions and strictly executes trades according to preset rules.

## Strategy Risks

Despite its many advantages, the strategy also presents some potential risks and limitations:

1. **False Breakout Risk**: The market may produce false breakouts, leading the strategy into undesirable trades. The solution is to add confirmation indicators or adjust the order distance buffer size to reduce the probability of false breakout triggers.

2. **Parameter Sensitivity**: Strategy performance highly depends on parameter settings such as BarsN, TPasPctBTC, and SLasPctBTC. Inappropriate parameters may lead to poor performance. Backtesting is recommended to find the optimal parameter combination.

3. **Incomplete Money Management**: Although the RiskPercent parameter is defined in the code, it is not actually applied to position size calculation. This may lead to imperfect risk management.

4. **Limited Ability to Handle Extreme Market Conditions**: In highly volatile or extreme market conditions, simple local extreme breakouts and fixed percentage stops may not be sufficient to effectively manage risk.

5. **Slippage and Execution Delay**: In actual trading, order execution may encounter slippage or delays, affecting strategy performance.

6. **Single Market Dependency**: The strategy is designed for specific assets and may not be applicable to other assets with different market characteristics.

## Strategy Optimization Directions

Based on code analysis, the strategy can be optimized in the following directions:

1. **Dynamic Position Management**: Implement dynamic position size calculation based on the RiskPercent parameter, adjusting position size according to account scale and current market risk for more refined risk control.

2. **Multiple Confirmation Mechanisms**: Introduce additional technical indicators as breakout confirmations, such as volume breakouts, momentum indicators, or trend indicators, to reduce false breakout trades.

3. **Adaptive Parameters**: Introduce parameters that automatically adjust based on market volatility or other market characteristics, allowing the strategy to better adapt to different market environments.

4. **Partial Profit-Taking Strategy**: Implement a partial profit-taking mechanism, allowing portions of the position to exit at different profit levels, both securing partial profits and preserving space for larger gains.

5. **Market State Filtering**: Add market state (trend, oscillation, etc.) judgment to adjust strategy parameters or stop trading under different market states.

6. **Stop Loss Optimization**: Implement dynamic stop losses based on ATR (Average True Range) or other volatility indicators for more reasonable stop loss placement.

7. **Backtesting and Optimization Framework**: Develop a more comprehensive backtesting framework to evaluate strategy performance under different periods and parameters, and find optimal parameter combinations.

## Summary

The Value Breakthrough Trailing Stop Strategy is an ingeniously designed automated trading system that manages risk by capturing local extreme breakouts and applying trailing stops. Its core advantages lie in automated execution, dynamic risk management, and profit protection mechanisms, making it a potentially effective trading tool.

However, the effectiveness of the strategy highly depends on parameter settings and market conditions. By implementing the suggested optimization measures such as dynamic position management, multiple confirmation mechanisms, and adaptive parameters, the robustness and adaptability of the strategy can be significantly improved.

For traders, it is recommended to conduct thorough backtesting before real-world application to find the parameter combination most suitable for the current market environment, and to consider combining other analytical tools to confirm trading signals. At the same time, continuously monitor and evaluate strategy performance, adjusting parameters in a timely manner according to market changes to maintain strategy effectiveness.




> Source (PineScript)

``` pinescript
/*backtest
start: 2025-01-01 00:00:00
end: 2025-04-06 00:00:00
period: 2d
basePeriod: 2d
exchanges: [{"eid":"Futures_Binance","currency":"ETH_USDT"}]
*/

//@version=6
strategy("BTC Trading Robot", overlay=true, pyramiding=1, initial_capital=100000)

//============== Input Groups ==============//
// Trading Profile
group_trading = "BTC"
systemType = input.int(1, title="Trading System (1:BTC)", group=group_trading)

// Common Trading Inputs
group_common = "Trading Inputs"
RiskPercent   = input.float(4.0, title="Risk as % of trading capital", group=group_common)
TradeComment  = input.string("BTC trading robot", title="Trade Comment", group=group_common)
SHInput       = input.int(0, title="Start Hour (0 = no filter)", group=group_common)
EHInput       = input.int(0, title="End Hour (0 = no filter)", group=group_common)

// Gold Related Inputs
group_BTC = "BTC Related Input"
TPasPctBTC         = input.float(0.2, title="TP as % of Price", group=group_BTC)
SLasPctBTC         = input.float(0.1, title="SL as % of Price", group=group_BTC)
TSLasPctofTPBTC   = input.float(5.0, title="Trail SL as % of TP", group=group_BTC)
TSLTgrasPctofTPBTC = input.float(7.0, title="Trail Tgra  SL as % of TP", group=group_BTC)

// Other parameters
BarsN = 5
OrderDistPoints = 100.0

//============== Calculate Trade Parameters ==============//
var float Tppoints = 0.0
var float Slpoints = 0.0
var float TslTriggerPoints = 0.0
var float TslPoints = 0.0

price = close

// Adjust parameters based on system type (using 1 for Gold)
if systemType == 1
    Tppoints := price * TPasPctBTC
    Slpoints := price * SLasPctBTC
    OrderDistPoints := Tppoints / 2.0
    TslPoints := Tppoints * TSLTgrasPctofTPBTC / 100.0
    TslTriggerPoints := Tppoints * TSLTgrasPctofTPBTC / 100.0

//============== Time Filter ==============//
currentHour = hour(time)
inSession = true
if SHInput != 0 and currentHour < SHInput
    inSession := false
if EHInput != 0 and currentHour >= EHInput
    inSession := false

//============== Find Local High and Low ==============//
localHigh = ta.highest(high, BarsN * 2 + 1)
localLow  = ta.lowest(low,  BarsN * 2 + 1)

//============== Entry Orders ==============//
if inSession and strategy.position_size == 0
    // For a BuyStop order: only submit if current price is less than the desired entry level minus a buffer.
    if price < localHigh - OrderDistPoints * syminfo.mintick
        strategy.order("BuyStop", strategy.long, stop=localHigh, comment="BuyStop")
    // For a SellStop order: only submit if current price is greater than the desired entry level plus a buffer.
    if price > localLow + OrderDistPoints * syminfo.mintick
        strategy.order("SellStop", strategy.short, stop=localLow, comment="SellStop")
    
//============== Trailing Stop Logic ==============//
if strategy.position_size > 0  // Long positions
    longProfit = price - strategy.position_avg_price
    if longProfit > TslTriggerPoints * syminfo.mintick
        strategy.exit("Long Exit", from_entry="BuyStop", stop=price - TslPoints * syminfo.mintick, limit=strategy.position_avg_price + Tppoints * syminfo.mintick)
        
if strategy.position_size < 0  // Short positions
    shortProfit = strategy.position_avg_price - price
    if shortProfit > TslTriggerPoints * syminfo.mintick
        strategy.exit("Short Exit", from_entry="SellStop", stop=price + TslPoints * syminfo.mintick, limit=strategy.position_avg_price - Tppoints * syminfo.mintick)

```

> Detail

https://www.fmz.com/strategy/489659

> Last Modified

2025-04-07 13:52:57
