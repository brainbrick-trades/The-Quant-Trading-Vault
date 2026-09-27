
> Name

Dynamic-Trend-Following-Strategy-Based-on-Relative-Strength-and-RSI

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1464b51d233260409d3.png)


#### Overview
This strategy is a trend following system based on Supertrend, Relative Strength (RS), and Relative Strength Index (RSI). By integrating these three technical indicators, it enters trades when market trends are clear and implements dynamic stop-loss for risk management. The strategy primarily aims to capture strong upward price trends while using RSI to confirm trend sustainability.

#### Strategy Principles
The strategy employs a triple-filtering mechanism for trade signals:
1. Uses Supertrend indicator to determine overall trend, considering uptrend when indicator direction is up.
2. Calculates Relative Strength (RS) value, percentizing price position within high-low range over 55 periods to measure price strength.
3. Utilizes RSI to judge overbought/oversold conditions, confirming upward momentum when RSI exceeds 60.
Trade entry requires simultaneous satisfaction of all three conditions: Supertrend up, RS above 0, and RSI above threshold.
Exit occurs when any two indicators signal reversal. A fixed 1.1% stop-loss manages risk.

#### Strategy Advantages
1. Multiple technical indicators confirmation enhances signal reliability.
2. Supertrend effectively tracks trends, reducing false signals in choppy markets.
3. RS indicator captures price strength changes promptly, improving entry timing accuracy.
4. RSI confirms trend momentum, avoiding entries during trend exhaustion.
5. Fixed stop-loss sets clear risk control boundaries.
6. Flexible exit conditions respond promptly to market changes.

#### Strategy Risks
1. Multiple indicators may cause signal lag, missing optimal entry points.
2. Frequent trading in choppy markets may increase transaction costs.
3. Fixed stop-loss might trigger easily in highly volatile markets.
4. RSI may remain in overbought territory during strong trends, missing opportunities.
5. Multiple exit conditions might lead to premature profit taking.

#### Strategy Optimization Directions
1. Introduce adaptive indicator parameters adjusting dynamically with market volatility.
2. Add volume indicators for signal confirmation enhancement.
3. Design dynamic stop-loss mechanism based on ATR values.
4. Optimize RSI thresholds, considering different values for various market conditions.
5. Add trend strength filtering to reduce trading frequency in weak trends.
6. Consider implementing trailing stop-profit mechanism for better profit retention.

#### Summary
The strategy constructs a relatively comprehensive trend following trading system by integrating Supertrend, RS, and RSI indicators. Its main advantage lies in the multiple signal confirmation mechanism enhancing trade reliability, while clear risk control mechanisms provide trading safeguards. Despite potential risks, suggested optimization directions can further improve strategy stability and profitability. This strategy is particularly suitable for markets with clear trends and can serve as a foundation framework for medium to long-term trading.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2025-01-04 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Sanjay RS&RSI Strategy V3 for nifty 15min, SL-1.3", overlay=true)

// Inputs
atrLength = input.int(10, title="ATR Length")
factor = input.float(3.0, title="ATR Multiplier")
rsPeriod = input.int(55, title="RS Period")
rsiPeriod = input.int(14, title="RSI Period")
rsiThreshold = input.float(60, title="RSI Threshold")
stopLossPercent = input.float(2.0, title="Stop Loss (%)", step=0.1) // Adjustable Stop Loss in Percentage

// Supertrend Calculation
[supertrendDirection, supertrend] = ta.supertrend(factor, atrLength)

// RS Calculation
rs = (close - ta.lowest(close, rsPeriod)) / (ta.highest(close, rsPeriod) - ta.lowest(close, rsPeriod)) * 100

// RSI Calculation
rsi = ta.rsi(close, rsiPeriod)

// Entry Conditions
buyCondition = (supertrendDirection > 0) and (rs > 0) and (rsi > rsiThreshold)

// Exit Conditions
exitCondition1 = (supertrendDirection < 0)
exitCondition2 = (rs <= 0)
exitCondition3 = (rsi < rsiThreshold)
exitCondition = (exitCondition1 and exitCondition2) or (exitCondition1 and exitCondition3) or (exitCondition2 and exitCondition3)

// Plot Supertrend
plot(supertrend, title="Supertrend", color=supertrendDirection > 0 ? color.green : color.red, linewidth=2)

// Strategy Entry
if (buyCondition)
    strategy.entry("Buy", strategy.long)

// Add Stop Loss with strategy.exit
stopLossLevel = strategy.position_avg_price * (1 - stopLossPercent / 100)
strategy.exit("SL Exit", from_entry="Buy", stop=stopLossLevel)

// Strategy Exit (Additional Conditions)
if (exitCondition)
    strategy.close("Buy")

```

> Detail

https://www.fmz.com/strategy/477564

> Last Modified

2025-01-06 14:02:13
