
> Name

Low-Lag-Triple-Moving-Average-Fast-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/d7ad3cd423121aaa02.png)

## Strategy Principle

This strategy uses three low-latency moving averages, including 12-period, 26-period and 55-period low-latency tema moving averages. These three moving averages represent respectively: fast moving average, medium speed moving average and slow moving average. When the fast moving average crosses the medium-speed moving average, a buy signal is generated; when the fast moving average crosses below the medium-speed moving average, a sell signal is generated. In this way, the market buying and selling points can be judged through the intersection of three moving averages to achieve high-frequency trading.

The template function tema() is defined in the code to calculate the low-latency tema moving average. The calculation formula is: TEMA = 2\*EMA - EMA(EMA), which is calculated using the quadratic exponential moving average EWMA. It is essentially a double exponential smoothing moving average. The main advantage is that it greatly reduces the lag. This can respond to price changes more quickly and improve the real-time judgment of trading signals.

Specifically, the entry judgment of this strategy is: when the fast moving average crosses the medium-speed moving average and the fast moving average is higher than the slow moving average, a buy signal is generated; when the fast moving average crosses below the medium-speed moving average and the fast moving average is lower than the slow moving average, a sell signal is generated.

## Advantage Analysis

The biggest advantage of this strategy is the rapid and accurate judgment of entry and exit. The three-moving average low-latency design greatly reduces lag and can quickly respond to price changes. At the same time, three moving averages are used for cross determination to avoid misjudgments.

In addition, this strategy is suitable for high-frequency trading and can capture short-term price fluctuations to make profits. Through the operation mode of fast in and fast out, you can make profits in volatile markets.

## Risk Analysis

The biggest risk of this strategy is the possibility of ultra-short-term arbitrage. The low-latency design of the three-moving average determines that it is extremely sensitive to price changes, and ultra-short-term shocks will occur in some markets. It's easy to get trapped at this time.

In addition, high-frequency trading requires more handling fees and slippage. If the profitability is insufficient, it is easy to be reversely arbitraged by transaction fees.

In addition, this strategy requires the trader to have a high real-time monitoring capability, needing timely updates to stop-loss and take-profit points.

## Optimization Direction

This strategy can be optimized from the following aspects:

1. Optimize the period parameters of the three moving averages to better adapt to different market characteristics;

2. Add volatility indicators or trading volume indicators to confirm signals and avoid being trapped in volatile market conditions;

3. Combine more factors to set stop-loss and take-profit mechanisms, achieving dynamic tracking;

4. Optimize position management and control single risk through fund management methods;

5. Combined with machine learning algorithms to dynamically optimize strategy parameters.

## Summary

This strategy is a three-moving average low-latency fast trading strategy. Through its low-latency design, it realizes fast in and fast out, which is suitable for high-frequency trading to capture short-term opportunities. The biggest advantage of this strategy is that signal judgment is fast and accurate, but the biggest disadvantage is that it is easy to be trapped in volatile market conditions. This article provides a comprehensive overview of this trading strategy through detailed principle analysis, advantage analysis, risk analysis and optimization discussion.

||

The strategy is named "Low Lag Triple Moving Average Fast Trading Strategy". Its main idea is to determine entries and exits based on the golden cross and death cross of three moving averages with different parameters and low lag design.  

## Strategy Principle 

The strategy uses three low-lag moving averages, including 12-, 26-, and 55-period low-lag TEMA. These three MAs represent fast, medium and slow MAs.  When the fast MA crosses over the medium MA, a buy signal is generated. When the fast MA crosses below the medium MA, a sell signal is generated. By using the crossover of the three MAs to determine market entry and exit points, high frequency trading can be achieved.

The template function tema() is defined in the code to calculate the low-lag TEMA. Its calculation formula is: TEMA = 2*EMA - EMA(EMA). It uses the double exponential moving average EWMA for calculation. Essentially it is a double smoothed EMA with the main merit of largely reducing the lagging effect. Thus it can respond to price changes faster and improve the timeliness of trading signals.  

Specifically, the entry rules of this strategy are: when the fast MA crosses over the medium MA and the fast MA is above the slow MA, a buy signal is generated. When the fast MA crosses below the medium MA and the fast MA is below the slow MA, a sell signal is generated.

## Advantage Analysis

The biggest advantage of this strategy is that the entries and exits are determined quickly and accurately. The low-lag design of the three MAs greatly reduces the lagging effect so that they can respond to price changes rapidly. Also, using the crossover of three MAs to determine signals avoids false signals.  

In addition, this strategy is suitable for high-frequency trading to capture profits from short-term price fluctuations. Through fast entries and exits it can profit from high volatility markets.

## Risk Analysis 

The biggest risk is that ultra short-term whipsaws may occur. Due to the high sensitivity to price changes from the low-lag design, some markets may experience high-frequency oscillations. Then whipsaws are very likely to happen.

