
> Name

Technical-Indicator-Distance-Measurement-and-MACD-Reversal-Hybrid-Quantitative-Trading-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8bbbd81f4d86cd0cc48.png)
![IMG](https://www.fmz.com/upload/asset/2d88fc21845cfac3f7817.png)




#### Strategy Overview

This strategy is a hybrid quantitative trading approach that combines technical indicator distance measurement with MACD reversal signals. It calculates the Euclidean distance between the current market state and predefined bullish and bearish centroids, while also incorporating MACD crossover signals to form a composite strategy capable of capturing trend momentum and identifying potential reversals. The strategy's uniqueness lies in combining multiple technical indicators (EMA, volatility, momentum, RSI, and MACD) into feature vectors, quantifying the similarity between the current market state and preset conditions through mathematical methods to generate more precise trading signals.

#### Strategy Principles

The core principles of this strategy are built on two main mechanisms:

1. **Distance Measurement Mechanism**: The strategy first constructs a feature vector comprising six technical indicators, including price EMA, volatility, momentum, RSI, MACD line, and MACD histogram. Simultaneously, it predefines two centroid vectors representing bullish and bearish market states, which represent ideal conditions during upward and downward trends. By calculating the Euclidean distance between the current market state vector and these two centroid vectors, the strategy can determine which state the current market more closely resembles.

2. **MACD Crossover Signal Mechanism**: As a second layer of confirmation, the strategy uses MACD indicator crossover signals to judge momentum changes in the market. MACD line crossing above the signal line is considered a buy signal, while MACD line crossing below the signal line is considered a sell signal.

The combination of these two mechanisms forms a dual confirmation system: one aspect judges the overall market tendency through distance measurement, while the other judges short-term momentum changes through MACD crossovers. The strategy can either utilize the joint confirmation of both mechanisms (when distance measurement and MACD simultaneously provide the same signal) or generate trades based on signals independently produced by either mechanism, increasing signal diversity and opportunity capture frequency.

#### Strategy Advantages

1. **Multi-dimensional Market State Assessment**: By combining multiple technical indicators into a feature vector, the strategy can assess market conditions from multiple dimensions rather than relying on a single indicator, thereby reducing the risk of false signals.

2. **Flexible Signal Generation Mechanism**: The strategy simultaneously uses distance measurement and MACD crossovers to generate signals, allowing it to capture sustained momentum in trending markets while also timely identifying potential reversal points, resulting in stronger adaptability.

3. **Objectivity of Mathematical Models**: Euclidean distance calculation provides an objective, mathematical method for evaluating market states, reducing the influence of subjective judgment factors.

4. **Automatic Position Closing Mechanism**: The strategy automatically closes positions in the opposite direction when new signals are generated, helping to implement timely stop-losses and switch position direction, adapting to rapidly changing markets.

5. **Performance Monitoring Functionality**: The strategy has built-in tracking and display functions for trade profits and losses, facilitating real-time assessment of strategy performance and necessary parameter adjustments.

#### Strategy Risks

1. **Parameter Sensitivity Risk**: The EMA, RSI, and MACD indicators used in the strategy all depend on specific parameter settings. If these parameters are not suitable for current market conditions, they may lead to erroneous signals. The solution is to find optimal parameter combinations through backtesting and periodically reassess parameter effectiveness.

2. **Overtrading Risk**: Since the strategy can independently generate signals based on two different mechanisms, it may produce excessive trading signals in highly volatile markets, increasing transaction costs. This can be mitigated by adding signal filtering mechanisms or adjusting signal generation logic to reduce unnecessary trades.

3. **Trend and Reversal Judgment Conflicts**: Under certain market conditions, distance measurement and MACD signals may provide contradictory indications, causing inconsistent strategy behavior. It is recommended to establish clear signal priority rules or introduce additional confirmation mechanisms.

4. **Static Nature of Centroid Settings**: Some parameters in the current strategy's bull and bear market centroids are statically set (such as RSI values), which may not adapt to all market environments. Consider introducing adaptive mechanisms to dynamically adjust centroid positions based on historical data.

5. **Single Timeframe Limitation**: The strategy operates within a single timeframe, potentially missing important signals from larger or smaller timeframes. Expanding to a multi-timeframe strategy can improve signal reliability.

#### Strategy Optimization Directions

1. **Adaptive Centroid Design**: Currently, some parameters for bull and bear market centroids are fixed. This could be improved to dynamic centroids automatically calculated based on historical data. For example, data from the past N periods could be used to determine ideal bullish and bearish states, allowing centroids to automatically adjust with market conditions.

2. **Signal Priority and Filtering Mechanisms**: Introduce a signal priority system based on market environment. For example, prioritize reversal signals in high-volatility environments and distance measurement signals in low-volatility environments with clear trends. Additionally, signal filters based on volatility or volume could be added to reduce noise signals.

3. **Stop-Loss and Profit Target Mechanisms**: The current strategy lacks clear stop-loss and profit target settings. Consider adding stop-loss mechanisms based on ATR or fixed percentages, as well as profit targets based on support/resistance levels or risk-reward ratios.

4. **Multi-Timeframe Analysis Integration**: Integrate trend information from larger timeframes into the current strategy. For example, only execute hourly-level trading signals when they align with the daily trend direction to improve signal reliability.

5. **Dynamic Adjustment of Feature Weights**: Assign dynamic weights to different indicators in the feature vector, automatically adjusting their influence based on each indicator's predictive ability under different market conditions to improve the accuracy of distance calculations.

6. **Machine Learning Enhancement**: Consider introducing simple machine learning algorithms to optimize centroid positions or feature weights. Clustering algorithms could even be used to automatically discover multiple market state centroids, rather than simply using two bull and bear states.

#### Summary

The Technical Indicator Distance Measurement and MACD Reversal Hybrid Quantitative Trading Strategy is an innovative quantitative trading method that integrates multiple common technical indicators into a unified market state assessment system through Euclidean distance calculation techniques, combined with MACD crossover signals to form a dual confirmation mechanism. This approach can capture momentum in sustained trends while also identifying potential market reversal points, demonstrating strong adaptability and flexibility.

The core advantages of this strategy lie in its multi-dimensional market assessment capability and the objectivity of its mathematical model. However, it also faces risks such as parameter sensitivity, overtrading, and signal conflicts. The strategy has significant optimization potential through introducing adaptive centroid designs, optimizing signal priority systems, adding stop-loss mechanisms, integrating multi-timeframe analysis, and applying machine learning techniques.

For quantitative traders, this strategy combining traditional technical analysis methods with mathematical models provides a worthwhile new direction to explore, particularly suitable for those who wish to improve the objectivity of trading decisions while maintaining strategy explainability.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-04-15 00:00:00
end: 2024-12-31 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("Bysq-Distance Reversal Entry - BTCUSDT (v6)", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10, margin_long=0, margin_short=0)

// ========== FEATURE ENGINEERING ==========
price = close
priceNorm = ta.ema(price, 5)
volatility = ta.stdev(price, 20)
momentum = ta.ema(close - close[5], 5)
rsi = ta.rsi(close, 14)
macdLine = ta.ema(close, 12) - ta.ema(close, 26)
signalLine = ta.ema(macdLine, 9)
macdHist = macdLine - signalLine

// Fitur sebagai vector
featureVector = array.new_float(6)
array.set(featureVector, 0, priceNorm)
array.set(featureVector, 1, volatility)
array.set(featureVector, 2, momentum)
array.set(featureVector, 3, rsi)
array.set(featureVector, 4, macdLine)
array.set(featureVector, 5, macdHist)

// Centroid bullish
bullishCentroid = array.new_float(6)
array.set(bullishCentroid, 0, price)
array.set(bullishCentroid, 1, volatility)
array.set(bullishCentroid, 2, momentum)
array.set(bullishCentroid, 3, 60.0)
array.set(bullishCentroid, 4, macdLine)
array.set(bullishCentroid, 5, macdHist)

// Centroid bearish
bearishCentroid = array.new_float(6)
array.set(bearishCentroid, 0, price)
array.set(bearishCentroid, 1, volatility)
array.set(bearishCentroid, 2, momentum)
array.set(bearishCentroid, 3, 40.0)
array.set(bearishCentroid, 4, macdLine)
array.set(bearishCentroid, 5, macdHist)

// Fungsi Euclidean Distance
euclideanDistance(arr1, arr2) =>
    dist = 0.0
    for i = 0 to array.size(arr1) - 1
        a = array.get(arr1, i)
        b = array.get(arr2, i)
        dist += math.pow((a - b), 2)
    math.sqrt(dist)

// Hitung jarak ke centroid
distToBullish = euclideanDistance(featureVector, bullishCentroid)
distToBearish = euclideanDistance(featureVector, bearishCentroid)

// ========== SINYAL ==========
// Original distance strategy signals
isDistanceBuySignal = distToBullish < distToBearish and ta.crossover(macdLine, signalLine)
isDistanceSellSignal = distToBearish < distToBullish and ta.crossunder(macdLine, signalLine)

// Reversal strategy signals
isReversalBuySignal = ta.crossover(macdLine, signalLine)
isReversalSellSignal = ta.crossunder(macdLine, signalLine)

// Combined signals - using both strategies
isBuySignal = isDistanceBuySignal or isReversalBuySignal
isSellSignal = isDistanceSellSignal or isReversalSellSignal

// ========== EKSEKUSI ==========
if isBuySignal
    strategy.close("Sell")         // Close any sell position first (from reversal strategy)
    strategy.entry("Buy", strategy.long)
    
if isSellSignal
    strategy.close("Buy")          // Close any buy position first (from reversal strategy)
    strategy.entry("Sell", strategy.short)

// ========== METRIK KINERJA ==========
float lastOpenTradeProfit = na
if strategy.opentrades > 0
    lastOpenTradeProfit := strategy.opentrades.profit(strategy.opentrades - 1)

float lastClosedTradeProfit = na
if strategy.closedtrades > 0
    lastClosedTradeProfit := strategy.closedtrades.profit(strategy.closedtrades - 1)

// Plot info
plot(lastOpenTradeProfit, title="Last Open Trade Profit", color=color.blue)
plot(lastClosedTradeProfit, title="Last Closed Trade Profit", color=color.orange)
```

> Detail

https://www.fmz.com/strategy/490794

> Last Modified

2025-04-16 15:19:46
