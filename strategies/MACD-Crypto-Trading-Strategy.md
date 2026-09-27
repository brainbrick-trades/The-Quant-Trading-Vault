
> Name

MACD-Crypto-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/f8ca9f396516d00206.png)
 
### Overview

This is a simple yet efficient MACD crypto trading strategy specifically designed for cryptocurrency markets and suitable for higher timeframe charts like 1 hour, 4 hours, 1 day etc. The strategy uses the MACD indicator to determine market trend direction and trading signals are generated with simple moving average. The biggest advantage of this strategy is being simple, efficient and easy to understand and implement, especially suitable for the highly volatile crypto markets. However there are also some risks that need further optimization and improvement.  

### Strategy Logic

The strategy utilizes the MACD indicator to decide market trend and generate trade signals. MACD consists of the fast line, slow line and MACD histogram. The fast line is the short term moving average and the slow line is the long term moving average. When fast line crosses above slow line, it's a buy signal. When fast line crosses below slow line, it's a sell signal. The MACD histogram is the difference between fast line and slow line. Positive histogram means an upward trending bull market while negative histogram means a downward bear market. This strategy uses simple moving average to further validate the signals and avoid false signals. Specifically, only when both the MACD histogram and simple moving average are positive, the strategy will generate long signal to go long. When both the MACD histogram and simple moving average are negative, the strategy will generate short signal to go short. Using the MACD histogram to determine market direction can prevent trading against the trend.   

### Advantage Analysis 

The biggest advantages of this simple yet efficient strategy are:

1. Using MACD to determine market direction, a mature and reliable technical indicator to accurately judge the trend;

2. Combining simple moving average for signal filtering, avoiding false signals and improving accuracy;  

3. Specially designed for the highly volatile crypto markets where MACD performs the best;

4. The logic is simple and clear, easy to understand and implement, low barrier for adoption;

5. Can run on higher timeframes to lower trade frequency and reduce trading costs.

### Risk Analysis

However there are also some risks of this strategy:

1. Using simple moving average for filtering might miss the best entry price in some market condition;

2. No profit taking or stop loss in place might lead to huge single trade loss;

3. Possible lagging signals and false signals might cause unnecessary loss; 

4. Haven't considered the impact of trading timeframe and frequency on overall profitability.

These risks need to be addressed by further optimization.

### Optimization Directions

Based on the risks mentioned above, the strategy can be improved in the following directions:

1. Test different parameters and indicators combinations to find the optimal setting;

2. Add stop loss and profit taking logic to limit max single trade loss;

3. Optimize entry logic with more strict signal confirmation to ensure high quality signals;  

4. Consider the impact of different trading timeframe and frequency on the overall profitability.

Through optimizations in these directions, the stability, profitability and viability of this strategy can be greatly enhanced.  

### Summary

In summary, this is a MACD trading strategy with huge practical value. It's simple, efficient and easy to implement, perfect for people who want to get started with algo trading quickly. At the same time there is ample room for further optimizations to turn it into a stable money making algorithm suitable for long term live trading.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © SoftKill21

//@version=4
strategy("MACD crypto strategy", overlay=true)

// Getting inputs
//fast_length = input(title="Fast Length", type=input.integer, defval=12)
//slow_length = input(title="Slow Length", type=input.integer, defval=26)
//src = input(title="Source", type=input.source, defval=close)
//signal_length = input(title="Signal Smoothing", type=input.integer, minval = 1, maxval = 50, defval = 9)
//sma_source = input(title="Simple MA(Oscillator)", type=input.bool, defval=true)
//sma_signal = input(title="Simple MA(Signal Line)", type=input.bool, defval=false)

fast_length = 12
slow_length = 26
src = input(title="Source", type=input.source, defval=close)
signal_length = 9
sma_source = true
sma_signal = false

// Calculating
fast_ma = sma_source ? sma(src, fast_length) : ema(src, fast_length)
slow_ma = sma_source ? sma(src, slow_length) : ema(src, slow_length)
macd = fast_ma - slow_ma
signal = sma_signal ? sma(macd, signal_length) : ema(macd, signal_length)
hist = macd - signal



longcondition = hist > 0 
shortcondition = hist < 0 

//sl = input(0.5, title="SL")
//tp = input(0.1, title="tp")

strategy.entry("long",1,when=longcondition)
strategy.entry("short",0,when=shortcondition)

//strategy.exit("x_long", "long" ,loss = close * sl / syminfo.mintick, profit = close * tp / syminfo.mintick , alert_message = "closelong")
//strategy.entry("short",0, when= loss = close * sl / syminfo.mintick)

//strategy.exit("x_short", "short" , loss = close * sl / syminfo.mintick, profit  = close * tp / syminfo.mintick,alert_message = "closeshort")

// risk = input(2, type=input.float,title="Risk percentage of BALANCE")
// strategy.risk.max_intraday_loss(risk, strategy.percent_of_equity)
```

> Detail

https://www.fmz.com/strategy/440073

> Last Modified

2024-01-26 14:20:04
