
> Name

BTST-High-Probability-Breakout-Strategy-with-Selective-Stock-Screening-System

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d88a14ee928f61812bc0.png)
![IMG](https://www.fmz.com/upload/asset/2d87131c06712bb912c8a.png)





#### Overview

The BTST High-Probability Breakout Strategy with Selective Stock Screening System is a quantitative approach designed for intraday and overnight trading, aimed at identifying and capturing short-term price momentum breakthrough opportunities. This strategy combines time-specific price movement screening, classic technical pattern confirmation, and dynamic resistance breakout analysis to construct a multi-layered trading decision system. The core of the strategy lies in precisely filtering targets with a 2-3% gain at 3 PM, further confirming bullish signals through candlestick pattern analysis, and setting reasonable entry and exit mechanisms to avoid overextension risks, thereby achieving high-probability short-term trading opportunities.

#### Strategy Principles

The operational principles of this strategy are based on multi-condition progressive filtering and confirmation:

1. **Initial Screening (3 PM)**: The strategy first screens for instruments with a daily gain of 2-3% at precisely 3 PM. This specific time window selection is based on the assumption that market momentum may continue to develop into the close.

2. **Daily Candlestick Pattern Analysis**: The strategy incorporates three classic bullish pattern assessments:
   - Bullish Engulfing Pattern: When the current day's candlestick completely engulfs the previous day's candlestick, and the current day's closing price is higher than its opening price.
   - Morning Star Pattern: Composed of three candlesticks, showing a transition from bearish to bullish sentiment.
   - Three White Soldiers Pattern: Three consecutive positive candlesticks with each closing price higher than the previous candlestick's closing price.

3. **30-Minute Resistance Breakout**: The strategy dynamically sets resistance levels every 30 minutes (the highest point of the current 30-minute period) and determines whether the price breaks through this resistance level, serving as a potential signal for continued upward movement or profit-taking.

4. **Avoiding Overextension**: The strategy calculates intraday gains to avoid instruments that have already risen more than 5% or fallen more than 10%, mitigating potential pullback risks.

5. **Next-Day Watchlist**: Combining the above conditions, instruments that meet the initial screening, bullish pattern confirmation, and are not overextended are added to the next-day watchlist.

6. **Exit Strategy**: Simulating pre-market and opening observations, if an instrument gaps up by more than 2% and the price remains above the previous day's low, positions are maintained for at least 15 minutes, awaiting potential further upside.

7. **Buy and Sell Triggers**: Buy signals are based on a combination of bullish patterns, initial screening conditions, and non-overextension assessment; sell signals rely on resistance level breakout conditions and non-overextension status.

#### Strategy Advantages

1. **Temporal Precision**: The strategy screens at the specific time point of 3 PM, effectively capturing a critical stage of intraday momentum development, providing early warning for potential continuation moves the next day.

2. **Multiple Confirmation Mechanism**: By combining percentage price changes, technical patterns, and resistance breakouts as triple confirmation, the strategy significantly enhances signal reliability and reduces false signal risks.

3. **Integrated Risk Management**: The strategy incorporates filtering conditions to avoid overextended stocks, effectively mitigating chase-the-high risks and improving the safety margin of trades.

4. **Flexible Exit Mechanism**: The strategy sets flexible exit conditions based on resistance breakouts and price performance, facilitating timely position closure when profits are realized or risks materialize.

5. **Visual Assistance**: The strategy marks various conditions and signals on charts, allowing traders to intuitively understand market status and strategy logic, facilitating real-time decision adjustments.

6. **Alert System Integration**: Built-in alert condition settings enable traders to receive timely buy and sell signal notifications without constant screen monitoring, improving trading efficiency.

#### Strategy Risks

1. **False Breakout Risk**: The 30-minute resistance breakout may exhibit false breakout phenomena, especially during high market volatility, potentially leading to unnecessary trading signals. The solution is to add volume confirmation or set higher breakout thresholds.

2. **Pattern Recognition Limitations**: Candlestick pattern recognition based on fixed rules may not capture all effective formations in complex market environments. Consider cross-validation with other technical indicators such as RSI or MACD.

3. **Time Dependency**: The strategy heavily relies on the 3 PM screening condition; missing this time point or experiencing data delays may lead to missed trading opportunities. Consider expanding the screening time window or setting alternative time points.

4. **Over-Filtering Risk**: The layering of multiple conditions may result in too few qualifying trading opportunities, affecting the strategy's practicality. Consider appropriately relaxing certain screening conditions or dynamically adjusting parameters based on market conditions.

5. **Market State Adaptability**: This strategy performs better in specific market conditions (such as moderate uptrends) but may underperform in range-bound or highly volatile markets. Recommend selectively employing the strategy based on the overall market environment.

#### Strategy Optimization Directions

1. **Dynamic Parameter Adjustment**: The current strategy uses fixed percentage thresholds (2-3% gain screening, 5-10% overextension judgment). Consider dynamically adjusting these parameters based on market volatility to improve the strategy's adaptability across different market environments.

2. **Volume Confirmation Addition**: The strategy currently relies primarily on price action. Consider adding volume analysis dimensions, such as requiring breakouts to occur on increased volume, or setting conditions where volume increases by a specific percentage compared to previous average levels, improving signal quality.

3. **Timeframe Expansion**: Consider performing pattern and breakout confirmations across different timeframes (such as 15-minute, 60-minute), constructing a multi-timeframe confirmation system to reduce false signals and enhance signal reliability.

4. **Trend Filter Integration**: Introduce medium-term trend assessment indicators, such as moving average systems or the ADX indicator, to ensure short-term trading direction aligns with medium-term trends, avoiding counter-trend operations and improving success rates.

5. **Machine Learning Optimization**: Utilize machine learning algorithms to recognize patterns and optimize parameters from successful historical cases, extracting more refined trading rules and dynamic threshold adjustment mechanisms.

6. **Drawdown Control Mechanism**: Add stop-loss settings based on fixed percentages or ATR multiples, and consider implementing partial profit-taking mechanisms, such as scaled exits or trailing stops, to better control risk and lock in profits.

#### Conclusion

The BTST High-Probability Breakout Strategy with Selective Stock Screening System constructs a systematic short-term trading decision framework by combining time-specific screening, technical pattern analysis, and dynamic resistance breakout assessment. This strategy is particularly suitable for finding instruments that have accumulated certain momentum during the day and have technical confirmations, capturing potential continuation moves the next day. Although the strategy considers multiple confirmations and risk controls in its design, it still requires flexible adjustments and continuous optimization based on actual market conditions. By implementing the suggested optimization directions, especially dynamic parameter adjustments, volume confirmation, and multi-timeframe analysis, the strategy's robustness and adaptability can be further enhanced, providing traders with a more reliable decision support tool.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-04-01 00:00:00
end: 2024-05-28 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"ETH_USDT"}]
*/

