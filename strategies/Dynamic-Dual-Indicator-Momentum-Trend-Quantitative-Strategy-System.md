
> Name

Dynamic-Dual-Indicator-Momentum-Trend-Quantitative-Strategy-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/652f0513b16012a70e.png)


#### Overview
This strategy is a quantitative trading system that combines the Relative Strength Index (RSI) and Moving Averages (MA) to identify market trends and trading opportunities. The system also incorporates volume and volatility filters to enhance the reliability of trading signals. The core concept is to determine trend direction through the crossover of fast and slow moving averages while using RSI for momentum confirmation, ultimately forming a complete trading decision framework.

#### Strategy Principle
The strategy employs a dual-signal confirmation mechanism:
1. Trend Confirmation Layer: Uses the crossover of Fast Moving Average (FastMA) and Slow Moving Average (SlowMA) to determine market trends. When the fast line crosses above the slow line, an uptrend is established; when the fast line crosses below the slow line, a downtrend is established.
2. Momentum Confirmation Layer: Uses RSI as a momentum confirmation tool. In uptrends, RSI should be below 50, indicating upward potential; in downtrends, RSI should be above 50, indicating downward potential.
3. Trading Filters: Sets minimum thresholds for volume and ATR volatility to filter out signals with insufficient liquidity or volatility.

#### Strategy Advantages
1. Multi-dimensional Signal Confirmation: Combines trend and momentum indicators to reduce the probability of false signals.
2. Comprehensive Risk Management: Integrates stop-loss and take-profit functions with percentage-based risk control points.
3. Flexible Filtering Mechanism: Volume and volatility filters can be enabled or disabled based on market conditions.
4. Automatic Position Closing: Closes positions automatically when reversal signals appear to avoid overholding.

#### Strategy Risks
1. Choppy Market Risk: False breakout signals may frequently occur in range-bound markets.
2. Slippage Risk: During volatile market conditions, actual execution prices may significantly deviate from signal trigger prices.
3. Parameter Sensitivity: Strategy performance highly depends on parameter settings, different market environments may require different parameter combinations.

#### Strategy Optimization Directions
1. Dynamic Parameter Adjustment: Introduce adaptive parameter mechanisms to dynamically adjust moving average periods and RSI thresholds based on market volatility.
2. Signal Weighting System: Establish a signal strength scoring system, assigning different weights based on indicator performance.
3. Market Environment Classification: Add market state identification modules to employ different trading strategies under different market conditions.
4. Enhanced Risk Control: Introduce dynamic stop-loss mechanisms to automatically adjust stop-loss positions based on market volatility.

#### Summary
This strategy establishes a comprehensive trading system through the integrated use of trend and momentum indicators. The system's strengths lie in its multi-layered signal confirmation mechanism and comprehensive risk management framework. However, practical application requires attention to the impact of market conditions on strategy performance and parameter optimization based on actual circumstances. Through continuous improvement and optimization, this strategy has the potential to maintain stable performance across different market environments.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-17 00:00:00
end: 2025-01-16 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT","balance":49999}]
*/

// © Boba2601
//@version=5
strategy("RSI-MA Synergy", overlay=true, margin_long=100, margin_short=100)

// === Налаштування індикаторів ===
length_rsi = input.int(14, title="RSI Period", group="Індикатори")
fastMALength = input.int(9, title="Fast MA Length", group="Індикатори")
slowMALength = input.int(21, title="Slow MA Length", group="Індикатори")

// === Налаштування стоп-лосу і тейк-профіту ===
useStopLossTakeProfit = input.bool(true, title="Використовувати стоп-лос і тейк-профіт", group="Стоп-лос і Тейк-профіт")
stopLossPercent = input.float(2.0, title="Стоп-лос (%)", minval=0.1, step=0.1, group="Стоп-лос і Тейк-профіт")
takeProfitPercent = input.float(4.0, title="Тейк-профіт (%)", minval=0.1, step=0.1, group="Стоп-лос і Тейк-профіт")

// === Налаштування об'єму та волатильності ===
useVolumeFilter = input.bool(false, title="Використовувати фільтр об'єму", group="Об'єм та Волатильність")
volumeThreshold = input.int(50000, title="Мінімальний об'єм", group="Об'єм та Волатильність")
useVolatilityFilter = input.bool(false, title="Використовувати фільтр волатильності", group="Об'єм та Волатильність")
atrLength = input.int(14, title="Період ATR для волатильності", group="Об'єм та Волатильність")
volatilityThreshold = input.float(1.5, title="Мінімальна волатильність (ATR)", step=0.1, group="Об'єм та Волатильність")


// === Розрахунок індикаторів ===
rsiValue = ta.rsi(close, length_rsi)
fastMA = ta.sma(close, fastMALength)
slowMA = ta.sma(close, slowMALength)

// === Розрахунок об'єму та волатильності ===
averageVolume = ta.sma(volume, 20)
atrValue = ta.atr(atrLength)

// === Умови входу в позицію ===
longCondition = ta.crossover(fastMA, slowMA) and rsiValue < 50
if useVolumeFilter
    longCondition := longCondition and volume > volumeThreshold
if useVolatilityFilter
    longCondition := longCondition and atrValue > volatilityThreshold

shortCondition = ta.crossunder(fastMA, slowMA) and rsiValue > 50
if useVolumeFilter
    shortCondition := shortCondition and volume > volumeThreshold
if useVolatilityFilter
    shortCondition := shortCondition and atrValue > volatilityThreshold

// === Логіка входу та виходу з позиції ===
if (longCondition)
    strategy.entry("Long", strategy.long)
    if (useStopLossTakeProfit)
        stopLossPrice = close * (1 - stopLossPercent / 100)
        takeProfitPrice = close * (1 + takeProfitPercent / 100)
        strategy.exit("Exit Long", "Long", stop = stopLossPrice, limit = takeProfitPrice)

if (shortCondition)
    strategy.entry("Short", strategy.short)
    if (useStopLossTakeProfit)
        stopLossPrice = close * (1 + stopLossPercent / 100)
        takeProfitPrice = close * (1 - takeProfitPercent / 100)
        strategy.exit("Exit Short", "Short", stop = stopLossPrice, limit = takeProfitPrice)

// === Закриття позицій за зворотнім сигналом ===
if (strategy.position_size > 0 and (ta.crossunder(fastMA, slowMA) or rsiValue > 50))
    strategy.close("Long", comment="Закрито по сигналу")

if (strategy.position_size < 0 and (ta.crossover(fastMA, slowMA) or rsiValue < 50))
    strategy.close("Short", comment="Закрито по сигналу")
```

> Detail

https://www.fmz.com/strategy/478749

> Last Modified

2025-01-17 16:41:17
