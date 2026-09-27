
> Name

Multi-Technical-Indicator-Dynamic-Wave-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/a47a36da80c383b202.png)


#### Overview
This is a dynamic wave trading strategy based on multiple technical indicators, combining trend following and wave operation characteristics. The strategy seeks high-probability trading opportunities through the coordination of multiple technical indicators including EMA, ADX, RSI, and MACD. The system manages risk and profit through dynamic stop-loss and batch profit-taking methods.

#### Strategy Principle
The core logic of the strategy is based on the following key elements:
1. Trend Judgment: Uses EMA55 and EMA144 crossover relationships to determine market trend direction, combined with ADX indicator strength (threshold 30) for trend confirmation.
2. Entry Timing: Identifies oversold and overbought areas through RSI indicator (oversold 45, overbought 55) to judge pullback buying and rebound shorting opportunities.
3. Stop-Loss Mechanism: Adopts ATR-based dynamic stop-loss, with a stop-loss distance of 1.5 times ATR, which can adaptively adjust according to market volatility.
4. Profit Strategy: Uses 50-period high/low prices as profit targets, adopting a 50% position batch profit-taking approach.

#### Strategy Advantages
1. Multiple Indicator Verification: Improves trading signal reliability through the combined use of multiple indicators including EMA, ADX, and RSI.
2. Dynamic Risk Management: ATR-based dynamic stop-loss can adapt to different market environments, providing better risk control.
3. Progressive Profit-Taking: The batch profit-taking approach allows both securing partial profits and maintaining positions in strong trends.
4. Trend Confirmation: Inclusion of ADX indicator filtering helps avoid frequent trading in sideways markets.

#### Strategy Risks
1. False Breakout Risk: Misjudgments may occur during increased market volatility, suggesting the addition of volume confirmation.
2. Slippage Loss: Dynamic stop-loss may face significant slippage during rapid market movements.
3. Sideways Market Losses: Despite ADX filtering, consecutive small losses may still occur in oscillating markets.
4. Signal Lag: Multiple indicator combinations may lead to delayed entry signals, missing optimal position-building opportunities.

#### Strategy Optimization Directions
1. Indicator Parameter Optimization: Recommend historical backtesting optimization for parameters like EMA periods and RSI thresholds.
2. Stop-Loss Optimization: Consider adding trailing stop-loss for better profit protection.
3. Position Management: Suggest introducing a volatility-adaptive position management system.
4. Market Adaptability: Can add market environment classification to use different parameter combinations under different market conditions.

#### Summary
The strategy constructs a complete trading system through the coordination of multiple technical indicators. It emphasizes both trend capture and risk control, balancing risk and return through dynamic stop-loss and batch profit-taking methods. While there is room for optimization, it is overall a logically rigorous and practical trading strategy.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-18 00:00:00
end: 2025-02-17 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("Professional level trading system", overlay=true, max_labels_count=500)
// ===== Parameter Settings =====
x1 = input.float(1.5,"atrMultiples",step=0.1)
x2 = input.int(50,"kNumber of lines",step=1)
// EMAParameters
ema55_len = input.int(55, "EMA55Length")
ema144_len = input.int(144, "EMA144Length")
// ADXParameters
adx_len = input.int(14, "ADXLength")
adx_threshold = input.float(30.0, "ADXTrend filtering")
// RSIParameters
rsi_len = input.int(14, "RSILength")
rsi_oversold = input.float(45.0, "RSIOversold Threshold")
rsi_overbuy = input.float(55.0, "RSIOverbought Threshold")
// MACDParameters
macd_fast = input.int(12, "MACDFast line")
macd_slow = input.int(26, "MACDSlow line")
macd_signal = input.int(9, "MACDSignal Line")
// ===== Indicator calculation =====
// EMACalculation
ema55 = ta.ema(close, ema55_len)
ema144 = ta.ema(close, ema144_len)
// ADXCalculation (using standard functions)
[di_plus, di_minus, adx] = ta.dmi(adx_len, adx_len)
// RSICalculation
rsi = ta.rsi(close, rsi_len)
// MACDCalculation (Correcting parameter order).)
[macdLine, signalLine, histLine] = ta.macd(close, macd_fast, macd_slow, macd_signal)
// ===== Signal Logic =====
// Trend Conditions:EMA55 > EMA144 and ADX > 30
trendCondition = ema55 > ema144 and adx > adx_threshold
trendConditions = ema55 < ema144 and adx > adx_threshold
// Pullback Conditions:RSI < 45 and MACDhistogram > -0.002
pullbackCondition = rsi < rsi_oversold 
pullbackConditions = rsi > rsi_overbuy 
// Comprehensive Signal
entrySignal = trendCondition and pullbackCondition
entrySignals = trendConditions and pullbackConditions

// ===== Visualization =====
// DrawEMA
plot(ema55, "EMA55", color=color.new(#FFA500, 0))
plot(ema144, "EMA144", color=color.new(#008000, 0))
//plotshape(series=entrySignal,title="Buy Signal",location=location.belowbar,color=color.new(color.green, 0),style=shape.labelup,text="BUY",textcolor=color.new(color.white, 0))
s = strategy.position_avg_price ,s1 = strategy.position_size
le = false
le := low < ema144 and low[1] > ema144 and ema55 > ema144 ? true : s1 > 0 ? false : le[1] 
se = false
se := high > ema144 and high[1] < ema144 and ema55 < ema144 ? true : s1 < 0 ? false : se[1]
if entrySignal and low < ema144 and close > ema144
    strategy.entry("l",strategy.long)
strategy.exit("Take Half Profit","l",limit= ta.highest(x2),qty_percent = 50)
if s1 > 0 and low < (close - x1*ta.atr(12))[1]
    strategy.close_all("Dynamic Stop Loss")

if entrySignals and high > ema144 and close < ema144
    strategy.entry("s",strategy.short)   
strategy.exit("Take Half Profit","s",limit = ta.lowest(x2),qty_percent = 50)
if s1 < 0 and high > (close + x1*ta.atr(12))[1]
    strategy.close_all("Dynamic Stop Loss")

//plotshape(series=entrySignal,title="Buy Signal",location=location.belowbar,color=color.new(color.green, 0),style=shape.labelup,text="BUY",textcolor=color.new(color.white, 0))
//plot(close+x1*ta.atr(12))
//plot(close-x1*ta.atr(12))
//bgcolor(le ? color.red:na)
```

> Detail

https://www.fmz.com/strategy/482499

> Last Modified

2025-02-18 17:13:58
