
> Name

Adaptive-Trend-Following-Strategy-Combining-Dual-Moving-Average-Crossover-and-RSI

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d928bf19c8cca8c9ebb3.png)
![IMG](https://www.fmz.com/upload/asset/2d8a42ee842e07ce2c2c0.png)





#### Overview
This strategy is a trend following system that combines a dual moving average crossover with the Relative Strength Index (RSI). It captures market trends through the crossover of 9-period and 21-period Exponential Moving Averages (EMA), while using RSI for overbought/oversold filtering and volume confirmation to enhance signal reliability. The strategy also incorporates a dynamic stop-loss mechanism based on Average True Range (ATR) for comprehensive risk control.

#### Strategy Principles
The core logic is based on several key elements:
1. Using fast EMA (9-period) and slow EMA (21-period) crossovers to identify potential trend changes
2. Filtering through RSI indicator, allowing trades only when RSI is between 40-60
3. Setting minimum volume threshold (100,000) as trade confirmation
4. Implementing 1.5x ATR as dynamic stop-loss distance for flexible risk control

Long signals are generated when the fast EMA crosses above the slow EMA, RSI is above 40, and volume exceeds the threshold. Conversely, short signals occur when the fast EMA crosses below the slow EMA, RSI is below 60, and volume confirms.

#### Strategy Advantages
1. Scientific indicator combination: integrating trend following, momentum, and volume analysis
2. Comprehensive risk control: multi-level risk management through RSI filtering and dynamic stops
3. Flexible parameters: key parameters can be optimized for different market characteristics
4. Strict signal confirmation: multiple conditions required, effectively reducing false signals
5. Clear execution logic: explicit rules facilitating live trading and backtesting

#### Strategy Risks
1. Frequent trades in ranging markets: multiple crossovers during consolidation
2. RSI filter may miss trend beginnings: RSI might be high at strong trend initiation
3. Volume filter might be too strict: challenging for low liquidity instruments
4. Fixed multiplier ATR stops may lack flexibility during extreme volatility
5. Absence of fixed take-profit levels may affect capital efficiency

#### Optimization Directions
1. Introduce adaptive parameters: dynamically adjust EMA periods and RSI thresholds based on volatility
2. Optimize stop-loss mechanism: implement multi-level stops using support/resistance
3. Add market environment filtering: incorporate trend strength indicators
4. Improve money management: adjust position sizes based on signal strength and volatility
5. Add take-profit mechanism: implement ATR-based dynamic take-profit levels

#### Summary
The strategy constructs a logically rigorous trend following system through scientific combination of classic technical indicators. Its multiple filtering mechanisms and risk control measures provide strong practical value. There's room for further improvement through the suggested optimizations. It's particularly suitable for volatile and liquid markets, but requires thorough testing and parameter optimization before implementation.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-11-07 00:00:00
end: 2025-02-18 08:00:00
period: 2d
basePeriod: 2d
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=5
strategy("Call & Put Options Strategy (Optimized)", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// ? Configuration Parameters
emaShort = input(9, title="Short EMA")
emaLong = input(21, title="Long EMA")
rsiLength = input(14, title="RSI Period")
rsiOverbought = input(60, title="RSI Overbought") // Adjusted for more signals
rsiOversold = input(40, title="RSI Oversold")   // More flexible to confirm buys
atrLength = input(14, title="ATR Period")
atrMult = input(1.5, title="ATR Multiplier for Stop Loss")
minVol = input(100000, title="Minimum Volume to Confirm Entry") // Volume filter

// ? Indicator Calculations
emaFast = ta.ema(close, emaShort)
emaSlow = ta.ema(close, emaLong)
rsi = ta.rsi(close, rsiLength)
atr = ta.atr(atrLength)
vol = volume

// ? Entry Signal Conditions
condCALL = ta.crossover(emaFast, emaSlow) and rsi > rsiOversold and vol > minVol
condPUT = ta.crossunder(emaFast, emaSlow) and rsi < rsiOverbought and vol > minVol

// ? Plot signals on the chart
plotshape(condCALL, location=location.belowbar, color=color.green, style=shape.labelup, title="CALL", size=size.small)
plotshape(condPUT, location=location.abovebar, color=color.red, style=shape.labeldown, title="PUT", size=size.small)

// ? Alert conditions
alertcondition(condCALL, title="CALL Signal", message="? CALL signal confirmed")
alertcondition(condPUT, title="PUT Signal", message="? PUT signal confirmed")

// ? Risk Management - Stop Loss and Take Profit
longStop = close - (atr * atrMult)
shortStop = close + (atr * atrMult)

strategy.entry("CALL", strategy.long, when=condCALL)
strategy.exit("CALL Exit", from_entry="CALL", stop=longStop)

strategy.entry("PUT", strategy.short, when=condPUT)
strategy.exit("PUT Exit", from_entry="PUT", stop=shortStop)

```

> Detail

https://www.fmz.com/strategy/482877

> Last Modified

2025-02-27 17:32:08
