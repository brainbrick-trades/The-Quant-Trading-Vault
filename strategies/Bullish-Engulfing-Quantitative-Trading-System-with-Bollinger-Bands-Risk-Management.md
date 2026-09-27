
> Name

Bullish-Engulfing-Quantitative-Trading-System-with-Bollinger-Bands-Risk-Management

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8a3a865635eca28f045.png)
![IMG](https://www.fmz.com/upload/asset/2d8b348affec26b3a46b5.png)




#### Overview
This strategy is a quantitative trading system based on technical analysis, primarily utilizing the Bullish Engulfing pattern as an entry signal, combined with Bollinger Bands volatility indicators for risk management and position sizing. After identifying a Bullish Engulfing pattern, the strategy calculates a risk ratio (R value) based on the Bollinger Bands range, then determines precise position size based on a fixed percentage (0.75%) of account equity, and finally manages trades through dynamic stop-loss and a fixed risk-reward ratio (4R) take-profit target.

#### Strategy Principles
The core logic of this strategy is divided into three main components: signal generation, position management, and exit conditions.

First, signal generation is based on the Bullish Engulfing pattern, which must meet the following criteria:
1. Current candle's close is higher than its open (bullish candle)
2. Previous candle's close is lower than its open (bearish candle)
3. Current candle's close is higher than the previous candle's open
4. Current candle's open is lower than the previous candle's close
5. Volume exceeds a minimum threshold (default 1,000,000)

Second, position management is implemented through these steps:
1. Calculate Bollinger Bands with 40-period length and 2.5 standard deviations
2. Compute the R value from the Bollinger Bands spread: R = 0.4 * (1 - (lowerBB / upperBB))
3. Use 0.75% of the portfolio equity as the risk amount per trade
4. Calculate precise position size based on the stop-loss distance (R value) and entry price

Finally, exit conditions are set as:
1. Stop-loss: Exit when price drops to entry price minus R%
2. Take-profit: Exit when price rises to entry price plus 4R%

#### Strategy Advantages
1. Precise and Dynamic Risk Control: The strategy doesn't use fixed stop-loss points but dynamically adjusts risk parameters based on current market volatility (calculated through Bollinger Bands), allowing the system to adapt to different market environments.

2. Fixed-Percentage Risk Management: Each trade risks only 0.75% of the account, effectively preventing excessive losses from single trades and achieving long-term capital management stability.

3. Precise Position Sizing: Position size is calculated precisely based on Bollinger Bands volatility and risk amount, ensuring consistent risk exposure under different market conditions.

4. Clear Risk-Reward Ratio: A fixed 4R take-profit target ensures that each trade's potential reward is 4 times the potential risk, aligning with professional trading risk-reward requirements.

5. Trade Visualization: Entry signals and trade range boxes are visually marked, helping traders intuitively understand trade performance.

#### Strategy Risks
1. Timing Risk: The Bullish Engulfing pattern is a short-term price reversal signal that may not predict medium or long-term trend changes, potentially leading to premature entries in strong trending markets.

2. Market Condition Limitations: The strategy may underperform in highly volatile or illiquid markets, especially when Bollinger Bands abnormally expand or contract.

3. Limited Entry Conditions: Relying solely on the Bullish Engulfing pattern may result in sparse signals or missed valid entry opportunities.

4. Fixed Multiplier Risk: Using a fixed 0.4 coefficient to calculate the R value may not be flexible enough in certain market conditions, failing to fully adapt to extreme market environments.

5. Potential Slippage Issues: In highly volatile markets, actual stop-loss execution prices may experience significant slippage, affecting real risk control effectiveness.

#### Strategy Optimization Directions
1. Add Filtering Conditions: Consider adding trend confirmation indicators (such as moving averages) to ensure trading Bullish Engulfing patterns only in the direction of the main trend, avoiding counter-trend trading.

2. Multi-Timeframe Analysis: Introduce higher timeframe market structure analysis, executing trades only when aligned with higher timeframe trends to improve signal quality.

3. Dynamic Risk Parameter Adjustment: Make the fixed 0.75% risk percentage and 0.4 R value coefficient adjustable parameters that automatically adapt to market volatility, increasing risk in low-volatility markets and reducing it in high-volatility markets.

4. Optimize Exit Strategy: Consider adding trailing stops or indicator-based dynamic exit conditions, rather than relying solely on fixed stop-loss and take-profit levels.

5. Add Multi-Indicator Confirmation: Combine the Bullish Engulfing pattern with other technical indicators (such as RSI, MACD, or volume analysis) to improve entry signal reliability.

#### Summary
The Bullish Engulfing Quantitative Trading System with Bollinger Bands Risk Management is a complete trading system that combines traditional candlestick pattern recognition with modern risk management methods. The strategy dynamically adjusts risk parameters through Bollinger Bands, precisely controls position size for each trade, and sets profit targets using a fixed risk-reward ratio. This approach provides adaptability to market volatility while maintaining trading discipline.

While the strategy excels in risk management, there is room for optimization, particularly in entry signal quality and exit strategy flexibility. By adding additional filtering conditions, multi-timeframe analysis, and dynamic risk parameter adjustments, the strategy can further improve its adaptability and profitability across different market environments.

Overall, this is a complete trading system with professional risk management characteristics, suitable for traders who value capital management and risk control. With reasonable optimization and parameter adjustments, this strategy can become a stable long-term trading tool.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-26 00:00:00
end: 2025-02-23 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Binance","currency":"SOL_USDT"}]
*/

//@version=5
strategy("Bullish Engulfing Strategy with BB Risk", overlay=true)

// Input parameters for customization (optional, can be adjusted in Strategy Tester)
minVolume = input.int(1000000, "Minimum Volume", minval=1)  // Optional filter for liquidity

// Calculate Bollinger Bands (length=40, StdDev=2.5) for R
length = 40
mult = 2.5
basis = ta.sma(close, length)  // Middle Band (40-period SMA of close)
dev = mult * ta.stdev(close, length)  // Standard deviation multiplied by 2.5
upperBB = basis + dev  // Upper Bollinger Band
lowerBB = basis - dev  // Lower Bollinger Band

// Define R as 0.4 times the Bollinger Bands spread: R = 0.4 * ((1 - (lowerBB / upperBB)) * 100)
R = 0.4 * (1 - (lowerBB / upperBB))  // Percentage value, scaled by 0.4

// Define Bullish Engulfing pattern with optional volume filter
isBullishEngulfing() => close > open and close[1] < open[1] and close > open[1] and open < close[1] and close[1] < open[1] and close > open and volume > minVolume

bullishEngulfing = isBullishEngulfing()

// Track position and entry details
var bool inPosition = false
var float entryPrice = 0.0
var int entryBar = 0
var int exitBar = 0  // Track exit bar (added here to fix undeclared variable)
var float exitPrice = 0.0  // Track exit price

// Enter long position on the next bar after Bullish Engulfing, with position size risking 0.75% of portfolio
if (bullishEngulfing and not inPosition)
    // Calculate position size to risk 0.75% of portfolio
    portfolioValue = strategy.equity  // Current portfolio equity
    riskPerTrade = portfolioValue * 0.0075  // 0.75% of portfolio
    stopLossDistance = R  // R% of entry price (stop-loss distance)
    entryPrice := close
    positionSize = riskPerTrade / stopLossDistance / entryPrice  // Position size in units (contracts/shares)
    
    // Ensure positionSize is rounded to a practical number (e.g., whole shares)
    positionSize := math.round(positionSize)
    
    // Enter long position with calculated size
    strategy.entry("Long", strategy.long, limit = entryPrice, qty=positionSize)
    inPosition := true
    entryBar := bar_index

// Exit logic: Stop-loss or Take-profit
if (inPosition)
    // Stop-loss: Exit if price drops below entryPrice - R%
    stopLossLevel = entryPrice * (1 - R)
    if (low <= stopLossLevel)
        strategy.close("Long")
        inPosition := false
        exitBar := bar_index
        exitPrice := close
    
    // Take-profit: Exit if price rises above entryPrice + 4R%
    takeProfitLevel = entryPrice * (1 + 4 * R)
    if (high >= takeProfitLevel)
        strategy.close("Long")
        inPosition := false
        exitBar := bar_index
        exitPrice := close

// Optional: Plot signals and R for visualization
if (bullishEngulfing)
    label.new(bar_index, high, "Bullish Engulfing", yloc=yloc.abovebar, color=color.green, style=label.style_label_down, textcolor=color.white)

plot(R, title="R (BB Spread %)", color=color.blue, style=plot.style_histogram)

```

> Detail

https://www.fmz.com/strategy/483677

> Last Modified

2025-02-25 10:57:40
