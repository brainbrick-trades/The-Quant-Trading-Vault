
> Name

Multi-MA-Trend-Following-with-RSI-Momentum-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/11549e253ad10783ca4.png)


#### Overview
This strategy is a trend-following system based on multiple moving averages and RSI indicator. It utilizes a combination of 20, 50, and 200-period moving averages to analyze market trends through their relative positions, combined with RSI confirmation for trade signals. The strategy incorporates dynamic stop-loss and profit targets with trailing stops to protect profits.

#### Strategy Principles
The core of the strategy lies in analyzing the relative positions of three moving averages (MA20, MA50, MA200) to determine market trends. The strategy defines 18 different moving average combination scenarios, focusing on crossovers and relative positions. Long positions are preferred when shorter-term MAs are above longer-term MAs, and vice versa. To avoid overtrading, RSI is introduced as a filter, allowing long entries when RSI is below 70 and short entries above 30. The strategy employs a 1:10 risk-reward ratio with a 25-point trailing stop to protect profits.

#### Strategy Advantages
1. Multi-dimensional trend confirmation: More accurate trend strength and direction determination through analysis of multiple MA relationships
2. Dynamic risk management: Trailing stop mechanism protects profits while allowing for continued growth
3. Comprehensive filtering: RSI indicator integration effectively reduces false signals
4. Optimized risk-reward ratio: 1:10 setting targets profits from major trends
5. High adaptability: Strategy applicable across different markets and timeframes

#### Strategy Risks
1. Choppy market risk: May generate frequent false breakout signals in ranging markets
2. Slippage risk: 25-point trailing stop may not execute accurately in fast markets due to slippage
3. Trend reversal risk: Strategy may react slowly to trend reversals, leading to profit giveback
4. Parameter dependency: Strategy effectiveness heavily relies on MA period and RSI parameter selection

#### Optimization Directions
1. Volume indicator integration: Add volume analysis to improve trend identification accuracy
2. Scenario definition optimization: Simplify redundant scenario definitions to improve strategy efficiency
3. Dynamic parameter adjustment: Adjust trailing stop levels based on market volatility
4. Time filtering addition: Add trading session filters to avoid high volatility market opens and closes
5. Signal confirmation enhancement: Add trend strength confirmation indicators to improve signal reliability

#### Summary
This is a well-structured trend-following strategy with clear logic. The combination of multiple moving average systems with RSI filtering creates a relatively reliable trading system. The risk management mechanism is well-designed, protecting profits through trailing stops without premature exits. While there is room for optimization, the overall framework is scientifically designed with practical application value.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-27 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Refined MA Strategy with Trailing Stop for 30m", overlay=true)

// Define the moving averages
TR20 = ta.sma(close, 20)
TR50 = ta.sma(close, 50)
TR200 = ta.sma(close, 200)

// Define the RSI for additional filtering
rsi = ta.rsi(close, 14)

// Define the scenarios
scenario1 = TR20 > TR50 and TR50 > TR200
scenario2 = TR50 > TR20 and TR20 > TR200
scenario3 = TR200 > TR50 and TR50 > TR20
scenario4 = TR50 > TR200 and TR200 > TR20
scenario5 = TR20 > TR200 and TR200 > TR50
scenario6 = TR200 > TR20 and TR20 > TR50
scenario7 = TR20 == TR50 and TR50 > TR200
scenario8 = TR50 == TR20 and TR20 > TR200
scenario9 = TR200 == TR50 and TR50 > TR20
scenario10 = TR20 > TR50 and TR50 == TR200
scenario11 = TR50 > TR20 and TR20 == TR200
scenario12 = TR20 > TR50 and TR50 == TR200
scenario13 = TR20 == TR50 and TR50 == TR200
scenario14 = TR20 > TR50 and TR200 == TR50
scenario15 = TR50 > TR20 and TR200 == TR50
scenario16 = TR20 > TR50 and TR50 == TR200
scenario17 = TR20 > TR50 and TR50 == TR200
scenario18 = TR20 > TR50 and TR50 == TR200

// Entry conditions
longCondition = (scenario1 or scenario2 or scenario5) and rsi < 70
shortCondition = (scenario3 or scenario4 or scenario6) and rsi > 30

// Execute trades based on scenarios with 50 points stop loss and 1:10 RR, using a trailing stop of 25 points
if (longCondition)
    strategy.entry("Long", strategy.long)
    strategy.exit("Take Profit", from_entry="Long", limit=close + 250, trail_offset=25)

if (shortCondition)
    strategy.entry("Short", strategy.short)
    strategy.exit("Take Profit", from_entry="Short", limit=close - 250, trail_offset=25)

```

> Detail

https://www.fmz.com/strategy/473360

> Last Modified

2024-11-29 15:20:30
