
> Name

Multi-Timeframe-RSI-SMA-Dynamic-Crossover-Adaptive-Trading-System

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8902231939588635db8.png)
![IMG](https://www.fmz.com/upload/asset/2d89a280f206215c5e9bc.png)




## Overview

The Multi-Timeframe RSI-SMA Dynamic Crossover Adaptive Trading System is an advanced quantitative trading strategy that combines Relative Strength Index (RSI) and Simple Moving Average (SMA) crossover signals. What makes this strategy unique is its ability to automatically adjust indicator parameters, risk levels, and filtering conditions according to different timeframes (from 1-minute to monthly charts), achieving cross-timeframe trading adaptability. Through in-depth analysis of the Pine Script code, it's evident that the strategy employs an intelligent parameter adjustment mechanism that automatically optimizes RSI periods, SMA periods, ATR multipliers, take-profit percentages, and volume requirements across different timeframes, thereby maintaining consistent performance in short-term, medium-term, and long-term trading.

## Strategy Principle

The core principle of this strategy is based on the crossover signals between RSI and its SMA line, combined with multiple confirmation filters and a dynamic risk management system. The specific operating principles are as follows:

1. **Intelligent Parameter Adaptation**: The strategy detects the current chart timeframe using the `timeframe.period` function, then assigns optimal parameters for various indicators using a switch structure. For example, the RSI period expands from 10 periods on 1-minute charts to 28 periods on monthly charts; SMA periods range from 20 to 200; ATR multipliers increase from 1.5x to 4.5x; take-profit targets range from 3% to 10%.

2. **Dynamic Indicator Calculation**: 
   - Adaptive RSI-SMA: Calculates RSI values and RSI SMA lines using optimized periods
   - Smart Volume Filtering: Adjusts volume requirements based on timeframe, requiring 2x the 20-period average volume for 1-minute charts, but only 0.5x for monthly charts
   - Trend Confirmation: Uses crossovers between fast and slow EMAs to confirm uptrends, ensuring trades follow the trend

3. **Entry Conditions**: 
   - RSI crosses above its SMA line
   - Volume exceeds the dynamic threshold
   - Confirmed uptrend (Fast EMA > Slow EMA)
   - Closing price greater than opening price (bullish candle)
   - Closing price breaks above the 5-period high

4. **Exit Conditions**: 
   - RSI crosses below its SMA line
   - Price drops below the 5-period low

5. **Risk Management**: 
   - Dynamic Stop-Loss: Based on ATR multipliers (from 1.5x to 4.5x), adapting to the volatility characteristics of different timeframes
   - Dynamic Take-Profit: Sets percentage targets from 3% to 10% based on entry point, expanding with the timeframe

## Strategy Advantages

Through in-depth analysis of the code structure, this strategy demonstrates the following significant advantages:

1. **Full Timeframe Adaptability**: The most prominent advantage is the strategy's ability to work adaptively across all timeframes from 1-minute to monthly charts without manual intervention to adjust parameters. This solves the common problem of traditional strategies performing inconsistently across different timeframes.

2. **Multiple Filtering Mechanisms**: The strategy relies not only on RSI-SMA crossover signals but also combines price breakouts, trend confirmation, volume verification, and other multiple filtering conditions, significantly reducing false signals.

3. **Dynamic Risk Management**: Stop-loss and take-profit levels automatically adjust with timeframe and market volatility. Higher timeframes set wider stop-losses and larger profit targets, which aligns with volatility patterns.

4. **Automatic Visualization**: The code includes clear visualization elements, including buy markers, stop-loss lines, and take-profit lines, helping traders intuitively understand the trading logic.

5. **Low Code Complexity**: Despite being powerful, the code structure is clear, well-organized, and logically concise, making it easy to maintain and further optimize.

## Strategy Risks

Despite its sophisticated design, the strategy still has the following potential risks:

1. **Parameter Optimization Overfitting Risk**: Although the strategy sets optimized parameters for different timeframes, these parameters may be derived from historical data optimization, presenting an overfitting risk. The solution is to backtest and validate across multiple market cycles (bull, bear, ranging markets) and different instruments.

2. **Rapid Trend Reversal Risk**: In highly volatile markets, prices may quickly reverse after triggering an entry signal, causing stop-losses to be hit. It's advisable to pause the strategy during extreme market volatility periods (such as before and after major economic announcements) or add additional filtering conditions.

3. **Volume Anomaly Risk**: The strategy relies on volume as a filtering condition, but under certain market conditions (such as liquidity droughts), abnormal volume fluctuations may occur, affecting signal quality. Consider adding relative volume indicators or volume accumulation/distribution analysis to enhance filtering effectiveness.

4. **Fixed Percentage Take-Profit Limitations**: Using fixed percentage take-profits may exit strong trends too early, missing out on larger profits. Consider implementing scaled profit-taking or dynamically adjusting take-profit levels based on trend strength.

5. **Timeframe Switching Confusion**: Switching timeframes during strategy operation may cause parameter mutations, affecting risk management settings for current positions. It's recommended to close all positions before switching timeframes.

## Strategy Optimization Directions

Based on code analysis, the strategy can be optimized in the following aspects:

1. **Add Adaptive Momentum Indicators**: Incorporate momentum indicators like MACD or OBV as additional confirmation alongside the RSI-SMA system, especially in long-term trading, to improve signal quality. The rationale for this optimization is that momentum indicators better capture trend continuity and strength.

2. **Market State Classification Mechanism**: Introduce an automatic classification mechanism for market states (range-bound/trending), automatically adjusting strategy preferences based on volatility and directional parameters. This can reduce trading frequency in range-bound markets and increase holding time in trending markets.

3. **Dynamic Stop-Loss Optimization**: Current stop-losses are based on fixed ATR multipliers. Consider dynamically adjusting stop-losses by incorporating support levels, resistance levels, or key price levels to increase the market relevance of stop-loss settings.

4. **Intraday Time Filtering**: For short timeframes (1-minute to 1-hour), add intraday time filtering to avoid high volatility periods 30 minutes before market open and close, or focus on specific high-efficiency trading sessions.

5. **Machine Learning Parameter Optimization**: Introduce simple machine learning algorithms to dynamically optimize RSI and SMA periods, automatically adjusting parameters based on recent market conditions, rather than using preset fixed parameter mappings.

6. **Multi-Indicator Resonance System**: Expand to a multi-indicator resonance system, combining price action, volume distribution, and market structure analysis to improve signal reliability and anti-interference capabilities.

## Summary

The Multi-Timeframe RSI-SMA Dynamic Crossover Adaptive Trading System is an intricately designed quantitative trading strategy. Its most significant feature is the ability to automatically adapt to any timeframe from 1-minute to monthly charts without manual parameter adjustments. The strategy uses RSI crossing above its SMA line as the core signal, combined with multiple filtering conditions and dynamic risk management, achieving cross-timeframe trading adaptability.

This strategy is particularly suitable for traders who need to flexibly switch between multiple timeframes, as well as quantitative analysts who want to build consistent trading systems from short-term to long-term. Through intelligent parameter adjustment, dynamic indicator calculation, and strict entry conditions, the strategy can maintain stable performance across different market environments.

Although risks such as parameter optimization overfitting and rapid trend reversals exist, through the optimization directions proposed in this article, such as adding adaptive momentum indicators, market state classification mechanisms, and machine learning parameter optimization, the strategy's robustness and profitability can be further enhanced. In practical application, it is recommended to conduct thorough backtesting across multiple market cycles and different instruments, combined with 0.1% transaction cost simulation, to verify the strategy's performance in real market environments.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-03-28 00:00:00
end: 2025-03-27 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"ETH_USDT"}]
*/

