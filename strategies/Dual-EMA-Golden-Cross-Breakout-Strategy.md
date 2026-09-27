
> Name

Dual-EMA-Golden-Cross-Breakout-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/975758c8a78b96ee18.png)
 
## Overview
The dual EMA golden cross breakout strategy is a trend-following and breakout trading strategy based on two exponential moving averages (EMAs) with different periods. It generates buy signals when a golden cross between the two EMAs emerges and sell signals when a death cross happens, in order to capture trend changes in prices. This strategy also combines the price breakout condition of EMAs to filter out false signals.   

## Strategy Logic   
The dual EMA golden cross breakout strategy is mainly based on the following logic:  

1. Use a shorter period EMA (26-day line) to capture short-term trends and a longer period EMA (200-day line) to determine the long-term trend direction.    

2. When the shorter period EMA crosses above the longer period EMA, it is called a "golden cross", indicating the trend changes from downtrend to uptrend, and a buy signal is generated.   

3. When the shorter period EMA crosses below the longer period EMA, it is called a "death cross", indicating the trend changes from uptrend to downtrend, and a sell signal is generated.  

4. When the cross signals occur, the price also needs to break through the EMAs to filter out false signals and ensure reliable trade signals.   

5. Apply stop loss and take profit techniques to control trading risks and lock in profits.   

## Advantages Analysis  
The dual EMA golden cross breakout strategy has the following advantages:  

1. Using dual EMAs to determine price trends and crossover signals can effectively track market movements.   

2. Combining price breakout filter signals avoids being misled by false crossover signals.   

3. Adopting simple and clear trading logic, easy to understand and implement.  

4. Applicable to different products and time frames, flexible and versatile.  

5. Configurable EMA parameters and stop loss/take profit conditions make it highly adaptable.  

## Risk Analysis
The dual EMA golden cross breakout strategy also has the following risks:   

1. Frequent crossovers may occur when prices oscillate, generating excessive trading signals. Adjusting EMA parameters properly can reduce crossover frequency.   

2. Dual EMAs sometimes have lagging performance and cannot respond to price changes in time. Other indicators can be combined for confirmation.  

3. Stop loss points that are too small may be easily triggered by slight price fluctuations, while take profit points that are too large may miss some profits. Stop loss and take profit positions need to be adjusted according to market conditions.  

4. Major trend judgments should be made before trade signals to avoid trading against the trend.  

## Optimization Directions
The dual EMA golden cross breakout strategy can be optimized in the following aspects:  

1. Apply machine learning algorithms to dynamically optimize EMA parameters so that they can better adapt to price fluctuations.  

2. Add other confirming signals like volume, Bollinger Bands etc. to improve signal quality.  

3. Incorporate deep learning predictions of price paths to place stop loss and take profit closer to optimal levels.  

4. Optimize strategies specifically for high frequency data to increase signal precision.   

5. Add adaptive adjustment mechanisms for stop loss to prevent excessive stopping out.  

## Conclusion
In summary, the dual EMA golden cross breakout strategy utilizes EMA crossover signals to determine price trends and turning points, and incorporates price breakout filters to avoid false signals. It is a reliable, steady and easy-to-implement trend following trading strategy. Further enhancements can be made through parameter optimization, signal filtering and adaptive adjustment. Its trading logic is simple and intuitive, suitable for all kinds of investors, and thus is one of the fundamental algorithmic trading strategies.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1_close|0|src: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|26|EMA-1|
|v_input_3|200|EMA-2|
|v_input_4|true|Show EMA ?|
|v_input_5|2|Take Profit (%)|
|v_input_6|true|Stop Loss (%)|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-26 00:00:00
end: 2024-01-25 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("EMA Buy/Sell Signal", shorttitle="EMABuySell", overlay=true)

// === INPUTS ===
src = input(close)
ema1Length = input(26, title='EMA-1')
ema2Length = input(200, title='EMA-2')

EMASig = input(true, title="Show EMA ?")
takeProfitPercent = input(2.0, title="Take Profit (%)") / 100
stopLossPercent = input(1, title="Stop Loss (%)") / 100

pema1 = ta.ema(src, ema1Length)
pema2 = ta.ema(src, ema2Length)

// Plotting EMAs
plot(EMASig ? pema1 : na, title='EMA-1', color=color.new(color.blue, 0), linewidth=2)
plot(EMASig ? pema2 : na, title='EMA-2', color=color.new(color.orange, 0), linewidth=2)

// EMA Crossover Buy Signal
EMACrossoverLong = ta.crossover(pema1, pema2)

// EMA Crossunder Short Signal
EMACrossoverShort = ta.crossunder(pema1, pema2)

// Crossover above EMA-200 Long Signal
CrossoverAboveEMA200 = ta.crossover(close, pema2)

// Trading logic for Long
if ((EMACrossoverLong and close > pema1 and close > pema2) or CrossoverAboveEMA200)
    strategy.entry("Buy", strategy.long, qty=1)

// Take Profit logic for Long
longCondition = close >= strategy.position_avg_price * (1 + takeProfitPercent)
if (strategy.position_size > 0 and longCondition)
    strategy.close("Buy")

// Stop Loss logic for Long
stopLossConditionLong = ta.crossunder(pema1, pema2)
if (strategy.position_size > 0 and stopLossConditionLong)
    strategy.close("Buy")

// Trading logic for Short
if (EMACrossoverShort and close < pema1 and close < pema2)
    strategy.entry("Sell", strategy.short, qty=1)

// Take Profit logic for Short
shortCondition = close <= strategy.position_avg_price * (1 - takeProfitPercent)
if (strategy.position_size < 0 and shortCondition)
    strategy.close("Sell")

// Stop Loss logic for Short
stopLossConditionShort = ta.crossover(pema1, pema2)
if (strategy.position_size < 0 and stopLossConditionShort)
    strategy.close("Sell")

// Visual Signals
plotshape(series=EMACrossoverLong or CrossoverAboveEMA200, title="Buy Signal", color=color.green, style=shape.triangleup, size=size.small)
plotshape(series=EMACrossoverShort, title="Sell Signal", color=color.red, style=shape.triangledown, size=size.small)

```

> Detail

https://www.fmz.com/strategy/440087

> Last Modified

2024-01-26 15:13:59