//@version=5
strategy("BTST Strategy", overlay=true)

// --- 1. Initial Screening at 3 PM (Identify 2-3% gain) ---
is3pm = (hour == 15 and minute == 0)  // Check if it's 3 PM
priceChangePercentage = (close - close[1]) / close[1] * 100  // Calculate percentage change from previous close

// Stocks with a gain of 2-3% by 3 PM
isSelectedStock = is3pm and priceChangePercentage >= 2 and priceChangePercentage <= 3
plotshape(series=isSelectedStock, title="Selected Stock", location=location.belowbar, color=color.green, style=shape.labelup, text="Selected")

// --- 2. Daily Candle Analysis (Bullish Patterns) ---
// Bullish Engulfing pattern
bullishEngulfing = close > open and open[1] > close[1] and close > open[1] and open < close[1]

// Morning Star pattern
morningStar = close[2] < open[2] and close[1] < open[1] and close > open and close[1] > open[1]

// Three White Soldiers pattern
threeWhiteSoldiers = close > open and close[1] > open[1] and close[2] > open[2] and close > close[1] and close[1] > close[2]

// Combine the patterns for bullish confirmation
bullishPattern = bullishEngulfing or morningStar or threeWhiteSoldiers
plotshape(series=bullishPattern, title="Bullish Pattern", location=location.belowbar, color=color.green, style=shape.labelup, text="Bullish")

// --- 3. 30-Minute Candle Breakout ---
var float resistanceLevel = na

// Capture the highest point every 30 minutes
if (minute == 30 or minute == 0)
    resistanceLevel := high

// Check for breakout above resistance level
breakoutAboveResistance = close > resistanceLevel
plotshape(series=breakoutAboveResistance, title="Breakout Above Resistance", location=location.abovebar, color=color.blue, style=shape.labelup, text="Breakout")

// --- 4. Avoid Over-Extended Stocks (5-10% intraday gains) ---
// Calculate the percentage gain from the open price
percentageGain = (close - open) / open * 100

// Avoid stocks that are up more than 5-10% intraday
avoidOverExtendedStocks = percentageGain > 5 or percentageGain < -10
plotshape(series=avoidOverExtendedStocks, title="Avoid Over-Extended Stocks", location=location.abovebar, color=color.red, style=shape.labeldown, text="Over-Extended")

// --- 5. Second-Day Watchlist (Add shortlisted stocks to watchlist) ---
// We will skip implementing a watchlist in Pine Script because it isn't supported for direct interaction with external systems, but we will mark it in the script visually.
watchlistCondition = isSelectedStock and bullishPattern and not avoidOverExtendedStocks
plotshape(series=watchlistCondition, title="Second Day Watchlist", location=location.belowbar, color=color.purple, style=shape.triangledown, text="Watchlist")

// --- 6. Exit Strategy - Pre-Market & Opening Observation ---
// This part requires real-time data and pre-market data, which isn't supported directly in Pine Script
// But, we can simulate exit strategy by showing potential exit points based on the gap-up opening:
gapUpOpening = open > close[1] * 1.02  // If the stock opens 2% above the previous close
hold15Min = gapUpOpening and close > low[1]  // Hold if price doesn't break the previous low

plotshape(series=hold15Min, title="Gap-Up Hold for 15 Minutes", location=location.abovebar, color=color.blue, style=shape.triangledown, text="Hold")

// --- 7. Buy and Sell Triggers (Strategy) ---

// Define conditions for the buy trigger
buySignal = bullishPattern and isSelectedStock and not avoidOverExtendedStocks

// Buy when the conditions are met
if buySignal
    strategy.entry("Buy", strategy.long)

// Define conditions for the sell trigger
sellSignal = breakoutAboveResistance and not avoidOverExtendedStocks

// Sell when the breakout above resistance condition is met
if sellSignal
    strategy.close("Buy")

// --- Alerts ---
// Alerts for Buy Signal based on 0.5% price movement
alertcondition(buySignal, title="Buy Signal", message="Buy Signal: Confirmed Bullish Pattern and 2-3% price increase by 3 PM!")

// Alerts for Sell Signal based on Breakout and other conditions
alertcondition(sellSignal, title="Sell Signal", message="Sell Signal: Breakout above resistance!")

```

> Detail

https://www.fmz.com/strategy/489133

> Last Modified

2025-04-02 09:33:50