//@version=5
strategy("Multi-Timeframe RSI-SMA Strategy [EB]", overlay=true, precision=2, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

//▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
//             SMART PARAMETER ADJUSTMENT
//▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

// Zaman Dilimi Tespiti
currentTF = timeframe.period

// Parametreler için ayrı switch yapıları
rsiPeriod = switch currentTF
    "1"  => 10
    "5"  => 12
    "15" => 14
    "30" => 16
    "60" => 18
    "240" => 20
    "D"  => 22
    "W"  => 24
    "M"  => 28
    => 14

smaPeriod = switch currentTF
    "1"  => 20
    "5"  => 25
    "15" => 30
    "30" => 40
    "60" => 50
    "240" => 60
    "D"  => 100
    "W"  => 150
    "M"  => 200
    => 50

atrMult = switch currentTF
    "1"  => 1.5
    "5"  => 1.8
    "15" => 2.0
    "30" => 2.2
    "60" => 2.5
    "240" => 3.0
    "D"  => 3.5
    "W"  => 4.0
    "M"  => 4.5
    => 2.0

tpPerc = switch currentTF
    "1"  => 3.0
    "5"  => 3.5
    "15" => 4.0
    "30" => 4.5
    "60" => 5.0
    "240" => 6.0
    "D"  => 7.0
    "W"  => 8.0
    "M"  => 10.0
    => 4.0

volMultiplier = switch currentTF
    "1"  => 2.0
    "5"  => 1.8
    "15" => 1.5
    "30" => 1.3
    "60" => 1.2
    "240" => 1.0
    "D"  => 0.8
    "W"  => 0.6
    "M"  => 0.5
    => 1.0

//▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
//             DYNAMIC INDICATORS
//▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

// Akıllı Hacim Filtresi
avgVol = ta.sma(volume, 20)
minVol = avgVol * volMultiplier

// Adaptif RSI-SMA
rsi = ta.rsi(close, rsiPeriod)
rsiSMA = ta.sma(rsi, smaPeriod)

// Volatilite Analizi
atr = ta.atr(14)
dynamicATR = atr * atrMult

// Trend Filtresi
emaFast = ta.ema(close, int(smaPeriod * 0.7))
emaSlow = ta.ema(close, smaPeriod * 2)
trendUp = emaFast > emaSlow

//▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
//             TRADE LOGIC
//▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

entryCondition = 
  ta.crossover(rsi, rsiSMA) and
  volume > minVol and
  trendUp and
  close > open and
  close > ta.highest(high, 5)[1]

exitCondition = 
  ta.crossunder(rsi, rsiSMA) or 
  close < ta.lowest(low, 5)[1]

//▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
//             RISK MANAGEMENT
//▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

var float entryPrice = na
var float stopLoss = na
var float takeProfit = na

if entryCondition
    entryPrice := close
    stopLoss := close - dynamicATR
    takeProfit := close + (dynamicATR * (tpPerc / 100))
    strategy.entry("Long", strategy.long)
    strategy.exit("Exit", "Long", stop=stopLoss, limit=takeProfit)

if exitCondition
    strategy.close("Long")

//▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
//             VISUALIZATION
//▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

plotshape(entryCondition, "Buy", shape.labelup, location.belowbar, color.green, 0, "LONG", textcolor=color.white)
plot(stopLoss, "Stop", color.red, 2, plot.style_linebr)
plot(takeProfit, "Take Profit", color.green, 2, plot.style_linebr)
```

> Detail

https://www.fmz.com/strategy/488502

> Last Modified

2025-03-28 11:36:12
