
> Name

Multi-Candlestick-Pattern-Recognition-and-Automated-Trading-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d969fef0da98329303b5.png)
![IMG](https://www.fmz.com/upload/asset/2d8051faa30fda1322930.png)



#### Overview

The Multi-Candlestick Pattern Recognition and Automated Trading Strategy is a quantitative trading system based on price action analysis, specifically designed to identify "Morning Star" and "Evening Star" formations, which are widely regarded as powerful reversal signals in technical analysis. This strategy employs a mathematically defined model to recognize these patterns and automatically executes long or short trades based on their occurrence. The system implements a 1% take profit and 0.5% stop loss, creating a 2:1 reward-to-risk ratio, which aligns with professional trading risk management principles. This strategy not only helps traders objectively identify market reversal points but also eliminates emotional bias through automated execution, making investment decisions more objective and systematic.

#### Strategy Principles

The core of this strategy lies in identifying Morning Star and Evening Star candlestick patterns through precise mathematical methods. These patterns typically consist of three consecutive candles with specific structural characteristics:

1. **Morning Star Pattern**:
   - First candle: A large bearish body in a downtrend
   - Second candle: A small body or doji, indicating market uncertainty
   - Third candle: A large bullish body with a close above the midpoint of the first candle

2. **Evening Star Pattern**:
   - First candle: A large bullish body in an uptrend
   - Second candle: A small body or doji, indicating market uncertainty
   - Third candle: A large bearish body with a close below the midpoint of the first candle

The strategy employs several helper functions to calculate key characteristics:
- `bullish`/`bearish` functions determine candle direction
- `bodySize`/`candleRange` calculate the size of candle bodies and ranges
- `smallBody`/`strongBody` evaluate the relative size of candle bodies
- `isMiddleReversalCandle` identifies middle reversal candle features

When the system confirms a pattern, it automatically executes the corresponding long or short trade with a 1% take profit and 0.5% stop loss level, forming a 2:1 reward-to-risk ratio. This ratio is widely considered a sustainable risk management approach in professional trading.

#### Strategy Advantages

1. **Objective Entry Signals**: Through clear mathematical definitions, the strategy eliminates subjective judgment, providing objective and consistent entry signals that avoid human bias and emotional decision-making.

2. **Robust Risk Management**: The built-in 2:1 reward-to-risk ratio (1% take profit, 0.5% stop loss) ensures disciplined money management, allowing for profitability in the long run even with a win rate as low as 40%.

3. **Adaptability Across Markets and Timeframes**: The strategy is based on universally present price action patterns, making it applicable across various financial markets and timeframes, enhancing its flexibility and utility.

4. **Refined Pattern Recognition**: The code's `strongBody`, `smallBody`, and `isMiddleReversalCandle` functions analyze candle characteristics in detail, improving the accuracy of pattern recognition and reducing false positives.

5. **Automated Execution**: The strategy automatically identifies patterns and executes trades, eliminating hesitation and delays associated with manual trading, ensuring trades are executed according to plan.

6. **Visual Confirmation**: By marking identified patterns on the chart, traders can easily backtest and verify strategy performance, facilitating continuous improvement.

#### Strategy Risks

1. **False Breakout Risk**: Candlestick patterns may generate false signals in certain market conditions, particularly in low-volatility environments or ranging markets. This risk can be mitigated by adding additional confirmation indicators such as volume or momentum oscillators.

2. **Fixed Percentage Stop Loss Limitations**: The strategy uses fixed percentages for stop loss and take profit points, which may not be suitable for the volatility characteristics of all markets. Considering dynamic stops based on ATR (Average True Range) might be more appropriate.

3. **Lack of Trend Filtering**: The current strategy does not consider the broader market trend, potentially leading to frequent stop-outs when trading against strong trends. Adding trend indicators (such as moving averages) to filter signals could improve success rates.

4. **Optimization Risk**: Current parameters (such as 0.3 and 0.6 body proportion thresholds) may be overfitted to historical data and perform poorly in future markets. Robust backtesting and forward testing are essential.

5. **Lack of Volume Confirmation**: The strategy relies solely on price action without considering volume, which is an important factor in confirming the validity of reversals. Integrating volume analysis into the strategy could improve signal quality.

#### Strategy Optimization Directions

1. **Add Trend Filters**: Implement moving averages or trend strength indicators to only trade reversal patterns in the direction of the trend. For example, only trading Morning Stars in uptrends and Evening Stars in downtrends could significantly improve win rates.

2. **Integrate Volume Confirmation**: Add volume patterns as an additional confirmation factor. Ideally, the third candle of a Morning Star should be accompanied by increased volume, and the third candle of an Evening Star should also have substantial volume support.

3. **Implement Dynamic Stop Losses**: Replace fixed percentage stops with dynamic stops based on market volatility, such as using ATR multiples to set stop loss positions, making them more adaptable to current market conditions.

4. **Add Multiple Timeframe Analysis**: Incorporate market structure analysis from higher timeframes to ensure trade direction aligns with larger trends, avoiding trading against major trends.

5. **Optimize Parameter Settings**: Conduct extensive backtesting across various markets and timeframes to find more robust parameter values. In particular, the thresholds for `smallBody` and `strongBody` can be adjusted to improve pattern recognition accuracy.

6. **Incorporate Time Filters**: Markets behave differently during various trading sessions. Adding time filters can avoid inefficient trading periods, such as high volatility periods during market openings and closings.

#### Summary

The Multi-Candlestick Pattern Recognition and Automated Trading Strategy represents a comprehensive solution that combines traditional technical analysis with modern quantitative methods. By precisely identifying Morning Star and Evening Star patterns, the strategy provides traders with objective market reversal entry points while enhancing execution discipline through automated trading and strict risk management.

While the base strategy is already well-developed, performance can be further enhanced through optimizations such as trend filtering, volume confirmation, and dynamic risk management. It is important for traders to recognize that any strategy requires comprehensive backtesting and validation in specific market environments to ensure its robustness and reliability.

Finally, this strategy not only provides trading signals but also offers educational value for understanding market structure and price action. By observing the formation of these classic patterns, traders can gain deeper insights into market psychology and potential supply-demand imbalances, fostering more mature market intuition.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-04-03 00:00:00
end: 2024-12-07 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BNB_USDT"}]
*/

//@version=6
strategy("Morning & Evening Star Strategy (1% TP, 0.5% SL)", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === Inputs ===
slPercent = 0.5
tpPercent = 1.0

// === Helper Functions ===
bullish(open, close) => close > open
bearish(open, close) => close < open
bodySize(open, close) => math.abs(close - open)
candleRange(high, low) => high - low

smallBody(open, close, high, low) =>
    bodySize(open, close) < (candleRange(high, low) * 0.3)

strongBody(open, close, high, low) =>
    bodySize(open, close) > (candleRange(high, low) * 0.6)

isMiddleReversalCandle(open, close, high, low) =>
    bSize = bodySize(open, close)
    cRange = candleRange(high, low)
    upperWick = high - math.max(open, close)
    lowerWick = math.min(open, close) - low
    smallBody(open, close, high, low) or (bSize < cRange * 0.4 and (upperWick > cRange * 0.3 or lowerWick > cRange * 0.3))

// === Candle Values for Last 3 Bars ===
o3 = open[2]
c3 = close[2]
h3 = high[2]
l3 = low[2]

o2 = open[1]
c2 = close[1]
h2 = high[1]
l2 = low[1]

o1 = open
c1 = close
h1 = high
l1 = low

// === Pattern Conditions ===
isMorningStar = bearish(o3, c3) and strongBody(o3, c3, h3, l3) and
                 isMiddleReversalCandle(o2, c2, h2, l2) and
                 bullish(o1, c1) and strongBody(o1, c1, h1, l1) and
                 c1 > (o3 + c3) / 2

isEveningStar = bullish(o3, c3) and strongBody(o3, c3, h3, l3) and
                 isMiddleReversalCandle(o2, c2, h2, l2) and
                 bearish(o1, c1) and strongBody(o1, c1, h1, l1) and
                 c1 < (o3 + c3) / 2

// === Entry & Exit ===
if isMorningStar
    strategy.entry("Long", strategy.long)
    strategy.exit("TP/SL Long", from_entry="Long", loss=slPercent * close / 100, profit=tpPercent * close / 100)

if isEveningStar
    strategy.entry("Short", strategy.short)
    strategy.exit("TP/SL Short", from_entry="Short", loss=slPercent * close / 100, profit=tpPercent * close / 100)

// === Visual Labels ===
plotshape(isMorningStar, title="Morning Star", location=location.belowbar, color=color.green, style=shape.labelup, text="MS")
plotshape(isEveningStar, title="Evening Star", location=location.abovebar, color=color.red, style=shape.labeldown, text="ES")

```

> Detail

https://www.fmz.com/strategy/489295

> Last Modified

2025-04-03 11:10:20
