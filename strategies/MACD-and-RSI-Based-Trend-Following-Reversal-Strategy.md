
> Name

MACD-and-RSI-Based-Trend-Following-Reversal-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/16057189a7397864fe1.png)
 
### Overview

This strategy combines MACD, EMA and RSI indicators to implement trend following and reversal trading. It generates buy signals when MACD goes up through signal line and close price is above EMA; and sell signals when MACD falls below signal line and close price is below EMA to capture trends. Meanwhile, it trades reversals when RSI reaches overbought or oversold levels.

### Strategy Logic

1. Calculate MACD diffs and EMA.

    ```
    fastMA = ema(close, fast)
    slowMA = ema(close, slow) 
    macd = fastMA - slowMA
    signal = sma(macd, 9)
    ema = ema(close, input(200))
    ```

2. Generate buy signal: MACD diff (macd - signal) goes above 0 and close price is above EMA.

    ```
    delta = macd - signal
    buy_entry= close>ema and delta > 0 
    ```

3. Generate sell signal: MACD diff goes below 0 and close price is below EMA.

    ```
    sell_entry = close<ema and delta<0
    ```

4. Trade reversals when RSI reaches overbought or oversold levels.

    ```
    if (rsi > 70 or rsi < 30)
        reversal := true
    ```

### Advantage Analysis

1. Combine trend following and reversal trading to profit from both trends and reversals.  
2. Use MACD to judge trend directions and avoid false breakouts.
3. Filter noise with EMA.  
4. Enhance profitability with RSI for reversal trades.

### Risk Analysis

1. Reversal trades may incur losses in strong trending markets.  
2. Improper parameter tuning may increase trading frequency and slippage costs.
3. Reversal signals may have some lag, missing best entry prices.

Solutions:

1. Optimize parameters to find best combination.
2. Adjust reversal RSI thresholds properly.  
3. Consider adding stop loss to control losses.

### Optimization Directions 

1. Test EMA lengths.  
2. Optimize MACD parameters.
3. Test different RSI reversal thresholds.  
4. Consider combining with other indicators.

### Summary

This strategy combines MACD, EMA and RSI to organically implement trend following and reversal trading. MACD judges trend directions, EMA filters noise, and RSI captures reversal points. Such multi-indicator combination can better determine market movements, improving profitability while reducing false signals. Parameter optimization and stop loss management could be further improved to reduce unnecessary losses. Overall, this is a solid strategy framework with potential for steady profits.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|200|v_input_1|
|v_input_2|14|v_input_2|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-17 00:00:00
end: 2023-12-17 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © mbuthiacharles4

//Good with trending markets
//@version=4
strategy("CHARL MACD EMA RSI")

fast = 12, slow = 26
fastMA = ema(close, fast)
slowMA = ema(close, slow)
macd = fastMA - slowMA
signal = sma(macd, 9)

ema = ema(close, input(200))

rsi = rsi(close, input(14))
//when delta > 0  and close above ema buy

delta = macd - signal

buy_entry= close>ema and delta > 0
sell_entry = close<ema and delta<0 
var bought = false
var sold = false
var reversal = false
if (buy_entry and bought == false and rsi <= 70) 
    strategy.entry("Buy",true , when=buy_entry)
    bought := true
    
strategy.close("Buy",when= delta<0 or rsi > 70)
if (delta<0 and bought==true)
    bought := false

//handle sells

if (sell_entry and sold == false and rsi >= 30)
    strategy.entry("Sell",false , when=sell_entry)
    sold := true

strategy.close("Sell",when= delta>0 or rsi < 30)
if (delta>0 and sold==true)
    sold := false
    
if (rsi > 70 or rsi < 30)
    reversal := true
    placing = rsi > 70 ? high :low
    label.new(bar_index, placing, style=label.style_flag, color=color.blue, size=size.tiny)
if (reversal == true)
    if (rsi < 70 and sold == false and delta < 0)
        strategy.entry("Sell",false , when= delta < 0)
        sold := true
        reversal := false
    else if (rsi > 30 and bought == false and delta > 0)
        strategy.entry("Buy",true , when= delta > 0)
        bought := true
        reversal := false


```

> Detail

https://www.fmz.com/strategy/435775

> Last Modified

2023-12-18 17:53:38
