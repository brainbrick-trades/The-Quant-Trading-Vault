
> Name

Adaptive-Trend-Following-Strategy-Based-on-Momentum-Oscillator

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/730f0e1fe6055b543c.png)



This strategy is a trend-following trading system based on the Chande Momentum Oscillator (CMO). It seeks buying opportunities in oversold regions and selling opportunities in overbought regions, while incorporating position holding time limits for risk management. This approach allows for capturing price reversals while avoiding frequent trading in ranging markets.

#### Strategy Principles
The core of the strategy uses the CMO indicator to measure market momentum. CMO generates an oscillator ranging from -100 to 100 by calculating the ratio of the difference between upward and downward movements to their sum. The system generates a long signal when CMO falls below -50, indicating an oversold market condition. Positions are closed when CMO exceeds 50 or when the holding period exceeds 5 cycles. This design captures price rebound opportunities while implementing timely profit-taking and stop-loss measures.

#### Strategy Advantages
1. Clear Signals: Uses fixed CMO thresholds (-50 and 50) as trading signals, providing clear entry and exit rules.
2. Risk Control: Implements position holding time limits to avoid maintaining unprofitable positions.
3. Trend Following: Effectively tracks market trends by entering during oversold conditions and exiting when momentum weakens.
4. Simple Calculation: CMO indicator calculation is intuitive and easy to understand and implement.
5. Adaptability: Strategy parameters can be adjusted for different market conditions, showing good adaptability.

#### Strategy Risks
1. False Breakout Risk: Frequent false signals may occur in ranging markets.
2. Slippage Impact: Actual execution prices may significantly deviate from signal prices in fast markets.
3. Parameter Sensitivity: Strategy performance is highly dependent on CMO period and threshold selections.
4. Market Condition Dependency: May underperform in markets without clear trends.
5. Delay Risk: CMO as a lagging indicator may result in slightly delayed entry and exit timing.

#### Strategy Optimization Directions
1. Dynamic Thresholds: Implement dynamic adjustment of CMO entry and exit thresholds based on market volatility.
2. Multiple Timeframes: Introduce CMO indicators from multiple timeframes to improve signal reliability.
3. Stop-Loss Optimization: Add trailing stop-loss functionality for better profit protection.
4. Position Management: Adjust position sizes based on CMO strength for more refined position control.
5. Market Filtering: Add trend filters to only trade in clearly trending markets.

#### Summary
This momentum-based trend following strategy captures market overbought and oversold opportunities using the CMO indicator. The strategy design is rational, with clear trading rules and risk control mechanisms. While inherent risks exist, optimization can further enhance strategy stability and profitability. The strategy is particularly suitable for highly volatile markets and can achieve good returns during clear trending phases.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-25 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Chande Momentum Oscillator Strategy", overlay=false)

// Input for the CMO period
cmoPeriod = input.int(9, minval=1, title="CMO Period")

// Calculate price changes
priceChange = ta.change(close)

// Separate positive and negative changes
up = priceChange > 0 ? priceChange : 0
down = priceChange < 0 ? -priceChange : 0

// Calculate the sum of ups and downs using a rolling window
sumUp = ta.sma(up, cmoPeriod) * cmoPeriod
sumDown = ta.sma(down, cmoPeriod) * cmoPeriod

// Calculate the Chande Momentum Oscillator (CMO)
cmo = 100 * (sumUp - sumDown) / (sumUp + sumDown)

// Define the entry and exit conditions
buyCondition = cmo < -50
sellCondition1 = cmo > 50
sellCondition2 = ta.barssince(buyCondition) >= 5

// Track if we are in a long position
var bool inTrade = false

if (buyCondition and not inTrade)
    strategy.entry("Long", strategy.long)
    inTrade := true

if (sellCondition1 or sellCondition2)
    strategy.close("Long")
    inTrade := false

// Plot the Chande Momentum Oscillator
plot(cmo, title="Chande Momentum Oscillator", color=color.blue)
hline(-50, "Buy Threshold", color=color.green)
hline(50, "Sell Threshold", color=color.red)

```

> Detail

https://www.fmz.com/strategy/473134

> Last Modified

2024-11-27 15:03:00