Also, high-frequency trading requires paying relatively high commissions and slippage costs. If the profiting ability is insufficient, it is easy to suffer losses from the trading costs.

Moreover, this strategy requires the trader to have strong real-time monitoring abilities to update the stop loss and take profit timely.

## Optimization Directions

The strategy can be optimized from the following aspects:

1. Optimize the period parameters of the three MAs to better suit different market characteristics.  

2. Add volatility indicators or volume indicators to confirm signals and avoid whipsaws in ranging markets.

3. Incorporate more factors to set up dynamic trailing stop mechanisms.  

4. Optimize position sizing to control single trade risks through money management techniques.

5. Incorporate machine learning algorithms to dynamically optimize the strategy parameters.

## Conclusion
This is a low-lag triple moving average fast trading strategy. Through its low-lag design, fast entries and exits can be achieved, which is suitable for high-frequency trading to capture short-term opportunities. The biggest advantage of this strategy is that its signal determination is fast and accurate. The biggest disadvantage is that it is prone to be whipsawed in ranging markets. This article comprehensively summarizes this trading strategy through detailed analysis of its rationale, advantages, risks and optimization directions.  


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|0|Moving Average Type: temadelay|ema|emadelay|fastema|tema|nkclose|
|v_input_2|8|N|
|v_input_3|1.2|K|
|v_input_4|true|fracCap|
|v_input_5|200|TP|
|v_input_6|130|SL|
|v_input_7|true|TS|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-24 00:00:00
end: 2023-12-24 00:00:00
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("scalping low lag tema etal", shorttitle="Scalping tema",initial_capital=10000, overlay=true)
mav = input(title="Moving Average Type", defval="temadelay", options=["nkclose", "ema", "emadelay", "fastema", "tema", "temadelay"])
lenb = 3
N = input(8)
K = input(1.2)
fracCap = input(1.0)
in = close + K*mom(close,N)
source = close
length = 8
sigma  = 12.0
offset = 0.9
p = 4
// length = 10
// sigma  = 6.0
// offset = 0.85
tema(src,len) => fastemaOut = 2*ema(src, len) - ema(ema(src, len), len)


a = 0.0
b = 0.0
c = 0.0
if mav == "nkclose"
    a := ema(in, 12)
    b := a[1]
    c := a[2]
if mav == "ema"
    a := ema(close, 12)
    b := ema(close, 26)
    c := ema(close, 55)
if mav == "emadelay"
    a := ema(close, 12)
    b := a[1]
    c := a[2]
if mav == "fastema"
    a := ema(in, 12)
    b := ema(in, 26)
    c := ema(in, 55)
if mav == "tema"
    a := tema(close, 12)
    b := tema(close, 26)
    c := tema(close, 55)
if mav == "temadelay"
    a := tema(close, 12)
    b := a[1]
    c := a[2]

TP = input(200)
SL = input(130)
TS = input(1)
// TP = input(50)
// SL = input(110)
// TS = input(1)

orderSize = floor((fracCap * strategy.equity) / close)
long = cross(a, c) and a > b
short = cross(a, c) and a < b
plot(a, title="12", color=color.red, linewidth=1)
plot(b, title="26", color=color.blue, linewidth=1)
plot(c, title="55", color=color.green, linewidth=1)

strategy.entry("Long", strategy.long, qty=orderSize,  when=long)
strategy.entry("Short", strategy.short, qty=orderSize,  when=short)
// strategy.entry("Long", strategy.long,  100.0, when=long)
// strategy.entry("Short", strategy.short,  100.0, when=short)
// strategy.entry("Long", strategy.long, 100.0, when=long)
// strategy.entry("Short", strategy.short, 100.0, when=short)
// strategy.entry("Long", strategy.long, 1.0, when=long)
// strategy.entry("Short", strategy.short, 1.0, when=short)

TPP = (TP > 0) ? TP : na
SLP = (SL > 0) ? SL : na
TSP = (TS > 0) ? TS : na
// strategy.exit("Close Short", "Short", qty_percent=100, profit=TPP, loss=SLP, trail_points=TSP, when=long)
// strategy.exit("Close Long", "Long", qty_percent=100, profit=TPP, loss=SLP, trail_points=TSP, when=short)
// strategy.exit("Close Long", "Long", qty_percent=100, profit=TPP, loss=SLP, trail_points=TSP, when=long[1])
// strategy.exit("Close Short", "Short", qty_percent=100, profit=TPP, loss=SLP, trail_points=TSP, when=short[1])
strategy.exit("Close Long", "Long", qty_percent=100, profit=TPP, loss=SLP, trail_points=TSP)
strategy.exit("Close Short", "Short", qty_percent=100, profit=TPP, loss=SLP, trail_points=TSP)

```

> Detail

https://www.fmz.com/strategy/436519

> Last Modified

2023-12-25 14:24:38
