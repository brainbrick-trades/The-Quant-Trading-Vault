
> Name

Dynamic-Trend-RSI-Crossover-Momentum-Enhancement-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8885676858bb3b96e7c.png)
![IMG](https://www.fmz.com/upload/asset/2d8ad1ff9c845b54bced8.png)





#### Overview
This strategy combines the Supertrend trend indicator with the RSI (Relative Strength Index) to create a trading system. It integrates trend following with momentum indicators to execute trades when market trends are clear and show good momentum. The system uses ATR (Average True Range) to calculate dynamic support and resistance levels, combined with RSI overbought/oversold signals for entry timing.

#### Strategy Principles
The core logic of the strategy is based on several key elements:
1. Supertrend indicator calculation is based on ATR and SMA, used to determine current market trend. The upper band is calculated by adding the factor multiplied by ATR to SMA, while the lower band subtracts the same value.
2. Buy signals are generated when price is above the Supertrend line, sell signals when below.
3. RSI indicator confirms market momentum, filtering trade signals through overbought/oversold levels (default 70 and 30).
4. Long conditions require Supertrend showing buy signal and RSI crossing upward from oversold zone.
5. Short conditions need Supertrend showing sell signal and RSI crossing downward from overbought zone.
6. Stop loss is set at the Supertrend line, take profit at 2x ATR distance.

#### Strategy Advantages
1. Combines trend and momentum confirmation, reducing false signal probability.
2. Uses dynamic ATR for stop loss and take profit, adapting to different market conditions.
3. Supertrend indicator effectively tracks trends, reducing ineffective trades in ranging markets.
4. RSI filter helps avoid entries in overextended markets.
5. System includes comprehensive risk management with dynamic stops and fixed risk ratio profit targets.

#### Strategy Risks
1. May generate frequent false breakout signals in sideways markets.
2. RSI overbought/oversold boundaries may not be flexible enough for certain market conditions.
3. Fixed ATR multiplier may not suit all market environments.
4. Stop loss placement may result in larger losses during quick reversals.
5. Strategy may face slippage risks during high volatility periods.

#### Strategy Optimization Directions
1. Introduce adaptive RSI thresholds, dynamically adjusting overbought/oversold levels based on market volatility.
2. Add volume confirmation mechanism to improve signal reliability.
3. Implement dynamic ATR multiplier adjustment to better match current market characteristics.
4. Include time filters to avoid trading during high volatility periods like market open/close.
5. Consider adding market environment filters, using different parameters based on trend strength.

#### Summary
The strategy combines Supertrend and RSI indicators to build a complete trend-following trading system. It performs well in trending markets, controlling risk through dynamic stops and reasonable profit targets. While it has some limitations, the proposed optimization directions can further enhance strategy stability and adaptability. The strategy is suitable for tracking medium to long-term trends while maintaining profitability with good risk control.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-04-11 00:00:00
end: 2025-02-19 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=5
strategy("Supertrend + RSI Strategy", overlay=true)

// Input Parameters
atrLength = input.int(10, title="ATR Length", minval=1)
factor = input.float(3.0, title="Supertrend Factor", step=0.1)
rsiLength = input.int(14, title="RSI Length", minval=1)
rsiOverbought = input.int(70, title="RSI Overbought Level")
rsiOversold = input.int(30, title="RSI Oversold Level")

// Supertrend Calculation
atr = ta.atr(atrLength)
upperBand = ta.sma(close, atrLength) + (factor * atr)
lowerBand = ta.sma(close, atrLength) - (factor * atr)
supertrend = 0.0
supertrend := close > nz(supertrend[1], close) ? lowerBand : upperBand
supertrendSignal = close > supertrend ? "Buy" : "Sell"

// RSI Calculation
rsi = ta.rsi(close, rsiLength)

// Trading Logic
longCondition = (supertrendSignal == "Buy") and (rsi > rsiOversold)
shortCondition = (supertrendSignal == "Sell") and (rsi < rsiOverbought)

// Entry and Exit Conditions
if longCondition
    strategy.entry("Long", strategy.long)

if shortCondition
    strategy.entry("Short", strategy.short)

// Plot Supertrend
plot(supertrend, title="Supertrend", color=color.new(color.blue, 0), linewidth=2, style=plot.style_line)

// Plot RSI Levels
hline(rsiOverbought, "Overbought", color=color.red)
hline(rsiOversold, "Oversold", color=color.green)
plot(rsi, title="RSI", color=color.orange, style=plot.style_stepline)

// Alerts
alertcondition(longCondition, title="Buy Alert", message="Supertrend + RSI Buy Signal")
alertcondition(shortCondition, title="Sell Alert", message="Supertrend + RSI Sell Signal")

```

> Detail

https://www.fmz.com/strategy/483027

> Last Modified

2025-02-21 10:00:53
